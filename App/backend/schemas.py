from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TarefaBase(BaseModel):
    titulo: str = Field(..., max_length=100, description="Título da tarefa")
    descricao: Optional[str] = Field(None, max_length=300, description="Detalhes da tarefa")
    concluida: bool = Field(False, description="Estado da tarefa")
    data_limite: Optional[datetime] = None


class TarefaCreate(TarefaBase):
    pass


class TarefaOut(TarefaBase):
    id: int
    data_criacao: datetime

    class Config:
        from_attributes = True