
from pydantic import BaseModel, Field


class ItemCheckoutSchema(BaseModel):
    id_medicamento: int
    quantidade: int = Field(gt=0)


class CheckoutSchema(BaseModel):
    id_farmacia: int
    endereco_entrega: str = Field(min_length=5)
    itens: list[ItemCheckoutSchema] = Field(min_length=1)
