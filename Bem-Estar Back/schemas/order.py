from pydantic import BaseModel
from datetime import datetime


class OrderSchema(BaseModel):

    id_cliente: int
    id_farmacia: int
    data_hora_pedido: datetime
    status_pedido: str
    valor_total: float
    endereco_entrega: str