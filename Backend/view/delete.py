from fastapi import APIRouter, status
from model.user_model import T
from typing import List
from controller.migration import delete_friend as friends_delete, delete_user, delete_users
from util.fastapi_custom_response import create_ordinary_response

router = APIRouter()


@router.delete("/user/{user_id}")
async def delete_user_by_id(user_id: T):
    return create_ordinary_response(delete_user(user_id))


@router.delete("/users")
async def delete_all():
    return create_ordinary_response(delete_users())


@router.delete("/friends/{user_id}")
async def delete_friends(body_friends: List[T], user_id: T):
    return create_ordinary_response(friends_delete(user_id, body_friends))

