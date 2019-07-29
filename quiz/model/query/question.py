from quiz.model.question import Question, Answer
from quiz.model.query import utils


def get_questions(page, size):
    """
    获得问题列表
    :param page
    :param size
    """
    query = Question.query

    query = utils.and_pagination(query, page, size)

    return query.all(), query.count()


def get_question(question_id):
    """
    获取问题
    :param question_id:
    :return:
    """
    query = Question.query.get(question_id)
    return query.first()


def create_question(**attrs):
    """
    创建问题
    :param attrs:
    :return:
    """
    question = Question(**attrs)
    question.create()
    return question


def get_answers(page, size, **params):
    """
    获取回答列表
    :param page:
    :param size:
    :param params:
    :return:
    """
    conditions = list()

    query = Answer.query

    if params.get('question_id'):
        conditions.append(Answer.question_id == params['question_id'])

    query = utils.and_pagination(query, page, size)

    return query.all(), query.count()
