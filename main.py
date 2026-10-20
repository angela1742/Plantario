from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import engine, Base, SessionLocal
import models
import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI()


def obter_banco():
    banco = SessionLocal()
    try:
        yield banco
    finally:
        banco.close()


@app.get("/")
def inicio():
    return {"mensagem": "Bem-vindo ao Plantário!"}


@app.post("/plantas")
def cadastrar_planta(
    planta: schemas.PlantaCreate,
    banco: Session = Depends(obter_banco)
):
    nova_planta = models.Planta(
        nome=planta.nome,
        especie=planta.especie,
        data_plantio=planta.data_plantio,
        local=planta.local
    )


    banco.add(nova_planta)
    banco.commit()
    banco.refresh(nova_planta)

    return {
        "mensagem": "Planta cadastrada com sucesso!",
        "id": nova_planta.id,
        "nome": nova_planta.nome,
        "especie": nova_planta.especie,
        "data_plantio": nova_planta.data_plantio,
        "local": nova_planta.local
    }


@app.get("/plantas")
def listar_plantas(banco: Session = Depends(obter_banco)):
    plantas = banco.query(models.Planta).all()

    return plantas


@app.get("/plantas/{planta_id}")
def buscar_planta(
    planta_id: int,
    banco: Session = Depends(obter_banco)
):
    planta = banco.query(models.Planta).filter(
        models.Planta.id == planta_id
    ).first()

    if planta is None:
        return {"mensagem": "Planta não encontrada."}

    return planta

@app.put("/plantas/{planta_id}")
def atualizar_planta(
    planta_id: int,
    dados: schemas.PlantaCreate,
    banco: Session = Depends(obter_banco)
):
    planta = banco.query(models.Planta).filter(
        models.Planta.id == planta_id
    ).first()

    if planta is None:
        raise HTTPException(
            status_code=404,
            detail="Planta não encontrada para a atualização."
        )

    planta.nome = dados.nome
    planta.especie = dados.especie
    planta.data_plantio = dados.data_plantio
    planta.local = dados.local

    banco.commit()
    banco.refresh(planta)

    return {
        "mensagem": "Planta atualizada com sucesso!",
        "id": planta.id,
        "nome": planta.nome,
        "especie": planta.especie,
        "data_plantio": planta.data_plantio,
        "local": planta.local
    }

@app.delete("/plantas/{planta_id}")
def excluir_planta(
    planta_id: int,
    banco: Session = Depends(obter_banco)
):
    planta = banco.query(models.Planta).filter(
        models.Planta.id == planta_id
    ).first()

    if planta is None:
        raise HTTPException(
            status_code=404,
            detail="Planta não encontrada para a exclusão."
        )

    banco.delete(planta)
    banco.commit()

    return {
        "mensagem": "Planta excluída com sucesso!"
    }

@app.post("/plantas/{planta_id}/registros")
def cadastrar_registro(
    planta_id: int,
    dados: schemas.RegistroCrescimentoCreate,
    banco: Session = Depends(obter_banco)
):
    planta = banco.query(models.Planta).filter(
        models.Planta.id == planta_id
    ).first()

    if planta is None:
        raise HTTPException(
            status_code=404,
            detail="Planta não encontrada para registro de crescimento."
        )

    novo_registro = models.RegistroCrescimento(
        data_registro=dados.data_registro,
        altura=dados.altura,
        descricao=dados.descricao,
        planta_id=planta_id
    )

    banco.add(novo_registro)
    banco.commit()
    banco.refresh(novo_registro)

    return {
        "mensagem": "Registro de crescimento cadastrado com sucesso!",
        "id": novo_registro.id,
        "data_registro": novo_registro.data_registro,
        "altura": novo_registro.altura,
        "descricao": novo_registro.descricao,
        "planta_id": novo_registro.planta_id
    }


