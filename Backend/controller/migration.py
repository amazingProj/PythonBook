from model.user_model import User
from db.es import es
from db.es_conf import (POSTS_INDEX_NAME)
import json
from model.user_model import T
from db.query import delete_all_query


def create_user(user: User):
    user_dict = user.dict()
    user_dict['location'] = json.dumps(user_dict['location'])
    response = es.index(index=POSTS_INDEX_NAME, body=user_dict)
    return response, user_dict


def delete_user(user_id: T):
    response = es.delete(index="your_index_name", id=user_id)
    return response


def delete_users():
    response = es.delete_by_query(index=POSTS_INDEX_NAME, body=delete_all_query())
    return response
