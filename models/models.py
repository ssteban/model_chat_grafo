from pydantic import BaseModel, Field

class data_chat(BaseModel):
    trastorno: str
    resultado: str
    probabilidad: float
    edad: int
    genero: str

class data_chat_general(BaseModel):
    pregunta: str = Field(..., min_length=1, max_length=1000)

class data_resumen_caso(BaseModel):
    nombre_estudiante: str = Field(..., min_length=1, max_length=255)
    edad: int = Field(..., ge=0, le=120)
    genero: str
    nombre_prueba: str
    resultado_modelo: str
    probabilidad: float = Field(..., ge=0, le=1)