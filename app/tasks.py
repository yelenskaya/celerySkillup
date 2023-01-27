from os import remove

from celery import group, shared_task

from app.dependencies import get_s3_resource, get_settings
from app.image_transformation import convert_image, resize_image, validate_extension
from app.s3_manager import (
    delete_file,
    get_file_object,
    get_object_summaries,
    S3Prefix,
    upload_image_result
)


@shared_task
def process_image_resizing(file_key: str, s3_prefix: S3Prefix, width: int, height: int) -> str:
    s3_resource = get_s3_resource()
    settings = get_settings()
    s3_file_path = f'{s3_prefix}{file_key}'

    image = get_file_object(s3_resource, settings.ORIGINAL_S3_BUCKET, s3_file_path)
    resized_image_path = resize_image(image, width, height)

    upload_image_result(s3_resource, settings.RESULT_S3_BUCKET, resized_image_path, s3_file_path)
    remove(resized_image_path)

    return s3_file_path


@shared_task
def process_image_conversion(file_key: str, target_format: str, s3_prefix: S3Prefix = None):
    validate_extension(f'.{target_format}')

    s3_resource = get_s3_resource()
    settings = get_settings()

    original_s3_file_path = f'{s3_prefix}{file_key}' if s3_prefix else file_key

    image = get_file_object(s3_resource, settings.ORIGINAL_S3_BUCKET, original_s3_file_path)
    converted_image = convert_image(image, target_format, original_s3_file_path)

    upload_image_result(s3_resource, settings.RESULT_S3_BUCKET, converted_image.image_path, converted_image.s3_path)
    remove(converted_image.image_path)

    delete_file(s3_resource, settings.ORIGINAL_S3_BUCKET, original_s3_file_path)

    return converted_image.s3_path


@shared_task()
def batch_convert_images():
    settings = get_settings()

    summaries = get_object_summaries(
        get_s3_resource(), settings.ORIGINAL_S3_BUCKET, S3Prefix.BATCH.value, settings.MAX_BATCH_IMAGES
    )

    tasks = [process_image_conversion.s(summary.key, settings.BATCH_CONVERT_FORMAT) for summary in
             summaries if not summary.key == S3Prefix.BATCH.value]

    group(tasks).apply_async()
