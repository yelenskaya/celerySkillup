from celery import current_app as current_celery_app
from celery.schedules import crontab
from fastapi import FastAPI

from app.dependencies import get_settings
from app.routes import router


def create_celery():
    celery_app = current_celery_app
    settings = get_settings()
    celery_app.conf.broker_url = settings.CELERY_BROKER_URL
    celery_app.conf.result_backend = settings.CELERY_RESULT_BACKEND

    celery_app.conf.task_routes = {
        'app.tasks.process_image_resizing': {'queue': 'resize'},
        'app.tasks.process_image_conversion': {'queue': 'convert'},
        'app.tasks.batch_convert_images': {'queue': 'convert'}
    }
    celery_app.conf.beat_schedule = {
        'batch_convert_images': {
            'task': 'app.tasks.batch_convert_images',
            'schedule': crontab(minute="*/1"),
        },
    }
    return celery_app


app = FastAPI()
app.celery_app = create_celery()
celery = app.celery_app
app.include_router(router)
