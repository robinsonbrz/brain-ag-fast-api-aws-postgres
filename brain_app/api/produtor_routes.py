from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from brain_app.schemas.produtor_schema import ProdutorCreate, ProdutorRead, ProdutorUpdate
from brain_app.services.produtor_service import ProdutorService
from brain_app.core.dependencies import get_db
from brain_app.core.logging_config import logger
import traceback

router = APIRouter(prefix="/produtores", tags=["produtores"])

@router.get("/", response_model=list[ProdutorRead])
def list_produtores(skip: int = Query(0, ge=0), limit: int = Query(100, gt=0), db: Session = Depends(get_db)):
    service = ProdutorService(db)
    produtores = service.get_produtores(skip=skip, limit=limit)
    return produtores

@router.get("/{cpf_cnpj}", response_model=ProdutorRead)
def get_produtor_por_cpf_cnpj(cpf_cnpj: str, db: Session = Depends(get_db)):
    service = ProdutorService(db)
    produtor = service.get_produtor_por_cpf_cnpj(cpf_cnpj)
    if not produtor:
        logger.error(f"Erro ao solicitar um produtor: \n{traceback.format_exc()}")
        raise HTTPException(status_code=404, detail="Produtor não encontrado")
    return produtor

@router.post("/", response_model=ProdutorRead, status_code=201)
def create_produtor(
    produtor_create: ProdutorCreate, 
    db: Session = Depends(get_db)):
    service = ProdutorService(db)
    try:
        produtor = service.create_produtor(produtor_create)
    except ValueError as e:
        logger.error(f"Erro ao criar um produtor: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=str(e))
    return produtor

@router.put("/{cpf_cnpj}", response_model=ProdutorRead)
def update_produtor_por_cpf_cnpj(
    cpf_cnpj: str, 
    produtor_update: ProdutorUpdate, 
    db: Session = Depends(get_db)
):
    service = ProdutorService(db)
    try:
        produtor = service.update_produtor_por_cpf_cnpj(cpf_cnpj, produtor_update)
    except ValueError as e:
        logger.error(f"Erro ao atualizar um produtor: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=404, detail=str(e))
    return produtor

@router.delete("/{cpf_cnpj}", status_code=204)
def delete_produtor_por_cpf_cnpj(cpf_cnpj: str, db: Session = Depends(get_db)):
    service = ProdutorService(db)
    try:
        service.delete_produtor_por_cpf_cnpj(cpf_cnpj)
    except ValueError as e:
        logger.error(f"Erro ao deletar um produtor: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=404, detail=str(e))
