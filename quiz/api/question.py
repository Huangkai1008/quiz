from flask import Blueprint, request, g

from quiz.resource.auth import token_auth
from quiz.resource import question as question_resource
from quiz.form.question import QuestionForm, AnswerForm
from quiz.schema.question import QuestionSchema, AnswerSchema
from quiz.model.queries import question as question_api
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
    获取问题详情
    :return:
    """
    question = question_api.get_question(question_id)
    if not question:
        raise NotFoundException('你似乎来到了没有知识存在的荒原')
    return dict(question)


@bp.route('/<int:question_id>/answers', methods=['GET'])
@token_auth.login_required
def question_answers(question_id):
    """
    获取问题答案
    :param question_id:
    :return:
    """
    params = AnswerForm(**request.args.to_dict()).data

    answers = question_resource.get_answers(question_id, params['sort_choice'],
                                            params['page'],
                                            params['size'])
    return dict(answers=answers)


@bp.route('/<int:question_id>/answers', methods=['POST'])
@token_auth.login_required
def answer_question(question_id):
    """回答问题"""
    answer_schema = AnswerSchema(request.json)
    answer_schema.validate()

    user_id = g.current_user.id
    answer = question_api.create_answer(user_id=user_id, question_id=question_id, **answer_schema.instance)
    return dict(answer)


@bp.route('/<int:question_id>/answers/<int:answer_id>/vote', methods=['POST'])
@token_auth.login_required
def vote_answer(question_id, answer_id):
    """对回答表明态度"""
    question_resource.vote_answer(question_id, answer_id)


@bp.route('/<int:question_id>/answers/<int:answer_id>/comments', methods=['GET'])
@token_auth.login_required
def answer_comments_get(question_id, answer_id):
    """获取回答下所有评论"""
    pass
