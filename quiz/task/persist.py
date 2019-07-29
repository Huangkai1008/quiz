from quiz.task import celery


@celery.task
def persist_answer_votes(arg):
    """
    持久化答案赞数
    :return:
    """
    pass
