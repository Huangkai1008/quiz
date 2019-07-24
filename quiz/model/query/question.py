from quiz.model.question import Question
from quiz.model.query import utils


def get_questions(page, size):
    """
    获得问题列表
    :param page
    :param size
    """
    query = Question.query

    query = utils.and_pagination(query, page, size)

    return query, query.count()


