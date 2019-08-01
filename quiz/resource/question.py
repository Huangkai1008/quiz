import math

from flask import request, g

from quiz.schema.question import VoteSchema
from quiz.constants import AnswerVote
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
