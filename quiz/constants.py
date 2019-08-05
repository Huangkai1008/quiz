from enum import Enum


class PaginateSize(Enum):
    """
    分页参数
    """
    QUESTION_SIZE = 7
    ANSWER_SIZE = 10


class QuestionStatus(Enum):
    """
    问题的状态
    """
    o = 'open'
    c = 'close'
    d = 'draft'


class AnswerSortChoice(Enum):
    """
    回答排序选择
    """
    up_to_date = 'up_to_date'  # 最新
    star_prior = 'star_prior'  # 赞数优先
    intelligence = 'intelligence'  # 智能排序


class AnswerVote(Enum):
    """
    回答赞同的状态
    """
    agree = 1
    disagree = 0
    cancel = -1


class QuestionRedisKey(Enum):
    """
    问题模块redis键
    """
    ANSWER_VOTE = 'quiz:answer:vote'  # 点赞状态
