from fastapi import APIRouter, Response
from controller.migration import create_user
from model.user_model import User
from util.fastapi_custom_response import create_ordinary_response

router = APIRouter()


@router.post("/register")
async def create_new_user(user: User):
    return create_ordinary_response(create_user(user))
