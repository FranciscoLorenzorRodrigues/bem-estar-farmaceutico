from pydantic import BaseModel, EmailStr


class CustomerSchema(BaseModel):
    nome: str
    cpf: str
    telefone: str
    email: EmailStr
    senha: str
    endereco: str

class LoginSchema(BaseModel):
    email: EmailStr
    senha: str