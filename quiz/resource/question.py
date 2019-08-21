import math

from flask import request, g

from quiz import utils
from quiz.schema.question import VoteSchema
from quiz.constants import AnswerVote, AnswerSortChoice
from quiz.client.redis import api as redis_api
from quiz.model.query import question as question_api


def vote_answer(question_id, answer_id):
    """对回答点赞/取消点赞/点踩"""

    vote_schema = VoteSchema(request.json)
    vote_schema.validate()

    agree = vote_schema.instance['agree']
    user_id = g.current_user.id  # 用户id
    past_agree = _get_past_agree(user_id, answer_id)

    # 更新点赞状态
    redis_api.answer_vote_update(user_id, answer_id, agree)

    # 更新该回答的点赞数
    if agree == AnswerVote.agree.value and past_agree != agree:  # 点赞数 +1
        redis_api.answer_vote_count_incr(question_id, answer_id, 1)
    if agree in {AnswerVote.disagree.value, AnswerVote.cancel.value} \
            and past_agree != agree:  # 点赞数 -1
        redis_api.answer_vote_count_incr(question_id, answer_id, -1)


def _get_past_agree(user_id, answer_id):
    past_agree = redis_api.answer_vote_get(user_id, answer_id)
    if not past_agree:
        vote = question_api.answer_vote_get(user_id=user_id, answer_id=answer_id)
        past_agree = vote.agree if vote else None
    return past_agree and int(past_agree)


def get_answers(question_id, sort_choice, page, size):
    """
    获取问题下的回答列表
    :param question_id:
    :param sort_choice:
    :param page
    :param size
    :return:
    """
    if sort_choice == AnswerSortChoice.up_to_date.value:  # 按最新排序
        answers = question_api.get_answers(question_id, create_time_sort=False,
                                           need_paginate=True, page=page, size=size)
    elif sort_choice == AnswerSortChoice.star_prior.value:  # 按点赞数排行
        start = (page - 1) * size
        end = page * size - 1  # 因为Redis zrange的右区间是闭区间
        answer_ids = [int(answer_id) for answer_id in redis_api.answer_vote_count_range(question_id, start, end)]
        if answer_ids:  # 存在排行数据在缓存
            answers = question_api.get_answers(question_id, ids=answer_ids, id_field_sort=True)
        else:
            items = question_api.get_answers_by_star_prior(question_id, agree_type=AnswerVote.agree.value,
                                                           page=page, size=size)
            answers = list()
            for item in items:
                answer = dict(item.Answer)
                redis_api.answer_vote_count_add(question_id, answer['id'], item.vote_up_count)  # 写回到缓存
                answers.append(answer)
    else:  # 默认是智能排序
        items = question_api.get_answers_by_intelligence(question_id)
        items.sort(key=lambda x: confidence(up=x.vote_up_count, down=x.vote_down_count), reverse=True)
        answers = [dict(item.Answer) for item in utils.paginate(items, page, size)]

    return answers


def _confidence(up, down):
    """
    获取威尔逊得分区间 (Wilson score interval)
    http://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval#Wilson_score_interval
    :param up: 点赞的人数
    :param down: 点踩的人数
    :return:
    """
    n = up + down  # 样本人数
    z = 1.6
    phat = float(up) / n
    return (phat + z ** 2 / (2 * n) - z * math.sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)) / (1 + z ** 2 / n)


def confidence(up, down):
    score = 0 if up + down == 0 else _confidence(up, down)
    return score


def get_answer_comments(answer_id):
    """
    获取回答下的评论列表
    :param answer_id:
    :return:
    """
    pass
