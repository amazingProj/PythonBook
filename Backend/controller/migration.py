from fastapi import status, HTTPException, Response
from typing import Union, List, Tuple, Any

from controller.search import is_phone_exists, friends, user_full
from db.es import es, create_index
from db.es_conf import POSTS_INDEX_NAME
from db.query import delete_all_query
from model.user_model import T, User
from util.es_object import extract_data_from_es_response

create_index()


def create_user(user: User) -> Tuple[dict, int]:
    is_phone_already_exists = is_phone_exists(user.phone_number)

    if is_phone_already_exists:
        return {}, status.HTTP_409_CONFLICT

    new_user_id, status_code = extract_data_from_es_response(es.index(index=POSTS_INDEX_NAME, body=user.dict()))
    return new_user_id, status_code


def update_user(user_id: T, user: dict) -> Union[str, int]:
    existing_user, status_code = user_full(user_id)

    for key in user.keys():
        if key not in existing_user.keys():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"There is no key named {key}")

        existing_user[key] = user[key]

    return replace_user_content(user_id, existing_user)


def add_friend(user_id: T, friend_id: Union[T, List[T]]) -> Union[Response, str, int]:
    response, status_code = user_full(user_id)
    user: dict = response

    if isinstance(friend_id, str):
        user["friends"].append(friend_id)
    elif isinstance(friend_id, list):
        user["friends"].extend(friend_id)
    else:
        return Response(content="Not valid body format", status_code=status.HTTP_400_BAD_REQUEST)

    return replace_user_content(user_id, user)


def delete_friend(user_id: T, body_friends: List[T]) -> Union[str, int]:
    user_, status_code = user_full(user_id)
    check_status(status_code)
    user: User = user_
    user.friends = [friend_id for friend_id in user.friends if friend_id not in body_friends]
    clean_friendship_friends(body_friends, user_id)

    return replace_user_content(user_id, user.dict())


def clean_friendship_friends(body_friends: List[T], user_id: T):
    for friend_id in body_friends:
        response, status_code = user_full(friend_id)
        check_status(status_code)
        user: User = response
        if user in user.friends:
            user.friends.remove([user_id])
        response = es.update(index=POSTS_INDEX_NAME, id=user_id, body={"doc": user})
    return response


def delete_user(user_id: T) -> Tuple[Any, Any]:
    message, status_code = friends(user_id)
    check_status(status_code)
    if message:
        clean_friendship_friends(message, user_id)
    es_delete_response = es.delete(index=POSTS_INDEX_NAME, id=user_id)
    status_code = es_delete_response.meta.status
    return es_delete_response["result"], status_code


def delete_users() -> Tuple[str, Any]:
    response = es.delete_by_query(index=POSTS_INDEX_NAME, body=delete_all_query())
    status_code = response.meta.status
    total = response["total"]
    deleted_count = response["deleted"]
    return f"from {total} deleted {deleted_count}", status_code


def replace_user_content(user_id: T, new_user_details: dict) -> Tuple[Any, Any]:
    response = es.update(index=POSTS_INDEX_NAME, id=user_id, body={"doc": new_user_details})
    status_code = response.meta.status
    return response["result"], status_code


def check_status(status_code: int):
    if status_code == status.HTTP_404_NOT_FOUND:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
