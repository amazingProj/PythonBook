from fastapi import HTTPException, status
from typing import Any, Set

from constant import MAXIMUM_LENGTH_ELASTIC_SEARCH_ID, ERROR_MAXIMUM_LENGTH_MESSAGE


def option(candidate: str, options: Set[str]) -> str:
    if candidate.lower() not in options:
        message = f'Invalid gender for fields gender or interested_in. Must be one of: {",".join(options)}. '
        raise HTTPException(status_code=400, detail=message)
    return candidate


def is_str(candidate: Any) -> bool:
    return isinstance(candidate, str)


def str_check(candidate: Any) -> str:
    if is_str(candidate):
        return candidate
    raise ValueError('Invalid gender. Must be a string.')


def response(message: str):
    print(message)
    return {"message": message}


def check_valid_user_id(user_id: str):
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please use alias of user")
    if len(user_id) >= MAXIMUM_LENGTH_ELASTIC_SEARCH_ID:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{ERROR_MAXIMUM_LENGTH_MESSAGE} {MAXIMUM_LENGTH_ELASTIC_SEARCH_ID}")
    if user_id == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Not a valid empty user id")
    if user_id == "null":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Not a valid user id {user_id}")
    return
