from datetime import date
from pydantic import BaseModel


class PlantaCreate(BaseModel):
    nome: str
    especie: str
    data_plantio: date
    local: str

class RegistroCrescimentoCreate(BaseModel):
    data_registro: date
    altura: int | None = None
    descricao: str
    planta_id: int