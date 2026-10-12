from pydantic import BaseModel, Field

class data_chat(BaseModel):
    trastorno: str
    resultado: str
    probabilidad: float
    edad: int
    genero: str

class data_chat_general(BaseModel):
    pregunta: str = Field(..., min_length=1, max_length=1000)