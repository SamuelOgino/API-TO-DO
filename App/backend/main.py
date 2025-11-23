from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from . import routers

Base.metadata.create_all(bind=engine)

app = FastAPI()


# --- CONFIGURAÇÃO DO CORS (Crucial para o Frontend funcionar) ---
# Permite que seu HTML (que roda numa porta) fale com a API (que roda em outra)
origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://127.0.0.1:8000",
    "*"  # Em produção não use *, mas para testes libera tudo
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Libera POST, GET, PUT, DELETE, OPTIONS
    allow_headers=["*"],
)


app.include_router(routers.router)
