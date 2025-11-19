from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from .schemas import TarefaOut, TarefaCreate
from .database import get_db
from .crud import create_tarefa


router = APIRouter(prefix="/tarefas", tags=["tarefas"])


@router.post("/", response_model=TarefaOut, status_code=status.HTTP_201_CREATED)
def create_tarefa_route(payload: TarefaCreate, db: Session = Depends(get_db)):
    try:
        return create_tarefa(db=db, tarefa=payload)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Erro ao criar. Dados duplicados ou inválidos.")


@router.get("/", response_model=List[TarefaOut])  # Concluir...
def get_tarefas_route(db: Session = Depends(get_db)):
    pass
