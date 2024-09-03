from fastapi import APIRouter

from .auth import router as auth_router
from .company import router as company_router
from .user import router as user_router
from .task import router as task_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(company_router)
router.include_router(user_router)
router.include_router(task_router)