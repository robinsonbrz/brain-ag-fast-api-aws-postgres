from fastapi import APIRouter
from brain_app.api import produtor_routes, fazenda_routes, cultura_routes, dashboard_routes

router = APIRouter()
router.include_router(produtor_routes.router, prefix="/produtores")
router.include_router(fazenda_routes.router, prefix="/fazendas")
router.include_router(cultura_routes.router)
router.include_router(dashboard_routes.router)
