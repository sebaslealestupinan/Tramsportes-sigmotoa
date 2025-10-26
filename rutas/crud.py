from sqlmodel import Session, select
from fastapi import HTTPException
from typing import List
from database import engine
from modelos import Rutas, ParadasBus, LinkRuPa
from .schemas import CrearRuta, CrearParadas


#CRUD RUTAS

def crear_ruta(data: CrearRuta) -> Rutas:
    with Session(engine) as session:
        ruta = session.exec(select(Rutas).where(Rutas.nome == data.nome)).first()
        if ruta:
            print("La ruta que estas tratando de crear ya existe")
        nueva_ruta = Rutas.from_orm(data)
        session.add(nueva_ruta)
        session.commit()
        session.refresh(nueva_ruta)
        return nueva_ruta


def obtener_rutas() -> List[Rutas]:
    with Session(engine) as session:
        rutas = session.exec(select(Rutas)).all()
        return rutas


def obtener_ruta_por_id(ruta_id: int) -> List[Rutas]:
    with Session(engine) as session:
        ruta = session.exec(select(Rutas).where(Rutas.ruta_id == ruta_id)).first()
        if not ruta:
            raise HTTPException(status_code=404, detail="Ruta no encontrada")
        return ruta


#CRUD PARADAS DE BUS
def crear_parada(data: CrearParadas) -> ParadasBus:
    with Session(engine) as session:
        nueva_parada = ParadasBus.from_orm(data)
        session.add(nueva_parada)
        session.commit()
        session.refresh(nueva_parada)
        return nueva_parada


def obtener_paradas() -> List[ParadasBus]:
    with Session(engine) as session:
        paradas = session.exec(select(ParadasBus)).all()
        return paradas


def obtener_parada_por_id(parada_id: int) -> ParadasBus:
    with Session(engine) as session:
        parada = session.get(ParadasBus, parada_id)
        if not parada:
            raise HTTPException(status_code=404, detail="Parada no encontrada")
        return parada


#RELACIÓN RUTAS - PARADAS (N:M)

def agregar_parada_a_ruta(data: CrearParadas) -> ParadasBus:
    with Session(engine) as session:
        # Verificar existencia de ruta y parada
        ruta = session.get(Rutas, data.id_ruta)
        parada = session.get(ParadasBus, data.id_parada)

        if not ruta or not parada:
            raise HTTPException(status_code=404, detail="Ruta o parada no encontrada")

        # Crear vínculo en la tabla intermedia
        enlace = LinkRuPa(id_ruta=data.id_ruta, id_parada=data.id_parada)
        session.add(enlace)
        session.commit()
        return {"message": f"Parada {data.id_parada} agregada a la ruta {data.id_ruta}"}


def obtener_paradas_por_ruta(ruta_id: int) -> List[ParadasBus]:
    with Session(engine) as session:
        ruta = session.get(Rutas, ruta_id)
        if not ruta:
            raise HTTPException(status_code=404, detail="Ruta no encontrada")

        session.refresh(ruta)
        return ruta.paradas