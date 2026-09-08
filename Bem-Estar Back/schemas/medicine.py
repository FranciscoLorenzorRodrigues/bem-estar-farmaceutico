from pydantic import BaseModel


class MedicineSchema(BaseModel):
    nome: str
    principio_ativo: str
    dosagem: str
    laboratorio: str
    preco: float
    controlado: bool = False