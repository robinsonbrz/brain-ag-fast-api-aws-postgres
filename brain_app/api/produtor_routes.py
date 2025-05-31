from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from brain_app.schemas.produtor_schema import ProdutorCreate, ProdutorRead, ProdutorUpdate
from brain_app.services.produtor_service import ProdutorService
from brain_app.core.database import SessionLocal

router = APIRouter(prefix="/produtores", tags=["produtores"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[ProdutorRead])
def list_produtores(skip: int = Query(0, ge=0), limit: int = Query(100, gt=0), db: Session = Depends(get_db)):
    service = ProdutorService(db)
    produtores = service.get_produtores(skip=skip, limit=limit)
    return produtores

@router.get("/{produtor_id}", response_model=ProdutorRead)
def get_produtor(produtor_id: int, db: Session = Depends(get_db)):
    service = ProdutorService(db)
    produtor = service.get_produtor(produtor_id)
    if not produtor:
        raise HTTPException(status_code=404, detail="Produtor não encontrado")
    return produtor

@router.post("/", response_model=ProdutorRead, status_code=201)
def create_produtor(produtor_create: ProdutorCreate, db: Session = Depends(get_db)):
    service = ProdutorService(db)
    try:
        produtor = service.create_produtor(produtor_create)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return produtor

@router.put("/{produtor_id}", response_model=ProdutorRead)
def update_produtor(produtor_id: int, produtor_update: ProdutorUpdate, db: Session = Depends(get_db)):
    service = ProdutorService(db)
    try:
        produtor = service.update_produtor(produtor_id, produtor_update)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return produtor

@router.delete("/{produtor_id}", status_code=204)
def delete_produtor(produtor_id: int, db: Session = Depends(get_db)):
    service = ProdutorService(db)
    try:
        service.delete_produtor(produtor_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return
