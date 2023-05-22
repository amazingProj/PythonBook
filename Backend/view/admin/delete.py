from fastapi import APIRouter
from controller.migration import delete_user, delete_users
from view.response import response_delete


router = APIRouter()


@router.delete("/{user_id}")
async def delete_user_by_id(user_id) -> str:
    message = delete_user(user_id)
    return response_delete(message, user_id)


@router.delete("/")
async def delete_all() -> str:
    message = delete_users()
    return response_delete(message, None)
