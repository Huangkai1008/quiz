from enum import Enum


class QuestionStatus(Enum):
    """
    问题的状态
    """
    o = 'open'
    c = 'close'
    d = 'draft'
