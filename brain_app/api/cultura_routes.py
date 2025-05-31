from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from brain_app.schemas.cultura_schema import CulturaCreate, CulturaRead, CulturaUpdate
from brain_app.services.cultura_service import CulturaService
from brain_app.core.dependencies import get_db

router = APIRouter(prefix="/culturas", tags=["culturas"])

@router.get("/", response_model=list[CulturaRead])
def list_culturas(skip: int = Query(0, ge=0), limit: int = Query(100, gt=0), db: Session = Depends(get_db)):
    service = CulturaService(db)
    culturas = service.get_culturas(skip=skip, limit=limit)
    return culturas

@router.get("/{cultura_id}", response_model=CulturaRead)
def get_cultura(cultura_id: int, db: Session = Depends(get_db)):
    service = CulturaService(db)
    cultura = service.get_cultura(cultura_id)
    if not cultura:
        raise HTTPException(status_code=404, detail="Cultura não encontrada")
    return cultura

@router.post("/", response_model=CulturaRead, status_code=201)
def create_cultura(cultura_create: CulturaCreate, db: Session = Depends(get_db)):
    service = CulturaService(db)
    try:
        cultura = service.create_cultura(cultura_create)
        return cultura
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{cultura_id}", response_model=CulturaRead)
def update_cultura(cultura_id: int, cultura_update: CulturaUpdate, db: Session = Depends(get_db)):
    service = CulturaService(db)
    try:
        cultura = service.update_cultura(cultura_id, cultura_update)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return cultura

@router.delete("/{cultura_id}", status_code=204)
def delete_cultura(cultura_id: int, db: Session = Depends(get_db)):
    service = CulturaService(db)
    try:
        service.delete_cultura(cultura_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return

@router.get("/fazenda/{fazenda_id}", response_model=list[CulturaRead])
def get_culturas_por_fazenda(
    fazenda_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, gt=0),
    db: Session = Depends(get_db),
):
    service = CulturaService(db)
    culturas = service.get_culturas_por_fazenda(fazenda_id, skip, limit)
    return culturas
