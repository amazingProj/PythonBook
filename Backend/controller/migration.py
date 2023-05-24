from fastapi import status, HTTPException
from typing import Union, List

from controller.search import is_phone_exists, user as user_search, friends, user_full
from db.es import es, create_index
from db.es_conf import POSTS_INDEX_NAME
from db.query import delete_all_query
from model.user_model import T, User
from util.es_object import extract_data_from_es_response

create_index()


def create_user(user: User):
    is_phone_already_exists = is_phone_exists(user.phone_number)
    if is_phone_already_exists:
        return {}, status.HTTP_409_CONFLICT
    response = es.index(index=POSTS_INDEX_NAME, body=user.dict())

    new_user_id, status_code = extract_data_from_es_response(response)
    return new_user_id, status_code


def update_user(user_id: T, user: dict):
    message, status_code = user_search(user_id)
    for key in user.keys():
        if key not in message.keys():
            raise HTTPException(status_code=400, detail=f"There is no key named {key}")
        message[key] = user[key]
    response = es.update(index=POSTS_INDEX_NAME, id=user_id, body={"doc": message})
    return extract_data_from_es_response(response)


def add_friend_to_existing_user(user_id: T, friend_id: Union[T, List[T]]):
    response, status_code = user_full(user_id)
    user: User = response

    if isinstance(friend_id, str):
        user['friends'].append(friend_id)
    elif isinstance(friend_id, list):
        user['friends'].extend(friend_id)

    response = es.update(index=POSTS_INDEX_NAME, id=user_id, body={"doc": user})
    status_code = response.meta.status
    return response, status_code


def delete_friends(user_id, body_friends):
    response, status_code = user_full(user_id)
    if status_code == status.HTTP_404_NOT_FOUND:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    user: User = response
    user['friends'] = [friend_id for friend_id in user['friends'] if friend_id not in body_friends]

    response = es.update(index=POSTS_INDEX_NAME, id=user_id, body={"doc": user})

    # deletes all the user to be friend of them also
    for friend_id in body_friends:
        response, status_code = user_full(friend_id)
        if status_code == status.HTTP_404_NOT_FOUND:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        user: User = response
        user['friends'].remove([user_id])

        response = es.update(index=POSTS_INDEX_NAME, id=user_id, body={"doc": user})

    status_code = response.meta.status
    return response["result"], status_code


def release_related_friends(user_id, friends_of_user):
    for friend_id in friends_of_user:
        response, status_code = user_full(friend_id)
        if status_code == status.HTTP_404_NOT_FOUND:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        user: User = response
        user['friends'] = [user_id]

        response = es.update(index=POSTS_INDEX_NAME, id=user_id, body={"doc": user})

    status_code = response.meta.status
    return response["result"], status_code


def delete_user(user_id: T):
    message, status_code = friends(user_id)
    if status_code == status.HTTP_404_NOT_FOUND:
        return message, status_code
    if message:
        release_related_friends(user_id, message)
    response = es.delete(index=POSTS_INDEX_NAME, id=user_id)
    status_code = response.meta.status
    return response["result"], status_code


def delete_users():
    response = es.delete_by_query(index=POSTS_INDEX_NAME, body=delete_all_query())
    status_code = response.meta.status
    total = response["total"]
    deleted_count = response["deleted"]
    return f"from {total} deleted {deleted_count}", status_code

