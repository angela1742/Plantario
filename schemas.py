
from datetime import date
from pydantic import BaseModel, Field, field_validator


class PlantaCreate(BaseModel):
    nome: str
    especie: str
    data_plantio: date
    local: str


class RegistroCrescimentoCreate(BaseModel):
    data_registro: date
    altura: int | None = Field(default=None, ge=0)
    descricao: str
    planta_id: int

    @field_validator("data_registro")
    @classmethod
    def validar_data_registro(cls, valor):
        if valor > date.today():
            raise ValueError(
                "A data do registro não pode estar no futuro."
            )
        return valor


class RegistroCrescimentoAtualizar(BaseModel):
    data_registro: date
    altura: int | None = Field(default=None, ge=0)
    descricao: str

    @field_validator("data_registro")
    @classmethod
    def validar_data_registro(cls, valor):
        if valor > date.today():
            raise ValueError(
                "A data do registro não pode estar no futuro."
            )
        return valor
