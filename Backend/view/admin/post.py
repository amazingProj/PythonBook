from fastapi import APIRouter, Response, status
from controller.migration import create_user
from model.user_model import User

router = APIRouter()


@router.post("/register")
async def create_new_user(user: User):
    message, status_code = create_user(user)
    response = Response(content=message, status_code=status.HTTP_201_CREATED if status_code == 201 else status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response
