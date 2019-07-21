from enum import Enum


class UserSchemas(Enum):
    REG_SCHEMA = dict(
        type='object',
        required=['username', 'email', 'password'],
        properties={
            'username': {'type': 'string'},
            'password': {'type': 'string'},
            'email': {'type': 'string', 'format': 'email'}
        }
    )

    LOGIN_SCHEMA = dict(
        type='object',
        required=['username', 'password'],
        properties={
            'username': {'type': 'string'},
            'password': {'type': 'string'}
        }
    )
