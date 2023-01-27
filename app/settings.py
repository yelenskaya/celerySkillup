from pydantic import BaseSettings


class Settings(BaseSettings):
    AWS_REGION: str
    AWS_ACCESS_KEY_ID: str
    AWS_ACCESS_KEY: str
    ORIGINAL_S3_BUCKET: str
    RESULT_S3_BUCKET: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    MAX_BATCH_IMAGES: int
    BATCH_CONVERT_FORMAT: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        frozen = True
