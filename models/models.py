from pydantic import BaseModel

class data_chat(BaseModel):
    trastorno: str
    resultado: str
    probabilidad: float
    edad: int
    genero: str