from wtforms import Form
from wtforms import IntegerField


class QuizForm(Form):
    page = IntegerField()
    size = IntegerField()

    @property
    def data(self):
        query_param: dict = super().data
        query_param['page'] = int(query_param['page']) if query_param.get('page') else 1
        query_param['size'] = (
            int(query_param['size']) if query_param.get('size') else 10
        )
        return query_param
