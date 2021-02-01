import datetime

import jwt

from helpers.token.exceptions import ReadTokenException


def create_token(payload: dict, secret: str) -> str:
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(days=1)
    return jwt.encode(payload, secret, algorithm='HS256')


def read_token(token: str, secret: str) -> dict:
    try:
        return jwt.decode(token, secret, algorithms='HS256')
    except jwt.exceptions.PyJWTError:
        raise ReadTokenException