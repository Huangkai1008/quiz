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

    # 更新点赞状态
    redis_api.answer_vote_update(user_id, answer_id, agree)

    past_agree = _get_past_agree(user_id, answer_id)

    # 更新该回答的点赞数
    if agree == AnswerVote.agree.value and past_agree != agree:  # 点赞数 +1
        redis_api.answer_vote_count_incr(question_id, answer_id, 1)
    if agree in {AnswerVote.disagree.value, AnswerVote.cancel.value} \
            and past_agree == agree:  # 点赞数 -1
        redis_api.answer_vote_count_incr(question_id, answer_id, -1)


def _get_past_agree(user_id, answer_id):
    past_agree = redis_api.answer_vote_get(user_id, answer_id)
    if not past_agree:
        vote = question_api.answer_vote_get(user_id=user_id, answer_id=answer_id)
        past_agree = vote.agree if vote else None
    return past_agree
