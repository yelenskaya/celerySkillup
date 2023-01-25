from os import remove
from uuid import UUID

from celery import shared_task

from app.dependencies import get_s3_resource, get_settings
from app.image_transformation import resize_image
from app.s3_manager import get_file_object, get_original_image_key, get_resized_image_key, upload_file_object


@shared_task
def process_image_resizing(image_id: UUID, file_name: str, width: int, height: int) -> str:
    s3_resource = get_s3_resource()
    settings = get_settings()

    image = get_file_object(s3_resource, settings.ORIGINAL_S3_BUCKET, get_original_image_key(image_id, file_name))

    resized_image_path = resize_image(image, width, height)
    resized_image_s3_key = get_resized_image_key(image_id, file_name)

    with open(resized_image_path, 'rb') as resized_image:
        upload_file_object(s3_resource, settings.RESULT_S3_BUCKET, resized_image, resized_image_s3_key)

    remove(resized_image_path)
    return resized_image_s3_key
