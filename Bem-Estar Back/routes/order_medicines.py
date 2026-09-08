from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_session
from database.models import PedidoMedicamento, Pedido
from schemas.order_medicine import OrderMedicineSchema


order_medicines_router = APIRouter(
    prefix="/order-medicines",
    tags=["order-medicines"]
)

@order_medicines_router.post("/")
async def adicionar_medicamento_pedido(pedido_medicamento_schema: OrderMedicineSchema,session: Session = Depends(get_session)):

    novo_pedido_medicamento = PedidoMedicamento(
        id_pedido=pedido_medicamento_schema.id_pedido,
        id_medicamento=pedido_medicamento_schema.id_medicamento,
        quantidade=pedido_medicamento_schema.quantidade,
        preco_unitario=pedido_medicamento_schema.preco_unitario
    )

    session.add(novo_pedido_medicamento)
    session.commit()

    medicamentos_pedido = session.query(PedidoMedicamento).filter(PedidoMedicamento.id_pedido == pedido_medicamento_schema.id_pedido).all()

    valor_total = sum(
    item.quantidade * item.preco_unitario
    for item in medicamentos_pedido
)
    pedido = session.query(Pedido).filter(Pedido.id_pedido == pedido_medicamento_schema.id_pedido).first()

    if pedido:
        pedido.valor_total = valor_total
        session.commit()

    return {
        "mensagem": "Medicamento adicionado ao pedido com sucesso",
        "valor_total": valor_total
    }

@order_medicines_router.get("/pedido/{id_pedido}")
async def listar_medicamentos_do_pedido(id_pedido: int,session: Session = Depends(get_session)):

    medicamentos_pedido = session.query(PedidoMedicamento).filter(PedidoMedicamento.id_pedido == id_pedido).all()

    return medicamentos_pedido