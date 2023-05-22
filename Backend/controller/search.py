from db.query import \
    (login_query, user_minimal_details, user_friends_query, user_gender_query, user_matches_query)
from db.es_conf import (POSTS_INDEX_NAME)
from db.es import es
from model.user_model import T
from util.es_object import extract_hits


def search(query):
    es_result = es.search(index=POSTS_INDEX_NAME, body=query)
    return extract_hits(es_result)


def login(email: str, password: str):
    return search(login_query(email, password))


def user(user_id: T):
    return search(user_minimal_details(user_id))


def friends(user_id: T):
    return search(user_friends_query(user_id))


def users():
    pass


def gender(user_id: T):
    return search(user_gender_query(user_id))[0]["gender"]


def matches(user_gender: str):
    return search(user_matches_query(user_gender))
