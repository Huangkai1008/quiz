from quiz.model.question import Question, Answer, AnswerVote
from quiz.model.query import utils
from quiz.extensions import db


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
    return Question.query.get(question_id)


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


def create_answer(**attrs):
    """
    作出回答
    :param attrs:
    :return:
    """
    answer = Answer(**attrs)
    answer.create()
    return answer


def answer_vote_get(**params):
    """
    回答点赞信息获取
    :param params:
    :return:
    """
    filters = dict()

    if params.get('user_id'):
        filters['user_id'] = params['user_id']
    if params.get('answer_id'):
        filters['answer_id'] = params['answer_id']

    query = AnswerVote.query.filter_by(**filters)
    return query.first()


def answer_vote_update(**attrs):
    """
    回答点赞信息修改
    :return:
    """
    vote = AnswerVote(**attrs)
    vote.update()
    return vote


def answer_vote_bulk_update(votes: list):
    """
    回答点赞信息批量修改
    :param votes:
    :return:
    """
    for vote in votes:
        entity = AnswerVote(**vote)
        entity.update(commit=False)
    db.session.commit()


def answer_vote_delete(user_id, answer_id):
    """
    取消用户对于某个回答的点赞或者点踩
    :param user_id:
    :param answer_id:
    :return:
    """
    vote = AnswerVote.query.filter_by(user_id=user_id, answer_id=answer_id)
    vote.delete()
