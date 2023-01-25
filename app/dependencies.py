from functools import lru_cache

from boto3 import resource

from app.settings import Settings


@lru_cache
def get_settings():
    return Settings()


@lru_cache
def get_s3_resource():
    settings = get_settings()
    return resource(
        's3',
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_ACCESS_KEY
    )
