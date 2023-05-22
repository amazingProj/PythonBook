from model.user_model import User
from db.es import es, create_index
from db.es_conf import (POSTS_INDEX_NAME)
from model.user_model import T
from db.query import delete_all_query
from controller.search import user as user_search
from typing import List
from util.es_object import extract_hits, extract_first_hit, extract_data_from_es_response
from fastapi import status

create_index()


def create_user(user: User):
    response = es.index(index=POSTS_INDEX_NAME, body=user.dict())
    # TODO set status code to be the relevant Http status code - Use HTTP_STATUS library
    new_user_id, status_code = extract_data_from_es_response(response)
    return new_user_id, status_code


def update_user(user_id: T, user: User):
    response = es.update(index=POSTS_INDEX_NAME, id=user_id, body={"doc": user.dict(exclude={"_id", "friends"})})
    return extract_hits(response)


def update_user_friends(user_id: T, friends: List[T]):
    response = user_search(user_id)
    user: User = extract_first_hit(response)
    # if user.friends:
    #     user['friends'] += friends
    # else:
    user['friends'] = friends
    response = es.update(index=POSTS_INDEX_NAME, id=user_id, body={"doc": user})
    return extract_hits(response)


def add_friend_to_existing_user(user_id: T, friend_id: T):
    response = user_search(user_id)
    user: User = extract_first_hit(response)
    # if user:
    #     user['friends'] += friend_id
    # else:
    user['friends'] = [friend_id]

    return es.update(index=POSTS_INDEX_NAME, id=user_id, body={"doc": user})


def delete_user(user_id: T):
    response = es.delete(index=POSTS_INDEX_NAME, id=user_id)
    return extract_hits(response)


def delete_users():
    response = es.delete_by_query(index=POSTS_INDEX_NAME, body=delete_all_query())
    return extract_hits(response)

