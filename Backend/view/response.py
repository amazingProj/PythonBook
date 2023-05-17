from util.constant import (NO_RESULT)
from util.string import response
from model.user_model import T


def response_create(response_message: str) -> str:
    message: str = 'Document stored successfully.' if response_message == 'created' else 'Failed to store the' \
                                                                                         ' document.'
    return response(message)


def response_login(hits: int) -> dict:
    message: str = 'Login successful.' if hits > NO_RESULT else 'Invalid credentials or user does not ' \
                                                                'exist. '
    return response(message)


def response_delete(is_succeeded: bool, user_id: T):
    message: str = "deleted successfully" if is_succeeded else "Invalid _id to delete"
    if user_id is None:
        return message

    return f'{message} {user_id}'

