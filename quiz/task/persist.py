from quiz.task import celery
from quiz.client.redis import api as redis_api
from quiz.constants import AnswerVote
from quiz.model.query import question as question_api


@celery.task
def persist_answer_votes():
    """
    持久化答案赞数
    :return:
    """
    # 更新用户对回答的赞/踩
    answer_votes = redis_api.answer_vote_scan()

    votes = list()
    for item in answer_votes:
        key, agree = item
        seqs = key.split('::')

        answer_id, user_id = int(seqs[0]), int(seqs[-1])

        if int(agree) in {AnswerVote.agree.value, AnswerVote.disagree.value}:
            votes.append(dict(
                user_id=user_id,
                answer_id=answer_id,
                agree=int(agree)
            ))
        else:  # 取消操作
            question_api.answer_vote_delete(user_id=user_id,
                                            answer_id=answer_id)
    question_api.answer_vote_bulk_update(votes)



