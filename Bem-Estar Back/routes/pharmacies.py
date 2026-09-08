from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_session
from database.models import Farmacia
from schemas.pharmacy import PharmacySchema


pharmacies_router = APIRouter( prefix="/pharmacies",tags=["pharmacies"])


@pharmacies_router.post("/")
async def cadastrar_farmacia(farmacia_schema: PharmacySchema,session: Session = Depends(get_session)):

    nova_farmacia = Farmacia(
        nome=farmacia_schema.nome,
        cnpj=farmacia_schema.cnpj,
        endereco=farmacia_schema.endereco,
        telefone=farmacia_schema.telefone,
        email=farmacia_schema.email,
        horario_abertura=farmacia_schema.horario_abertura,
        horario_fechamento=farmacia_schema.horario_fechamento
    )

    session.add(nova_farmacia)
    session.commit()

    return { "mensagem": "Farmácia cadastrada com sucesso" }

@pharmacies_router.get("/")
async def listar_farmacias(
    session: Session = Depends(get_session)):

    farmacias = session.query(Farmacia).all()

    return farmacias

@pharmacies_router.get("/{id_farmacia}")
async def buscar_farmacia(
    id_farmacia: int,
    session: Session = Depends(get_session)):

    farmacia = session.query(Farmacia).filter( Farmacia.id_farmacia == id_farmacia).first()

    if not farmacia:
        return {"mensagem": "Farmácia não encontrada"}

    return farmacia

@pharmacies_router.put("/{id_farmacia}")
async def atualizar_farmacia(id_farmacia: int,farmacia_schema: PharmacySchema,session: Session = Depends(get_session)):

    farmacia = session.query(Farmacia).filter(Farmacia.id_farmacia == id_farmacia).first()

    if not farmacia:
        return { "mensagem": "Farmácia não encontrada"}

    farmacia.nome = farmacia_schema.nome
    farmacia.cnpj = farmacia_schema.cnpj
    farmacia.endereco = farmacia_schema.endereco
    farmacia.telefone = farmacia_schema.telefone
    farmacia.email = farmacia_schema.email
    farmacia.horario_abertura = farmacia_schema.horario_abertura
    farmacia.horario_fechamento = farmacia_schema.horario_fechamento

    session.commit()

    return {"mensagem": "Farmácia atualizada com sucesso" }

@pharmacies_router.delete("/{id_farmacia}")
async def deletar_farmacia(id_farmacia: int,session: Session = Depends(get_session)):

    farmacia = session.query(Farmacia).filter(
        Farmacia.id_farmacia == id_farmacia
    ).first()

    if not farmacia:
        return { "mensagem": "Farmácia não encontrada" }

    session.delete(farmacia)
    session.commit()

    return {"mensagem": "Farmácia deletada com sucesso"}