from fastapi import FastAPI
from .database import Base, engine
from . import models, routers

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(routers.router)
