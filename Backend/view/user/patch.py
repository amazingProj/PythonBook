from fastapi import APIRouter
from controller.migration import *
from view.response import *

router = APIRouter()


@router.patch("/{user_id}")
async def update_user_details(user_id: T, user: User):
    message = update_user(user_id, user)
    return message
