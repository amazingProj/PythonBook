from fastapi import APIRouter
from view.user.get import router as get_route
from view.user.post import router as post_route
from view.user.patch import router as patch_route
from view.user.delete import router as delete_route

router = APIRouter()


router.include_router(get_route)
router.include_router(post_route)
router.include_router(patch_route)
router.include_router(delete_route)
