from quiz.task.persist import persist_answer_votes
from quiz.task import celery


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        10.0,
        persist_answer_votes.s('Done, Done'),
        name='sync'
    )
