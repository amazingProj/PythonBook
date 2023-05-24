from fastapi import APIRouter, Response, Query
from controller.migration import delete_user, delete_users
from model.user_model import T
from util.fastapi_custom_response import create_ordinary_response


router = APIRouter()


@router.delete("/user")
async def delete_user_by_id(user_id: T = Query(None, alias="user")):
    return create_ordinary_response(delete_user(user_id))


@router.delete("/users")
async def delete_all():
    return create_ordinary_response(delete_users())
