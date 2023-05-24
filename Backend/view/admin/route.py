from fastapi import APIRouter
from view.admin.post import router as post_router
from view.admin.delete import router as delete_router
from view.admin.get import router as get_router

router = APIRouter()

router.include_router(post_router)
router.include_router(delete_router)
router.include_router(get_router)
