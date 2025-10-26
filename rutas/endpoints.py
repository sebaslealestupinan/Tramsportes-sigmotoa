from fastapi import APIRouter
from . import crud
from .schemas import CrearRuta, CrearParadas, CrearRuPa

router = APIRouter(prefix="/rutas", tags=["rutas"])

#RUTAS
@router.post("/crear_ruta")
def crear_ruta(ruta:CrearRuta):
    return crud.crear_ruta(ruta)

@router.get("/ver_las_rutas")
def obtener_rutas():
    return crud.obtener_rutas()

@router.get("/{ruta_id}")
def obtener_ruta(ruta_id: int):
    return crud.obtener_ruta_por_id(ruta_id)

#PARADAS
@router.post("/ingresar_parada")
def crear_parada(parada: CrearParadas):
    return crud.crear_parada(parada)

@router.get("/Listar_paradas")
def obtener_paradas():
    return crud.obtener_paradas()

@router.get("/paradas/{parada_id}")
def obtener_parada(parada_id: int):
    return crud.obtener_parada_por_id(parada_id)

#RELACIÓN RUP(la relacion que existe o no entre las rutas y las diferentes paradas)
@router.post("/asignar_parada")
def asignar_parada(data: CrearRuPa):
    return crud.agregar_parada_a_ruta(data)

@router.get("/{ruta_id}/paradas")
def listar_paradas_de_ruta(ruta_id: int):
    return crud.obtener_paradas_por_ruta(ruta_id)