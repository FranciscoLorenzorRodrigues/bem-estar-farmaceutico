from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_session
from database.models import Medicamento
from schemas.medicine import MedicineSchema


medicines_router = APIRouter(prefix="/medicines",tags=["medicines"])


@medicines_router.post("/")
async def cadastrar_medicamento(medicamento_schema: MedicineSchema,session: Session = Depends(get_session)):

    novo_medicamento = Medicamento(
        nome=medicamento_schema.nome,
        principio_ativo=medicamento_schema.principio_ativo,
        dosagem=medicamento_schema.dosagem,
        laboratorio=medicamento_schema.laboratorio,
        preco=medicamento_schema.preco,
        controlado=medicamento_schema.controlado
    )

    session.add(novo_medicamento)
    session.commit()

    return {"mensagem": "Medicamento cadastrado com sucesso"}

@medicines_router.get("/")
async def listar_medicamentos( session: Session = Depends(get_session)):

    medicamentos = session.query(Medicamento).all()

    return medicamentos

@medicines_router.get("/{id_medicamento}")
async def buscar_medicamento(id_medicamento: int,session: Session = Depends(get_session)
):

    medicamento = session.query(Medicamento).filter(
        Medicamento.id_medicamento == id_medicamento).first()

    if not medicamento:
        return {
            "mensagem": "Medicamento não encontrado"
        }

    return medicamento

@medicines_router.put("/{id_medicamento}")
async def atualizar_medicamento(
    id_medicamento: int,
    medicamento_schema: MedicineSchema,
    session: Session = Depends(get_session)
):

    medicamento = session.query(Medicamento).filter( Medicamento.id_medicamento == id_medicamento).first()

    if not medicamento:
        return {"mensagem": "Medicamento não encontrado"}

    medicamento.nome = medicamento_schema.nome
    medicamento.principio_ativo = medicamento_schema.principio_ativo
    medicamento.dosagem = medicamento_schema.dosagem
    medicamento.laboratorio = medicamento_schema.laboratorio
    medicamento.preco = medicamento_schema.preco
    medicamento.controlado = medicamento_schema.controlado

    session.commit()

    return {"mensagem": "Medicamento atualizado com sucesso" }

@medicines_router.delete("/{id_medicamento}")
async def deletar_medicamento(id_medicamento: int,session: Session = Depends(get_session)):

    medicamento = session.query(Medicamento).filter( Medicamento.id_medicamento == id_medicamento).first()

    if not medicamento:
        return { "mensagem": "Medicamento não encontrado" }

    session.delete(medicamento)
    session.commit()

    return {"mensagem": "Medicamento deletado com sucesso"}
