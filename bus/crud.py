from typing import List, Optional
from sqlmodel import Session, select
from fastapi import HTTPException

from database import engine
from modelos import Bus, BusesEliminados
from .schemas import CrearBus, ActualizarBus
from modelos import Rutas

#Crear un nuevo bus
def crear_bus(data: CrearBus) -> Bus:
    with Session(engine) as session:
        ruta = session.get(Rutas, data.ruta)
        if not ruta:
            raise HTTPException(status_code=404, detail="Ruta asignada no existe")
        bus = Bus.model_validate(data)
        session.add(bus)
        session.commit()
        session.refresh(bus)

        return bus

#Obtener todos los buses
def obtener_buses() -> List[Bus]:
    with Session(engine) as session:
        return session.exec(select(Bus)).all()

#Obtener buses activos
def obtener_activos() -> List[Bus]:
    with Session(engine) as session:
        return session.exec(select(Bus).where(Bus.estado == "activo")).all()

#Obtener buses dañados
def obtener_dañados() -> List[Bus]:
    with Session(engine) as session:
        return session.exec(select(Bus).where(Bus.estado == "dañado")).all()


#Buscar por destino
def buscar_por_destino(destino: str) -> List[Bus]:
    with Session(engine) as session:
        return session.exec(select(Bus).where(Bus.destino == destino)).all()


#Buscar por placa
def buscar_por_placa(placa: str) -> Optional[Bus]:
    with Session(engine) as session:
        bus = session.exec(select(Bus).where(Bus.placa == placa)).first()
        if not bus:
            raise HTTPException(status_code=404, detail="Bus no encontrado")
        return bus


#Actualizar por placa
def actualizar_bus(placa: str, edit: ActualizarBus) -> Bus:
    with Session(engine) as session:
        bus = session.exec(select(Bus).where(Bus.placa == placa)).first()
        if not bus:
            raise HTTPException(status_code=404, detail="Bus no encontrado")

        update_data = edit.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(bus, key, value)

        session.add(bus)
        session.commit()
        session.refresh(bus)
        return bus

#Conteo de buses por estado
def conteo_buses() -> dict:
    with Session(engine) as session:
        total = session.exec(select(Bus)).all()
        activos = len([b for b in total if b.estado == "activo"])
        dañados = len([b for b in total if b.estado == "dañado"])
        otros = len(total) - activos - dañados
        return {
            "total_buses": len(total),
            "activos": activos,
            "dañados": dañados,
            "otros": otros
        }

#Eliminar por placa
def eliminar_bus(placa: str) -> dict:
    with Session(engine) as session:
        bus = session.exec(select(Bus).where(Bus.placa == placa)).first()
        if not bus:
            raise HTTPException(status_code=404, detail="Bus no encontrado")

        bus_eliminado = BusesEliminados(
            placa=bus.placa,
            modelo=bus.modelo,
            capacidad=bus.capacidad,
            estado=bus.estado if bus.estado else "dañado",
            ultima_ruta=bus.ruta_actual,
            ultimo_destino=bus.destino
        )
        session.add(bus_eliminado)

        session.delete(bus)
        session.commit()
        return {"message": f"El bus con placa {placa} se eliminado correctamente."}

def ver_buses_eliminados() -> list[BusesEliminados]:
    with Session(engine) as session:
        return session.exec(select(BusesEliminados)).all()