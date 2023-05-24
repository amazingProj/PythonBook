from fastapi import APIRouter, Response, Body
from controller.search import login
from controller.migration import *
from typing import List

router = APIRouter()


@router.post("/friends/{user_id}")
async def add_friends(user_id: T, body_friends: List[str] = Body(...)):
    friends_user, status_code_friends_request = friends(user_id)
    friends_to_add = [friend_id for friend_id in body_friends if not friends_user.__contains__(friend_id)]
    for friend_id in friends_to_add:
        # here is the opposite (friend_id, user_id) because I want the friend to add him the current user as a friend
        add_friend_to_existing_user(friend_id, user_id)

    result, status_code = add_friend_to_existing_user(user_id, friends_to_add)
    api_response = Response(content=result["result"], status_code=status_code)
    return api_response


@router.post("/login")
async def login_user(user: User):
    message, status_code = login(user.email, user.password)
    return message, status_code
