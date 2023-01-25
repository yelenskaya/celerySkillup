from os import path
from typing import BinaryIO
from uuid import uuid4

from PIL import Image

SUPPORTED_IMAGE_EXTENSIONS = frozenset(('.jpg', '.jpeg', '.png'))


class ImageFormatError(BaseException):
    pass


def validate_image_extension(file_name: str):
    file_extension = path.splitext(file_name)[1]
    if file_extension not in SUPPORTED_IMAGE_EXTENSIONS:
        raise ImageFormatError(f'File format {file_extension} is not supported. '
                               f'Supported formats are {SUPPORTED_IMAGE_EXTENSIONS}')


def resize_image(image_file: BinaryIO, width: int, height: int) -> str:
    with Image.open(image_file) as image:
        image.thumbnail((width, height))
        resized_image_path = f'{str(uuid4())}.{image.format.lower()}'
        image.save(resized_image_path, image.format)
    return resized_image_path
