from fastapi import APIRouter, Query
from controller.migration import *
from util.fastapi_custom_response import create_ordinary_response

router = APIRouter()


@router.patch("/update/{user_id}")
async def update_user_details(user: dict, user_id: T):
    return create_ordinary_response(update_user(user_id, user))
