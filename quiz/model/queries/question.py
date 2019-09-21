from sqlalchemy import func, or_

from quiz.model.question import Question, Answer, AnswerVote
from quiz.model.queries import utils
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


def create_answer(**attrs):
    """
    作出回答
    :param attrs:
    :return:
    """
    answer = Answer(**attrs)
    answer.create()
    return answer


def get_answers(question_id, **params):
    """获得答案列表"""
    conditions = list()
    sort_conditions = list()

    query = Answer.query

    if 'ids' in params:
        conditions.append(Answer.question_id.in_(params['ids']))
    if params.get('create_time_sort') is not None:
        sort_condition = Answer.create_time.asc() if params['create_time_sort'] else Answer.create_time.desc()
        sort_conditions.append(sort_condition)
    if params.get('id_field_sort'):
        sort_condition = func.field(Answer.id, *params['ids'])
        sort_conditions.append(sort_condition)

    conditions.append(Answer.question_id == question_id)

    query = query.filter(*conditions).order_by(*sort_conditions)

    if params.get('need_paginate'):
        query = utils.and_pagination(query, params['page'], params['size'])

    return query.all()


def get_answers_by_star_prior(question_id, agree_type, **params):
    """
    答案列表-赞数优先
    :return:
    """
    query = Answer.query \
        .outerjoin(AnswerVote, Answer.id == AnswerVote.answer_id) \
        .filter(AnswerVote.agree == agree_type,
                Answer.question_id == question_id) \
        .add_columns(func.count(AnswerVote.answer_id).label('vote_up_count')) \
        .order_by('vote_up_count')

    if params.get('size') and params.get('page'):
        query = utils.and_pagination(query, params['page'], params['size'])

    return query.all()


def get_answers_by_intelligence(question_id):
    """
    答案列表-智能排序
    :param question_id:
    :return:
    """
    query = Answer.query \
        .outerjoin(AnswerVote, Answer.id == AnswerVote.answer_id) \
        .filter(Answer.question_id == question_id) \
        .add_columns(func.count(or_(AnswerVote.agree == 1, None)).label('vote_up_count'),
                     func.count(or_(AnswerVote.agree == 0, None)).label('vote_down_count'))
    return query.all()


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
