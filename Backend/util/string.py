from fastapi import HTTPException
from typing import Any, Set


def option(candidate: str, options: Set[str]) -> str:
    if candidate.lower() not in options:
        message = f'Invalid. Must be one of: {",".join(options)}'
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
