from flask import Blueprint, request, g

from quiz.resource.auth import token_auth
from quiz.form.question import QuestionForm
from quiz.schema.question import QuestionSchema
from quiz.model.query import question as question_api
from quiz.exceptions import NotFoundException

bp = Blueprint('question', __name__, url_prefix='/questions')


@bp.route('/', methods=['GET'])
def questions_get():
    """
    问题列表
    :return:
    """
    params = QuestionForm(**request.args.to_dict()).data
    questions, total = question_api.get_questions(params['page'], params['size'])
    return dict(questions=questions, total=total)


@bp.route('/', methods=['POST'])
@token_auth.login_required
def question_post():
    """
    提出问题
    :return:
    """
    question_schema = QuestionSchema(request.json)
    question_schema.validate()

    user_id = g.current_user.id
    question = question_api.create_question(user_id=user_id, **question_schema.instance)
    return dict(question)


@bp.route('/<int:question_id>', methods=['GET'])
@token_auth.login_required
def question_get(question_id):
    """
    获取问题详情  包括回答列表
    :return:
    """
    params = QuestionForm(**request.args.to_dict()).data

    question = question_api.get_question(question_id)
    if not question:
        raise NotFoundException('你似乎来到了没有知识存在的荒原')
    answers = question_api.get_answers(params['page'], params['size'])
    return dict(question=question, answers=answers)
