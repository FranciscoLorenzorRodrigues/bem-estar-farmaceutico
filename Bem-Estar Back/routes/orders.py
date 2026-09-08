from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_session
from database.models import Pedido
from schemas.order import OrderSchema


orders_router = APIRouter(prefix="/orders",tags=["orders"])


@orders_router.post("/")
async def criar_pedido(pedido_schema: OrderSchema,session: Session = Depends(get_session)):

    novo_pedido = Pedido(
        id_cliente=pedido_schema.id_cliente,
        id_farmacia=pedido_schema.id_farmacia,
        data_hora_pedido=pedido_schema.data_hora_pedido,
        status_pedido=pedido_schema.status_pedido,
        valor_total=pedido_schema.valor_total,
        endereco_entrega=pedido_schema.endereco_entrega
    )

    session.add(novo_pedido)
    session.commit()

    return {"mensagem": "Pedido criado com sucesso"}

@orders_router.get("/")
async def listar_pedidos(
    session: Session = Depends(get_session)):

    pedidos = session.query(Pedido).all()

    return pedidos

@orders_router.get("/{id_pedido}")
async def buscar_pedido(
    id_pedido: int,
    session: Session = Depends(get_session)):

    pedido = session.query(Pedido).filter(Pedido.id_pedido == id_pedido).first()

    if not pedido:
        return {"mensagem": "Pedido não encontrado"}

    return pedido

@orders_router.put("/{id_pedido}")
async def atualizar_pedido(id_pedido: int,pedido_schema: OrderSchema,session: Session = Depends(get_session)):

    pedido = session.query(Pedido).filter( Pedido.id_pedido == id_pedido).first()

    if not pedido:
        return {"mensagem": "Pedido não encontrado" }

    pedido.id_cliente = pedido_schema.id_cliente
    pedido.id_farmacia = pedido_schema.id_farmacia
    pedido.data_hora_pedido = pedido_schema.data_hora_pedido
    pedido.status_pedido = pedido_schema.status_pedido
    pedido.valor_total = pedido_schema.valor_total
    pedido.endereco_entrega = pedido_schema.endereco_entrega

    session.commit()

    return { "mensagem": "Pedido atualizado com sucesso"}

@orders_router.delete("/{id_pedido}")
async def deletar_pedido(id_pedido: int,session: Session = Depends(get_session)):

    pedido = session.query(Pedido).filter(
        Pedido.id_pedido == id_pedido).first()

    if not pedido:
        return {"mensagem": "Pedido não encontrado"}

    session.delete(pedido)
    session.commit()

    return {"mensagem": "Pedido deletado com sucesso"}