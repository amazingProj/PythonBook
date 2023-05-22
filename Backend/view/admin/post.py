from fastapi import APIRouter
from controller.migration import create_user
from model.user_model import User

router = APIRouter()


@router.post("/register")
async def create_new_user(user: User) -> str:
    message = create_user(user)
    return message
