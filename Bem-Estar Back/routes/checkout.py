
from datetime import datetime, timezone
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from database.database import get_session
from database.models import (
    Cliente,
    Farmacia,
    Medicamento,
    Estoque,
    Pedido,
    PedidoMedicamento
)
from schemas.checkout import CheckoutSchema
from services.security import validar_token


checkout_router = APIRouter(
    prefix="/checkout",
    tags=["checkout"]
)

seguranca = HTTPBearer()


@checkout_router.post("/")
def finalizar_compra(
    dados: CheckoutSchema,
    credenciais: HTTPAuthorizationCredentials = Depends(seguranca),
    session: Session = Depends(get_session)
):
    id_cliente = validar_token(credenciais.credentials)

    if id_cliente is None:
        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado"
        )

    try:
        cliente = session.get(Cliente, id_cliente)
        farmacia = session.get(Farmacia, dados.id_farmacia)

        if not cliente or not farmacia:
            raise HTTPException(
                status_code=404,
                detail="Cliente ou farmácia não encontrado"
            )

        quantidades = {}

        for item in dados.itens:
            quantidades[item.id_medicamento] = (
                quantidades.get(item.id_medicamento, 0)
                + item.quantidade
            )

        total = Decimal("0.00")
        itens_pedido = []

        for id_medicamento, quantidade in sorted(quantidades.items()):
            medicamento = session.get(
                Medicamento,
                id_medicamento
            )

            if not medicamento:
                raise HTTPException(
                    status_code=404,
                    detail=f"Medicamento {id_medicamento} não encontrado"
                )

            if medicamento.controlado:
                raise HTTPException(
                    status_code=400,
                    detail="Medicamento controlado exige validação de receita"
                )

            lotes = (
                session.query(Estoque)
                .filter(
                    Estoque.id_farmacia == dados.id_farmacia,
                    Estoque.id_medicamento == id_medicamento,
                    Estoque.estoque > 0,
                    Estoque.data_validade >= datetime.now(timezone.utc).date()
                )
                .order_by(
                    Estoque.data_validade,
                    Estoque.id_estoque
                )
                .with_for_update()
                .all()
            )

            disponivel = sum(lote.estoque for lote in lotes)

            if disponivel < quantidade:
                raise HTTPException(
                    status_code=400,
                    detail=f"Estoque insuficiente para {medicamento.nome}"
                )

            restante = quantidade

            for lote in lotes:
                retirar = min(lote.estoque, restante)
                lote.estoque -= retirar
                restante -= retirar

                if restante == 0:
                    break

            preco = medicamento.preco
            total += preco * quantidade

            itens_pedido.append({
                "id_medicamento": id_medicamento,
                "quantidade": quantidade,
                "preco_unitario": preco
            })

        pedido = Pedido(
            id_cliente=id_cliente,
            id_farmacia=dados.id_farmacia,
            status_pedido="Pendente",
            valor_total=total,
            endereco_entrega=dados.endereco_entrega
        )

        session.add(pedido)
        session.flush()

        for item in itens_pedido:
            session.add(
                PedidoMedicamento(
                    id_pedido=pedido.id_pedido,
                    **item
                )
            )

        session.commit()

        return {
            "mensagem": "Pedido criado com sucesso",
            "id_pedido": pedido.id_pedido,
            "valor_total": float(total)
        }

    except HTTPException:
        session.rollback()
        raise

    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail="Erro ao finalizar pedido"
        )
