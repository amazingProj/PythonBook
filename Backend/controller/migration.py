from model.user_model import User
from db.es import es, create_index
from db.es_conf import (POSTS_INDEX_NAME)
from model.user_model import T
from db.query import delete_all_query

create_index()


def create_user(user: User):
    user_dict = user.dict()
    response = es.index(index=POSTS_INDEX_NAME, body=user_dict)
    return response, user_dict


def delete_user(user_id: T):
    response = es.delete(index=POSTS_INDEX_NAME, id=user_id)
    return response


def delete_users():
    response = es.delete_by_query(index=POSTS_INDEX_NAME, body=delete_all_query())
    return response


def update_user(user_id: T, user: User):
    response = es.update(index=POSTS_INDEX_NAME, id=user_id, body={"doc": user.dict(exclude={"_id", "friends"})})
    return response
