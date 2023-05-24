from fastapi import APIRouter, Query, Response
from model.user_model import T
from typing import List
from controller.migration import delete_friends as friends_delete
from util.fastapi_custom_response import create_ordinary_response

router = APIRouter()


@router.delete("/friends")
async def delete_friends(body_friends: List[T], user_id: T = Query(None, alias="user")):
    return create_ordinary_response(friends_delete(user_id, body_friends))

