from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from brain_app.schemas.fazenda_schema import FazendaCreate, FazendaRead, FazendaUpdate
from brain_app.services.fazenda_service import FazendaService
from brain_app.core.dependencies import get_db

router = APIRouter(prefix="/fazendas", tags=["fazendas"])

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
        raise HTTPException(status_code=404, detail="Fazenda não encontrada")
    return fazenda

@router.post("/", response_model=FazendaRead, status_code=201)
def create_fazenda(fazenda_create: FazendaCreate, db: Session = Depends(get_db)):
    service = FazendaService(db)
    try:
        fazenda = service.create_fazenda(fazenda_create)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return fazenda

@router.put("/{fazenda_id}", response_model=FazendaRead)
def update_fazenda(fazenda_id: int, fazenda_update: FazendaUpdate, db: Session = Depends(get_db)):
    service = FazendaService(db)
    try:
        fazenda = service.update_fazenda(fazenda_id, fazenda_update)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return fazenda

@router.delete("/{fazenda_id}", status_code=204)
def delete_fazenda(fazenda_id: int, db: Session = Depends(get_db)):
    service = FazendaService(db)
    try:
        service.delete_fazenda(fazenda_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return
