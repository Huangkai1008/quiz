from wtforms.fields import StringField
from wtforms import Form

from quiz.form.base import QuizForm
from quiz.constants import AnswerSortChoice, PaginateSize


class QuestionForm(QuizForm):
    @property
    def data(self):
        query_param: dict = super().data
        query_param['sort_choice'] = query_param.get('sort_choice') or AnswerSortChoice.intelligence.value
        query_param['page'] = int(query_param['page']) if query_param.get('page') else 1
        query_param['size'] = int(query_param['size']) if query_param.get(
            'size') else PaginateSize.QUESTION_SIZE.value  # 默认取7条
        return query_param


class AnswerForm(Form):
    sort_choice = StringField('排序类型')

    @property
    def data(self):
        query_param: dict = super().data
        query_param['sort_choice'] = query_param.get('sort_choice') or AnswerSortChoice.intelligence.value
        query_param['page'] = int(query_param['page']) if query_param.get('page') else 1
        query_param['size'] = int(query_param['size']) if query_param.get(
            'size') else PaginateSize.ANSWER_SIZE.value  # 默认取10条
        return query_param
