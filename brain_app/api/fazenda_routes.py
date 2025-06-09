import traceback

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from brain_app.core.dependencies import get_db
from brain_app.core.logging_config import logger
from brain_app.schemas.fazenda_schema import (
    FazendaCreateSchema,
    FazendaReadSchema,
    FazendaUpdateSchema,
)
from brain_app.services.fazenda_service import FazendaService

router = APIRouter()


@router.get("/fazendas", response_model=list[FazendaReadSchema])
def list_fazendas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, gt=0),
    db: Session = Depends(get_db),
):
    service = FazendaService(db)
    fazendas = service.get_fazendas(skip=skip, limit=limit)
    return fazendas


@router.get("/fazendas/{fazenda_id}", response_model=FazendaReadSchema)
def get_fazenda(fazenda_id: int, db: Session = Depends(get_db)):
    service = FazendaService(db)
    fazenda = service.get_fazenda(fazenda_id)
    if not fazenda:
        logger.error(f"Erro ao solicitar uma fazenda: \n{traceback.format_exc()}")
        raise HTTPException(status_code=404, detail="Fazenda não encontrada")
    return fazenda


@router.post("/fazendas", response_model=FazendaReadSchema, status_code=201)
def create_fazenda(fazenda_create: FazendaCreateSchema, db: Session = Depends(get_db)):
    try:
        service = FazendaService(db)
        fazenda = service.create_fazenda(fazenda_create)
        return fazenda
    except ValueError as e:
        logger.error(f"Erro ao criar uma fazenda: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/fazendas/{fazenda_id}", response_model=FazendaReadSchema)
def update_fazenda(fazenda_id: int, fazenda_update: FazendaUpdateSchema, db: Session = Depends(get_db)):
    try:
        service = FazendaService(db)
        fazenda = service.update_fazenda(fazenda_id, fazenda_update)
    except ValueError as e:
        logger.error(f"Erro ao criar uma fazenda: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=str(e))
    return fazenda


@router.delete("/fazendas/{fazenda_id}", status_code=204)
def delete_fazenda(fazenda_id: int, db: Session = Depends(get_db)):
    try:
        service = FazendaService(db)
        service.delete_fazenda(fazenda_id)
    except ValueError as e:
        logger.error(f"Erro ao deletar uma fazenda: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=404, detail=str(e))
    return
