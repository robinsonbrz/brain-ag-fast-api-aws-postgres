from fastapi import APIRouter
from brain_app.api import produtor_routes

router = APIRouter()
router.include_router(produtor_routes.router)