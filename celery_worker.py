# Celery quiz
from abc import ABC

from celery import current_app
from celery.app.task import Task as BaseTask

from quiz.app import create_app
from quiz.task import task_conf, celery


def make_celery(celery_app, flask_app):
    """Start the celery with the flask context"""
    celery_app.config_from_object(task_conf)

    class AppContextTask(BaseTask, ABC):
        def __call__(self, *args, **kwargs):
            """Execute task"""
            with flask_app.app_context():
                return self.run(*args, **kwargs)

    current_app.Task = AppContextTask

    return celery_app


app = create_app()

make_celery(celery, app)
