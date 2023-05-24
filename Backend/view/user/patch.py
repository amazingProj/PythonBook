from fastapi import APIRouter
from controller.migration import *
from util.fastapi_custom_response import create_ordinary_response

router = APIRouter()


@router.patch("/{user_id}")
async def update_user_details(user_id: T, user: dict):
    return create_ordinary_response(update_user(user_id, user))
