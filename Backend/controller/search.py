from fastapi import status, HTTPException

from db.query import \
    (login_query, user_minimal_details, user_friends_query, user_gender_query, user_matches_query, user_phone_query, \
     users_location_query, users_hobbies_query, all_users_query, user_full_details, users_by_ids_query, users_friends_query)
from db.es_conf import (POSTS_INDEX_NAME)
from db.es import es
from model.user_model import T
from util.es_object import extract_hits


def search(query):
    es_result = es.search(index=POSTS_INDEX_NAME, body=query)
    status_code = es_result.meta.status
    return extract_hits(es_result), status_code


def login(email: str, password: str):
    return search(login_query(email, password))


def user_search(tuple_response_status):
    response, status_code = tuple_response_status
    response = first_element("User does not exist in database", response)
    return response, status_code


def user(user_id: T):
    return user_search(search(user_minimal_details(user_id)))


def friends(user_id: T):
    response, status_code = search(user_friends_query(user_id))
    response = first_element("User does not exist in database", response)
    return response["friends"], status_code


def users():
    return search(all_users_query())


def gender(user_id: T):
    gender_str, status_code = search(user_gender_query(user_id))
    gender_str = first_element("This user is not exists", gender_str)
    return gender_str["gender"]


def matches(user_gender: str):
    return search(user_matches_query(user_gender))


def is_phone_exists(phone: str):
    return search((user_phone_query(phone)))[0] != []


def hobbies(hobbies_list):
    return search(users_hobbies_query(hobbies_list))


def locations(location_x, location_y):
    return search(users_location_query(location_x, location_y))


def user_full(user_id: T):
    return user_search(search(user_full_details(user_id)))


def multiple_users(users_ids):
    return search(users_by_ids_query(users_ids))


def users_friends(users_ids):
    return search(users_friends_query(users_ids))


def first_element(message, search_result):
    if not search_result:
        raise HTTPException(detail=f"{message}", status_code=status.HTTP_404_NOT_FOUND)
    return search_result[0]
