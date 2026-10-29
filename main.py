from fastapi import FastAPI, Depends, HTTPException, status, Query
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


@app.post("/plantas", status_code=status.HTTP_201_CREATED)
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
def listar_plantas(
    Busca_Geral: str | None = Query(
        default=None,
        description="nome, especie ou local."
    ),
    Por_Especie: str | None = Query(
        default=None,
        description="especie específica."
    ),
    Ordenar_Por: str = Query(
        default="nome",
        description="id, nome, especie, data_plantio ou local."
    ),
    Ordem: str = Query(
        default="Crescente",
        description="ordenar: Crescente ou Decrescente."
    ),
    Pagina_Consulta: int = Query(default=1, ge=1,
        description="Escolha a pagina de consulta"),
    Limite_de_plantas: int = Query(default=10, ge=1, le=100,
        description="Escolha o limite de plantas, mínimo: 1, máximo: 100, padrão: 10"),
    banco: Session = Depends(obter_banco)
):
    consulta = banco.query(models.Planta)

    if Busca_Geral:
        termo = f"%{Busca_Geral.strip()}%"
        consulta = consulta.filter(
            models.Planta.nome.ilike(termo)
            | models.Planta.especie.ilike(termo)
            | models.Planta.local.ilike(termo)
        )

    if Por_Especie:
        consulta = consulta.filter(
            models.Planta.especie.ilike(Por_Especie.strip())
        )

    campos = {
        "id": models.Planta.id,
        "nome": models.Planta.nome,
        "especie": models.Planta.especie,
        "data_plantio": models.Planta.data_plantio,
        "local": models.Planta.local
    }

    if Ordenar_Por not in campos:
        raise HTTPException(
            status_code=400,
            detail="Campo de ordenação inválido."
        )

    if Ordem not in ("Crescente", "Decrescente"):
        raise HTTPException(
            status_code=400,
            detail="A ordem deve ser Crescente ou Decrescente."
        )

    campo = campos[Ordenar_Por]

    if Ordem == "Decrescente":
        consulta = consulta.order_by(campo.desc())
    else:
        consulta = consulta.order_by(campo.asc())

    total = consulta.count()

    deslocamento = (Pagina_Consulta - 1) * Limite_de_plantas

    plantas = consulta.offset(deslocamento).limit(
        Limite_de_plantas
    ).all()

    return {
        "total": total,
        "pagina": Pagina_Consulta,
        "limite": Limite_de_plantas,
        "total_paginas": (
            total + Limite_de_plantas - 1
        ) // Limite_de_plantas,
        "plantas": plantas
    }

@app.get("/plantas/{planta_id}")
def buscar_planta(
    planta_id: int,
    banco: Session = Depends(obter_banco)
):
    planta = banco.query(models.Planta).filter(
        models.Planta.id == planta_id
    ).first()

    if planta is None:
        raise HTTPException(
        status_code=404,
        detail="Planta não encontrada."
    )

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


@app.post("/plantas/{planta_id}/registros",status_code=status.HTTP_201_CREATED)
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
            detail="Planta não encontrada."
        )

    if dados.data_registro < planta.data_plantio:
        raise HTTPException(
        status_code=400,
        detail="A data do registro não pode ser anterior à data de plantio da planta."
    )

    ultimo_registro = banco.query(
        models.RegistroCrescimento
    ).filter(
        models.RegistroCrescimento.planta_id == planta_id
    ).order_by(
        models.RegistroCrescimento.id_registro.desc()
    ).first()

    if ultimo_registro is None:
        proximo_id = 1
    else:
        proximo_id = ultimo_registro.id_registro + 1

    novo_registro = models.RegistroCrescimento(
        id_registro=proximo_id,
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
        "id_registro": novo_registro.id_registro,
        "data_registro": novo_registro.data_registro,
        "altura": novo_registro.altura,
        "descricao": novo_registro.descricao,
        "planta_id": novo_registro.planta_id
    }



@app.get("/plantas/{planta_id}/registros/{registro_id}")
def buscar_registro(
    planta_id: int,
    registro_id: int,
    banco: Session = Depends(obter_banco)
):
    planta = banco.query(models.Planta).filter(
        models.Planta.id == planta_id
    ).first()

    if planta is None:
        raise HTTPException(
            status_code=404,
            detail="Planta não encontrada."
        )

    registro = banco.query(
        models.RegistroCrescimento
    ).filter(
        models.RegistroCrescimento.id_registro == registro_id,
        models.RegistroCrescimento.planta_id == planta_id
    ).first()

    if registro is None:
        raise HTTPException(
            status_code=404,
            detail="Registro não encontrado para esta planta."
        )

    return registro


@app.get("/plantas/{planta_id}/registros")
def listar_registros(
    planta_id: int,
    banco: Session = Depends(obter_banco)
):
    planta = banco.query(models.Planta).filter(
        models.Planta.id == planta_id
    ).first()

    if planta is None:
        raise HTTPException(
            status_code=404,
            detail="Planta não encontrada."
        )

    registros = banco.query(
        models.RegistroCrescimento
    ).filter(
        models.RegistroCrescimento.planta_id == planta_id
    ).all()

    return registros


@app.put("/plantas/{planta_id}/registros/{registro_id}")
def atualizar_registro(
    planta_id: int,
    registro_id: int,
    dados: schemas.RegistroCrescimentoAtualizar,
    banco: Session = Depends(obter_banco)
):
    planta = banco.query(models.Planta).filter(
        models.Planta.id == planta_id
    ).first()

    if planta is None:
        raise HTTPException(
            status_code=404,
            detail="Planta não encontrada."
        )

    registro = banco.query(
        models.RegistroCrescimento
    ).filter(
        models.RegistroCrescimento.id_registro == registro_id,
        models.RegistroCrescimento.planta_id == planta_id
    ).first()

    if registro is None:
        raise HTTPException(
            status_code=404,
            detail="Registro não encontrado para esta planta."
        )

    registro.data_registro = dados.data_registro
    registro.altura = dados.altura
    registro.descricao = dados.descricao

    banco.commit()
    banco.refresh(registro)

    return {
        "mensagem": "Registro atualizado com sucesso!",
        "id_registro": registro.id_registro,
        "data_registro": registro.data_registro,
        "altura": registro.altura,
        "descricao": registro.descricao,
        "planta_id": registro.planta_id
    }



@app.delete("/plantas/{planta_id}/registros/{registro_id}")
def excluir_registro(
    planta_id: int,
    registro_id: int,
    banco: Session = Depends(obter_banco)
):
    planta = banco.query(models.Planta).filter(
        models.Planta.id == planta_id
    ).first()

    if planta is None:
        raise HTTPException(
            status_code=404,
            detail="Planta não encontrada."
        )

    registro = banco.query(
        models.RegistroCrescimento
    ).filter(
        models.RegistroCrescimento.id_registro == registro_id,
        models.RegistroCrescimento.planta_id == planta_id
    ).first()

    if registro is None:
        raise HTTPException(
            status_code=404,
            detail="Registro não encontrado para esta planta."
        )

    banco.delete(registro)
    banco.commit()

    return {
        "mensagem": "Registro excluído com sucesso!",
        "id_registro": registro_id,
        "planta_id": planta_id
    }


