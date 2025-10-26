from sqlmodel import SQLModel
from typing import Optional

#Crear Bus
class CrearBus(SQLModel):
    placa: str
    modelo: str
    capacidad: int
    estado: str = "activo"
    ruta: str

#Actualizar Bus
class ActualizarBus(SQLModel):
    modelo: Optional[str] = None
    capacidad: Optional[int] = None
    estado: Optional[str] = None
    ruta: Optional[str] = None

# Buses eliminados
class MoverEliminarBus(SQLModel):
    placa: str
    modelo: str
    capacidad: int
    estado: Optional[str] = "dañado"
    ultima_ruta: str | None = "desconocida"
    ultimo_destino: str | None = "desconocido"
