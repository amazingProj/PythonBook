from fastapi import APIRouter, Query
from controller.search import \
    (
        login,
        user as search_user,
        user_friends as friends
    )
from controller.migration import *
from view.response import *
from typing import List


router = APIRouter()


@router.get("/{user_id}/friends")
async def user_friends(user_id: T):
    message = friends(user_id)
    return message


@router.get("/")
async def filter_users(hobbies: List[str] = Query(None),
                       location_x: float = Query(None),
                       location_y: float = Query(None)):
    pass


@router.get("/{user_id}")
async def user_by_id(user_id):
    return search_user(user_id)


@router.post("/{user_id}/friends")
async def add_friends(user_id: T, body_friends: List[T]):
    friends_user = friends(user_id)
    friends_to_add = [friend_id for friend_id in body_friends if not friends_user.__contains__(friend_id)]
    return friends_user | friends_to_add


@router.post("/register")
async def create_new_user(user: User) -> dict:
    message, user_dict = create_user(user)
    response_create(message['result'])
    return user_dict


@router.post("/login")
async def login_user(user: User) -> dict:
    message = login(user.email, user.password)
    return response_login(message['hits']['total']['value'])


@router.delete("/{user_id}")
async def delete_user_by_id(user_id) -> str:
    message = delete_user(user_id)
    return response_delete(message, user_id)


@router.delete("/")
async def delete_all() -> str:
    message = delete_users()
    return response_delete(message, None)


@router.patch("/{user_id}")
async def update_user_details(user_id: T, user: User):
    message = update_user(user_id, user)
    return message


