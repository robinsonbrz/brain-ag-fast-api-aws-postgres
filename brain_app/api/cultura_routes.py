import traceback

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from brain_app.core.dependencies import get_db
from brain_app.core.logging_config import logger
from brain_app.schemas.cultura_schema import CulturaCreateSchema, CulturaReadSchema, CulturaUpdateSchema
from brain_app.services.cultura_service import CulturaService

router = APIRouter()


@router.get("/culturas", response_model=list[CulturaReadSchema])
def list_culturas(skip: int = Query(0, ge=0), limit: int = Query(100, gt=0), db: Session = Depends(get_db)):
    service = CulturaService(db)
    culturas = service.get_culturas(skip=skip, limit=limit)
    return culturas


@router.get("/culturas/{cultura_id}", response_model=CulturaReadSchema)
def get_cultura(cultura_id: int, db: Session = Depends(get_db)):
    try:
        service = CulturaService(db)
        cultura = service.get_cultura(cultura_id)
        if not cultura:
            raise HTTPException(status_code=404, detail="Cultura não encontrada")
        return cultura
    except HTTPException as e:
        logger.error(f"Erro ao solicitar uma cultura: {e}\n{traceback.format_exc()}")
        raise


@router.post("/culturas", response_model=CulturaReadSchema, status_code=201)
def create_cultura(cultura_create: CulturaCreateSchema, db: Session = Depends(get_db)):
    service = CulturaService(db)
    try:
        cultura = service.create_cultura(cultura_create)
        return cultura
    except ValueError as e:
        logger.error(f"Erro ao criar uma cultura: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/culturas/{cultura_id}", response_model=CulturaReadSchema)
def update_cultura(cultura_id: int, cultura_update: CulturaUpdateSchema, db: Session = Depends(get_db)):
    service = CulturaService(db)
    try:
        cultura = service.update_cultura(cultura_id, cultura_update)
    except ValueError as e:
        logger.error(f"Erro ao atualizar uma cultura: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=404, detail=str(e))
    return cultura


@router.delete("/culturas/{cultura_id}", status_code=204)
def delete_cultura(cultura_id: int, db: Session = Depends(get_db)):
    service = CulturaService(db)
    try:
        service.delete_cultura(cultura_id)
    except ValueError as e:
        logger.error(f"Erro ao deletar uma cultura: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=404, detail=str(e))
    return


@router.get("/culturas/fazenda/{fazenda_id}", response_model=list[CulturaReadSchema])
def get_culturas_por_fazenda(
    fazenda_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, gt=0),
    db: Session = Depends(get_db),
):
    service = CulturaService(db)
    culturas = service.get_culturas_por_fazenda(fazenda_id, skip, limit)
    return culturas
