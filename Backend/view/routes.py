from fastapi import APIRouter
from view.admin.route import router as admin_route
from view.user.route import router as user_route
from constant import ADMIN_PREFIX, USER_PREFIX

router = APIRouter()

router.include_router(admin_route, prefix=ADMIN_PREFIX)
router.include_router(user_route, prefix=USER_PREFIX)
