from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from .schemas import TarefaOut, TarefaCreate
from .database import get_db
from .crud import create_tarefa, get_tarefas, update_tarefa, delete_tarefa


router = APIRouter(prefix="/tarefas", tags=["tarefas"])


@router.post("/", response_model=TarefaOut, status_code=status.HTTP_201_CREATED)
def create_tarefa_route(payload: TarefaCreate, db: Session = Depends(get_db)):
    try:
        return create_tarefa(db=db, tarefa=payload)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Erro ao criar. Dados duplicados ou inválidos.")


@router.get("/", response_model=List[TarefaOut]) #Porque aqui tem esse response_model, de onde vem esse list, e é realmente necessário que tenha isso?
def get_tarefas_route(db: Session = Depends(get_db)):
    return get_tarefas(db)


@router.put("/{tarefa_id}", response_model=TarefaOut)
def update_tarefa_route(tarefa_id: int, payload: TarefaCreate, db: Session = Depends(get_db)):
    db_tarefa = update_tarefa(db, tarefa_id=tarefa_id, tarefa=payload)
    if db_tarefa is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada")
    return db_tarefa


@router.delete("/{tarefa_id}", response_model=TarefaOut)
def delete_tarefa_route(tarefa_id: int, db: Session = Depends(get_db)):
    db_tarefa = delete_tarefa(db, tarefa_id=tarefa_id)
    if db_tarefa is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada")
    return db_tarefa