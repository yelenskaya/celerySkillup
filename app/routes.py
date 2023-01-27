from uuid import uuid4

from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile

from app.dependencies import get_s3_resource, get_settings
from app.image_transformation import ImageFormatError, validate_image_extension
from app.s3_manager import S3Prefix, upload_file_object
from app.schemas import Notification
from app.settings import Settings
from app.tasks import process_image_resizing

router = APIRouter(prefix='/images', tags=['images'])


@router.post('/resize', status_code=202, response_model=Notification)
def trigger_resize_image(
        upload_file: UploadFile,
        width: int = Form(),
        height: int = Form(),
        s3=Depends(get_s3_resource),
        settings: Settings = Depends(get_settings),
):
    try:
        validate_image_extension(upload_file.filename)
    except ImageFormatError as e:
        raise HTTPException(status_code=400, detail=str(e))

    s3_file_key = f'{uuid4()}/{upload_file.filename}'
    upload_file_object(
        s3, settings.ORIGINAL_S3_BUCKET, upload_file.file, f'{S3Prefix.SINGLE}{s3_file_key}'
    )

    process_image_resizing.delay(s3_file_key, S3Prefix.SINGLE, width, height)

    return {'message': 'Started resizing the image'}
