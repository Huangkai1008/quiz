from quiz.extensions import redis_cli
from quiz.constants import QuestionRedisKey


def follow_add(follower_id, followed_id):
    """
    添加关注
    :param follower_id: 关注者id
    :param followed_id: 被关注者id
    key --> quiz:user:$user_id:followed(set)  用户关注的
            quiz:user:$user_id:followers(set) 用户的粉丝
    value --> user_id  关注用户id/被关注用户id
    :return:
    """
    redis_cli.pipe.sadd(f'quiz:user:{follower_id}:followed', followed_id)
    redis_cli.pipe.sadd(f'quiz:user:{followed_id}:followers', follower_id)
    redis_cli.pipe.execute()


def follow_remove(follower_id, followed_id):
    """
    取消关注
    :param follower_id:  关注者id
    :param followed_id:  被关注者id
    key --> quiz:user:$user_id:followed(set)  用户关注的
            quiz:user:$user_id:followers(set) 用户的粉丝
    value --> user_id  关注用户id/被关注用户id
    :return:
    """
    redis_cli.pipe.srem(f'quiz:user:{follower_id}:followed', followed_id)
    redis_cli.pipe.srem(f'quiz:user:{followed_id}:followers', follower_id)
    redis_cli.pipe.execute()


def followed_get(user_id):
    """
    获取用户的关注用户
    :param user_id: 用户id
    :return:
    """
    return redis_cli.r.smembers(f'quiz:user:{user_id}:followed')


def followers_get(user_id):
    """
    获取用户的粉丝用户
    :param user_id:
    :return:
    """
    return redis_cli.r.smembers(f'quiz:user:{user_id}:followers')


def answer_vote_update(user_id, answer_id, agree):
    """
    点赞状态改变
    :param answer_id  问题id
    :param user_id  用户id
    :param agree 赞同状态
    key   -->  quiz:answer:vote(hash)
    value -->  {$answer_id::$user_id : $agree, ...}
    :return:
    """
    return redis_cli.r.hset(
        QuestionRedisKey.ANSWER_VOTE.value, f'{answer_id}::{user_id}', agree
    )


def answer_vote_get(user_id, answer_id):
    """
    获得点赞状态
    :param answer_id  问题id
    :param user_id  用户id
    :return:
    """
    return redis_cli.r.hget(
        QuestionRedisKey.ANSWER_VOTE.value, f'{answer_id}::{user_id}'
    )


def answer_vote_scan():
    """
    获得所有点赞状态
    :return:
    """
    return redis_cli.r.hscan_iter(QuestionRedisKey.ANSWER_VOTE.value)


def answer_vote_count_add(question_id, answer_id, score):
    """
    答案点赞数条目添加
    :param question_id:
    :param answer_id:
    :param score:
    :return:
    """
    redis_cli.r.zadd(
        f'quiz:question:{question_id}:answer:vote:count', mapping={answer_id: score}
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
        f'quiz:question:{question_id}:answer:vote:count', increment, answer_id
    )


def answer_vote_count_range(question_id, start=0, stop=-1):
    """
    答案点赞数排行 Desc
    :param question_id: 问题id
    :param start: 开始
    :param stop: 结束位置
    :return:
    """
    return redis_cli.r.zrevrange(
        f'quiz:question:{question_id}:answer:vote:count', start, stop
    )
