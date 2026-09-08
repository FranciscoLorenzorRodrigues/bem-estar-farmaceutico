from pydantic import BaseModel
from datetime import time


class PharmacySchema(BaseModel):

    nome: str
    cnpj: str
    endereco: str
    telefone: str
    email: str
    horario_abertura: time
    horario_fechamento: time