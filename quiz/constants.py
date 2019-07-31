from enum import Enum


class QuestionStatus(Enum):
    """
    问题的状态
    """
    o = 'open'
    c = 'close'
    d = 'draft'


class AnswerVote(Enum):
    """
    回答赞同的状态
    """
    agree = 1
    disagree = -1
    cancel = 0


class QuestionRedisKey(Enum):
    """
    问题模块redis键
    """
    ANSWER_VOTE = 'quiz:answer:vote'    # 点赞状态
