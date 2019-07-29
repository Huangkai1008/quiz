from quiz.schema.base import Schema
from quiz.schema.schemas import QuestionSchemas


class QuestionSchema(Schema):
    _schema = QuestionSchemas.QU_SCHEMA.value


class AnswerSchema(Schema):
    _schema = QuestionSchemas.ANSWER_SCHEMA.value
