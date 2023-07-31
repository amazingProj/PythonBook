from fastapi import APIRouter
from view.route import router as user_route
from constant import USER_PREFIX

router = APIRouter()

router.include_router(user_route, prefix=USER_PREFIX)
