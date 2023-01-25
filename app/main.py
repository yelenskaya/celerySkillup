from celery import current_app as current_celery_app
from fastapi import FastAPI

from app.dependencies import get_settings
from app.routes import router


def create_celery():
    celery_app = current_celery_app
    celery_app.config_from_object(get_settings(), namespace="CELERY")
    return celery_app


app = FastAPI()
app.celery_app = create_celery()
celery = app.celery_app
app.include_router(router)
