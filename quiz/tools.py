from collections.abc import Iterator

from flask import Flask as _Flask

from quiz import utils


class QuizFlask(_Flask):
    """
    自定义flask
    """

    json_encoder = utils.ExtendedEncoder

    def make_response(self, rv):
        if rv is None:
            rv = dict()

        if isinstance(rv, Iterator):
            rv = list(rv)

        return super(QuizFlask, self).make_response(rv)
