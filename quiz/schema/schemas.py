from enum import Enum


class UserSchemas(Enum):
    REG_SCHEMA = dict(
        type='object',
        required=['username', 'email', 'password'],
        properties={
            'username': {'type': 'string', 'maxLength': 128},
            'password': {'type': 'string'},
            'email': {'type': 'string', 'format': 'email'}
        },
        additionalProperties=False
    )

    LOGIN_SCHEMA = dict(
        type='object',
        required=['username', 'password'],
        properties={
            'username': {'type': 'string'},
            'password': {'type': 'string'}
        },
        additionalProperties=False
    )


class QuestionSchemas(Enum):
    QU_SCHEMA = dict(
        type='object',
        required=['title'],
        properties={
            'title': {'type': 'string', 'maxLength': 255},
            'content': {'type': 'string'}
        },
        additionalProperties=False
    )

    ANSWER_SCHEMA = dict(
        type='object',
        required=['content'],
        properties={
            'content': {'type': 'string'}
        },
        additionalProperties=False
    )