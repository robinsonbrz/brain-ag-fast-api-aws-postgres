from fastapi import APIRouter

from brain_app.api import cultura_routes, dashboard_routes, fazenda_routes, produtor_routes

router = APIRouter()
router.include_router(produtor_routes.router)
router.include_router(fazenda_routes.router)
router.include_router(cultura_routes.router)
router.include_router(dashboard_routes.router)
