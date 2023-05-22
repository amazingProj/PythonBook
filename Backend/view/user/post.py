from fastapi import APIRouter
from controller.search import \
    (login, friends as friends)
from controller.migration import *
from view.response import *
from typing import List
from util.es_object import extract_first_hit

router = APIRouter()


@router.post("/friends/{user_id}")
async def add_friends(user_id: T, body_friends: List[T]):
    friends_user = friends(user_id)
    friends_user = extract_first_hit(friends_user)["friends"]
    friends_to_add = [friend_id for friend_id in body_friends if not friends_user.__contains__(friend_id)]
    for friend_id in friends_to_add:
        # here is the opposite (friend_id, user_id) because I want the friend to add him the current user as a friend
        add_friend_to_existing_user(friend_id, user_id)

    return update_user_friends(user_id, friends_user + friends_to_add)


@router.post("/login")
async def login_user(user: User) -> dict:
    message = login(user.email, user.password)
    return response_login(message['hits']['total']['value'])
