from sqlalchemy.orm import Session
from . import models, schemas

# Puxa uma tarefa específica, pelo id
def get_tarefa(db: Session, tarefa_id: int):
    # .filter(model......) pega a taref que tem o id especificado (WHERE)
    # .first pega o primeiro resultado encontrado (SeNão, NONE)
    return db.query(models.Tarefa).filter(models.Tarefa.id == tarefa_id).first()

# Puxa todas as tarefas
def get_tarefas(db: Session):
    # .all para pegar a lista completa de tudo que tem na tabela
    return db.query(models.Tarefa).all()

# Cria uma nova tarefa
def create_tarefa(db: Session, tarefa: schemas.TarefaCreate):

    db_tarefa = models.Tarefa(
        titulo = tarefa.titulo,
        descricao = tarefa.descricao,
        concluida = tarefa.concluida,
        data_limite = tarefa.data_limite
    )

    db.add(db_tarefa)
    db.commit()
    db.refresh(db_tarefa)

    return db_tarefa

# Atualiza uma tarefa
def update_tarefa(db:Session, tarefa_id: int, tarefa: schemas.TarefaCreate):

    db_tarefa = get_tarefa(db, tarefa_id)

    if db_tarefa:

        db_tarefa.titulo = tarefa.titulo
        db_tarefa.descricao = tarefa.descricao
        db_tarefa.concluida = tarefa.concluida
        db_tarefa.data_limite = tarefa.data_limite

        db.commit()
        db.refresh(db_tarefa)

    return db_tarefa

# Deleta uma tarefa
def delete_tarefa(db:Session, tarefa_id: int):

    db_tarefa = get_tarefa(db, tarefa_id)

    if db_tarefa:
        db.delete(db_tarefa)
        db.commit()

    return db_tarefa