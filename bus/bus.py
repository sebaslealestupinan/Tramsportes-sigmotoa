from fastapi import APIRouter
from typing import List

from modelos import Bus
from .schemas import CrearBus, ActualizarBus
from . import crud

router = APIRouter(prefix="/bus", tags=["bus"])

#Crear un nuevo bus
@router.post("/crear", response_model=Bus)
async def crear_bus_endpoint(data: CrearBus):
    return crud.crear_bus(data)

#Obtener todos los buses
@router.get("/ver_buses", response_model=List[Bus])
async def obtener_buses_endpoint():
    return crud.obtener_buses()

#Listar buses activos
@router.get("/activos", response_model=List[Bus])
async def obtener_activos_endpoint():
    return crud.obtener_activos()

#Listar buses dañados
@router.get("/dañados", response_model=List[Bus])
async def obtener_danados_endpoint():
    return crud.obtener_danados()

#Buscar por destino
@router.get("/destino/{destino}", response_model=List[Bus])
async def buscar_por_destino_endpoint(destino: str):
    return crud.buscar_por_destino(destino)

#Buscar un bus por placa
@router.get("/buscar/{placa}", response_model=Bus)
async def buscar_por_placa_endpoint(placa: str):
    return crud.buscar_por_placa(placa)

#Actualizar un bus por placa
@router.put("/editar_datos/{placa}", response_model=Bus)
async def actualizar_bus_endpoint(placa: str, edit: ActualizarBus):
    return crud.actualizar_bus(placa, edit)

# Conteo de buses por estado
@router.get("/conteo_estados")
async def conteo_buses_endpoint():
    return crud.conteo_buses()

#Eliminar un bus por placa
@router.delete("/placa/{placa}")
async def eliminar_bus_endpoint(placa: str):
    return crud.eliminar_bus(placa)

#Listar los buses que han salido de circulacion
@router.get("/ver_buses_eliminados")
async def ver_buses_eliminados_endpoint():
    return crud.ver_buses_eliminados()