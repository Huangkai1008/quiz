import json
from collections import Iterator

from flask import Flask as _Flask
from flask import current_app
from flask import Response

from quiz import utils


class QuizResponse(Response):
    """
    自定义响应
    """

    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, (list, dict)):
            response = Response(json.dumps(response, cls=utils.ExtendedEncoder),
                                mimetype=current_app.config['JSONIFY_MIMETYPE'])
        return super(QuizResponse, cls).force_type(response, environ)


class QuizFlask(_Flask):
    """
    自定义flask
    """
    response_class = QuizResponse

    def make_response(self, rv):
        if rv is None:
            rv = dict()

        if isinstance(rv, Iterator):
            rv = list(rv)

        return super(QuizFlask, self).make_response(rv)