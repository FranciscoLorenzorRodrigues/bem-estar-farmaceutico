from pydantic import BaseModel


class OrderMedicineSchema(BaseModel):

    id_pedido: int
    id_medicamento: int
    quantidade: int
    preco_unitario: float