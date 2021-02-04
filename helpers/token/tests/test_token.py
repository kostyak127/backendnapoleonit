import pytest

from helpers.token.exceptions import ReadTokenException
from helpers.token.token import create_token, read_token


@pytest.fixture()
def token_data() -> dict:
    return {'id': 1}


@pytest.fixture()
def secret_key() -> str:
    return 'SUPERSECRET'


def test_read_valid_token(token_data, secret_key):
    request_token = create_token(token_data, secret_key)
    response_token = read_token(request_token, secret_key)

    response_token.pop('exp')

    assert response_token == token_data


def test_read_invalid_token(secret_key):
    invalid_token = 'wrong token'

    with pytest.raises(ReadTokenException):
        read_token(invalid_token, secret_key)


def test_read_old_token(token_data, secret_key):
    request_token = create_token(token_data, secret_key, lifetime=-7)

    with pytest.raises(ReadTokenException):
        read_token(request_token, secret_key)