from fastapi import APIRouter
from model.user_model import User
from controller.search import \
    (
        login,
        user as search_user
    )
from controller.migration import \
    (
        create_user,
        delete_user,
        delete_users
    )
from view.response import *

router = APIRouter()


@router.get("/{user_id}")
async def user_by_id(user_id):
    return search_user(user_id)


@router.post("/register/")
async def create_item(user: User) -> dict:
    message, user_dict = create_user(user)
    response_create(message['result'])
    return user_dict


@router.post("/login/")
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
