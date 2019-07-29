from quiz.extensions import redis_cli
from quiz.constants import QuestionRedisKey


def answer_vote_update(user_id, answer_id, agree):
    """
    点赞状态改变
    :param answer_id  问题id
    :param user_id  用户id
    :param agree 赞同状态
    key   -->  quiz:question:answer:vote(hash)
    value -->  {$answer_id::$user_id : $agree, ...}
    :return:
    """
    return redis_cli.r.hset(
        QuestionRedisKey.ANSWER_VOTE.value,
        f'{answer_id}::{user_id}',
        agree
    )


def answer_vote_get(user_id, answer_id):
    """
    获得点赞状态
    :param answer_id  问题id
    :param user_id  用户id
    :return:
    """
    return redis_cli.r.hget(
        QuestionRedisKey.ANSWER_VOTE.value,
        f'{answer_id}::{user_id}'
    )


def answer_vote_count_incr(question_id, answer_id, increment):
    """
    答案点赞数增加/减少
    :param question_id 问题id
    :param answer_id   回答id
    :param increment   增加量/减少量
    key    -->  quiz:question:$question_id:answer:vote:count(sortedSet)
    :return:
    """
    return redis_cli.r.zincrby(
        f'quiz:question:{question_id}:answer:vote:count',
        increment,
        f'answer:{answer_id}'
    )
