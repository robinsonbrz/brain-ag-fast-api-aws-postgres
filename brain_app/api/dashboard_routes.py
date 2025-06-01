from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from brain_app.core.dependencies import get_db
from brain_app.services.dashboard_service import DashboardService
from brain_app.schemas.dashboard_schema import DashboardResponse
from brain_app.core.logging_config import logger
import traceback

router = APIRouter()

@router.get("/dashboard", response_model=DashboardResponse)
def dashboard(db: Session = Depends(get_db)):
    service = DashboardService(db)
    return service.get_dashboard_data()
