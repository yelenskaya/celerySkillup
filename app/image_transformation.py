from os import path
from typing import BinaryIO
from uuid import uuid4

from PIL import Image
from pydantic import BaseModel

SUPPORTED_IMAGE_EXTENSIONS = frozenset(('.jpg', '.jpeg', '.png'))


class ImageFormatError(BaseException):
    pass


class ConvertedImage(BaseModel):
    s3_path: str
    image_path: str


def validate_image_extension(file_name: str):
    file_extension = path.splitext(file_name)[1]
    validate_extension(file_extension)


def validate_extension(file_extension: str):
    if file_extension not in SUPPORTED_IMAGE_EXTENSIONS:
        raise ImageFormatError(f'File format {file_extension} is not supported. '
                               f'Supported formats are {SUPPORTED_IMAGE_EXTENSIONS}')


def replace_file_extension(file_path: str, target_format: str) -> str:
    return f'{path.splitext(file_path)[0]}.{target_format}'


def resize_image(image_file: BinaryIO, width: int, height: int) -> str:
    with Image.open(image_file) as image:
        image.thumbnail((width, height))
        resized_image_path = f'{str(uuid4())}.{image.format.lower()}'
        image.save(resized_image_path, image.format)
    return resized_image_path


def convert_image(image_file: BinaryIO, image_format: str, original_s3_path: str) -> ConvertedImage:
    with Image.open(image_file) as image:
        converted_image_path = f'{str(uuid4())}.{image_format}'
        image.save(converted_image_path, image_format.upper())
    converted_s3_path = replace_file_extension(original_s3_path, image_format)
    return ConvertedImage(s3_path=converted_s3_path, image_path=converted_image_path)
