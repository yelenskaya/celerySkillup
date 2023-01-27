from enum import StrEnum
from logging import getLogger
from typing import BinaryIO

from boto3.resources.base import ServiceResource
from botocore.exceptions import ClientError
from botocore.response import StreamingBody
from pydantic import BaseModel

logger = getLogger(__name__)


class S3Prefix(StrEnum):
    SINGLE = 'single/'
    BATCH = 'batch/'


class S3Error(Exception):
    pass


class S3FileNotFoundError(S3Error):
    pass


class S3ObjectSummary(BaseModel):
    key: str


def get_file_object(resource: ServiceResource, bucket: str, object_key: str) -> StreamingBody:
    try:
        file = resource.Object(bucket, object_key).get()['Body']
    except ClientError as e:
        logger.error(f'Could not get file {object_key} from the bucket. Error: {e.response["Error"]}')
        if e.response['Error']['Code'] == 'NoSuchKey':
            raise S3FileNotFoundError(f'File with key {object_key} does not exist')
        raise S3Error
    return file


def upload_file_object(resource: ServiceResource, bucket: str, file: BinaryIO, target_object_key: str):
    try:
        resource.Bucket(bucket).upload_fileobj(file, target_object_key)
    except ClientError as e:
        logger.error(f'Failed to upload recording to S3\n{e.response["Error"]}')
        raise S3Error


def get_object_summaries(
        resource: ServiceResource, bucket: str, folder_name: str = None, max_number: int = None
) -> list[S3ObjectSummary]:
    try:
        if folder_name:
            summaries = resource.Bucket(bucket).objects.filter(Prefix=folder_name)
        else:
            summaries = resource.Bucket(bucket).objects.all()

    except ClientError as e:
        logger.error(f'Failed to get files from S3\n{e.response["Error"]}')
        raise S3Error

    if max_number:
        summaries = summaries.limit(max_number)

    return [S3ObjectSummary(key=summary.key) for summary in summaries]


def delete_file(resource: ServiceResource, bucket: str, file_key: str):
    try:
        resource.Object(bucket, file_key).delete()
    except ClientError as e:
        logger.error(f'Failed to delete file {file_key} from S3\n{e.response["Error"]}')
        raise S3Error


def upload_image_result(resource: ServiceResource, bucket: str, transformed_image_path: str, s3_file_path: str):
    with open(transformed_image_path, 'rb') as transformed_image:
        upload_file_object(resource, bucket, transformed_image, s3_file_path)
