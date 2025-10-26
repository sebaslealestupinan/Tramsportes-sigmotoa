from contextlib import asynccontextmanager

from database import create_db_and_tables
from fastapi import FastAPI

from bus import bus
from rutas import endpoints

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    print("Base de datos funcionando")
    yield
    print("Aplicacion apagada correctamente")

app = FastAPI(lifespan=lifespan)

app.include_router(bus.router)
app.include_router(endpoints.router)