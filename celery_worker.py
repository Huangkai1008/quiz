# Celery quiz
from abc import ABC

from celery import current_app
from celery.schedules import crontab
from celery.app.task import Task as BaseTask

from quiz.app import create_app
from quiz.task import task_conf, celery
from quiz.task.persist import persist_answer_votes


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


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute=0,
                hour='*/3'),
        persist_answer_votes.s(),
        name='persist answer votes per 3 hours'
    )

