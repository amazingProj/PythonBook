from fastapi import APIRouter, Body
from controller.migration import *
from model.user_model import User
from util.algorithm import add_friends_algorithm
from util.fastapi_custom_response import create_json_response
from typing import List

router = APIRouter()


@router.post("/friends/{user_id}")
async def add_friends(user_id: T, body_friends: List[str] = Body(...),):
    return add_friends_algorithm(body_friends, user_id)


@router.post("/register")
async def create_new_user(user: User):
    return create_json_response(create_user(user))
