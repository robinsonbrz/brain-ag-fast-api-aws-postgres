from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from brain_app.schemas.fazenda_schema import FazendaCreate, FazendaRead, FazendaUpdate
from brain_app.services.fazenda_service import FazendaService
from brain_app.core.dependencies import get_db
from brain_app.core.logging_config import logger
import traceback

router = APIRouter()

@router.get("/", response_model=list[FazendaRead])
def list_fazendas(skip: int = Query(0, ge=0), limit: int = Query(100, gt=0), db: Session = Depends(get_db)):
    service = FazendaService(db)
    fazendas = service.get_fazendas(skip=skip, limit=limit)
    return fazendas

@router.get("/{fazenda_id}", response_model=FazendaRead)
def get_fazenda(fazenda_id: int, db: Session = Depends(get_db)):
    service = FazendaService(db)
    fazenda = service.get_fazenda(fazenda_id)
    if not fazenda:
        logger.error(f"Erro ao solicitar uma fazenda: \n{traceback.format_exc()}")
        raise HTTPException(status_code=404, detail="Fazenda não encontrada")
    return fazenda

@router.post("/", response_model=FazendaRead, status_code=201)
def create_fazenda(fazenda_create: FazendaCreate, db: Session = Depends(get_db)):
    try:
        service = FazendaService(db)
        fazenda = service.create_fazenda(fazenda_create)
        return fazenda
    except ValueError as e:
        logger.error(f"Erro ao criar uma fazenda: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=str(e))
    

@router.put("/{fazenda_id}", response_model=FazendaRead)
def update_fazenda(fazenda_id: int, fazenda_update: FazendaUpdate, db: Session = Depends(get_db)):
    try:
        service = FazendaService(db)
        fazenda = service.update_fazenda(fazenda_id, fazenda_update)
    except ValueError as e:
        logger.error(f"Erro ao criar uma fazenda: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=str(e))
    return fazenda

@router.delete("/{fazenda_id}", status_code=204)
def delete_fazenda(fazenda_id: int, db: Session = Depends(get_db)):
    try:
        service = FazendaService(db)
        service.delete_fazenda(fazenda_id)
    except ValueError as e:
        logger.error(f"Erro ao deletar uma fazenda: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=404, detail=str(e))
    return
