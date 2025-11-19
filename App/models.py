from sqlalchemy import Column, Integer, String, Boolean, DateTime
from .database import Base
import datetime

class Tarefa(Base):
    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    concluida = Column(Boolean, default=False)
    data_limite = Column(DateTime, nullable=True)

    data_criacao = Column(DateTime, default=datetime.datetime.now)
