import json

from collections.abc import Iterator

from flask import Flask as _Flask
from flask import Response, current_app

from quiz import utils


class QuizFlask(_Flask):
    """自定义flask"""

    json_encoder = utils.ExtendedEncoder

    def make_response(self, rv):
        if rv is None:
            rv = dict()

        if isinstance(rv, (list, Iterator)):
            return Response(
                json.dumps(list(rv), cls=utils.ExtendedEncoder),
                mimetype=current_app.config['JSONIFY_MIMETYPE'],
            )

        return super().make_response(rv)
