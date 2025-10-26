from __future__ import annotations
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class LinkRuPa(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    id_ruta: int = Field(foreign_key="rutas.id")
    id_parada: int = Field(foreign_key="paradasbus.id")

class Rutas(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True, nullable=False)
    origen: str
    destino: str
    duracion_estimada_horas: int

    paradas: List["ParadasBus"] = Relationship(back_populates="rutas", link_model=LinkRuPa)
    bus: Optional["Bus"] = Relationship(back_populates="ruta")


class ParadasBus(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True, nullable=False)
    direccion: str
    departamento: str
    pueblo_ciudad: str
    tiempo_en_horas: int

    rutas: List[Rutas] = Relationship(back_populates="paradas", link_model=LinkRuPa)


class Bus(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    placa: str = Field(index=True, unique=True)
    modelo: str
    capacidad: int
    estado: str = Field(default="activo")

    id_ruta: Optional[int] = Field(default=None, foreign_key="rutas.id", unique=True)
    ruta: Optional[Rutas] = Relationship(back_populates="bus")


class BusesEliminados(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    placa: str = Field(index=True, unique=True)
    modelo: str
    capacidad: int
    estado: Optional[str] = Field(default="dañado")
    ultima_ruta: Optional[str] = None
    ultimo_destino: Optional[str] = None