from sqlmodel import SQLModel

#PARADAS del bus
class CrearParadas(SQLModel):
    nombre: str
    direccion: str
    departamento: str
    pueblo_ciudad: str
    tiempo_en_horas: int

#RUTA
class CrearRuta(SQLModel):
    nombre: str
    origen: str
    destino: str
    duracion_estimada_horas: int

#conexion Ruta Paradas
class CrearRuPa(SQLModel):
    nombre_ruta: int
    nombre_parada: int
