from db.query import \
    (login_query, user_exclude_friend)
from db.es_conf import (POSTS_INDEX_NAME)
from db.es import es
from model.user_model import T


def search(query):
    return es.search(index=POSTS_INDEX_NAME, body=query)


def login(email: str, password: str):
    return search(login_query(email, password))


def user(user_id: T):
    return search(user_exclude_friend(user_id))

