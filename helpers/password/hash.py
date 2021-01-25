import bcrypt

from helpers.password.exception import GeneratePasswordHashException, CheckPasswordHashException


def generate_password(pwd: str) -> bytes:
    try:
        return bcrypt.hashpw(
            password=pwd.encode(),
            salt=bcrypt.gensalt()
        )
    except (TypeError, ValueError) as error:
        raise GeneratePasswordHashException(str(error))


def check_hash(pwd: str, hsh: bytes) -> bool:
    try:
        result = bcrypt.checkpw(
            password=pwd.encode(),
            hashed_password=hsh
        )
    except (TypeError, ValueError) as error:
        raise CheckPasswordHashException(str(error))

    return result