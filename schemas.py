
from datetime import date
from pydantic import BaseModel, Field, field_validator


class PlantaCreate(BaseModel):
    nome: str
    especie: str
    data_plantio: date
    local: str

    @field_validator("nome", "especie", "local")
    @classmethod
    def validar_textos_obrigatorios(cls, valor):
        if not valor.strip():
            raise ValueError(
                "Este campo não pode estar vazio."
            )
        return valor

    @field_validator("data_plantio")
    @classmethod
    def validar_data_plantio(cls, valor):
        if valor > date.today():
            raise ValueError("A data de plantio não pode estar no futuro.")
        return valor


class RegistroCrescimentoCreate(BaseModel):
    data_registro: date
    altura: int | None = Field(default=None, ge=0)
    descricao: str
    planta_id: int

    @field_validator("descricao")
    @classmethod
    def validar_descricao(cls, valor):
        if not valor.strip():
           raise ValueError(
            "A descrição não pode estar vazia."
           )
        return valor

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

    @field_validator("descricao")
    @classmethod
    def validar_descricao(cls, valor):
        if not valor.strip():
             raise ValueError(
            "A descrição não pode estar vazia."
           )
        return valor

    @field_validator("data_registro")
    @classmethod
    def validar_data_registro(cls, valor):
        if valor > date.today():
            raise ValueError(
                "A data do registro não pode estar no futuro."
            )
        return valor
