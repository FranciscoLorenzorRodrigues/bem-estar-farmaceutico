
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from database.database import get_session
from database.models import Cliente
from schemas.customer import CustomerSchema, LoginSchema

from services.security import (hash_password,verify_password,criar_token,validar_token)

auth_router = APIRouter(prefix="/auth",tags=["auth"])
seguranca = HTTPBearer()

@auth_router.post("/register")
async def register(customer_schema: CustomerSchema,session: Session = Depends(get_session)):

    cliente_email = session.query(Cliente).filter(Cliente.email == customer_schema.email).first()

    if cliente_email:
        raise HTTPException(status_code=400,detail="E-mail já cadastrado")

    cliente_cpf = session.query(Cliente).filter(Cliente.cpf == customer_schema.cpf).first()

    if cliente_cpf:
        raise HTTPException(status_code=400,detail="CPF já cadastrado")

    senha_criptografada = hash_password(customer_schema.senha)

    novo_cliente = Cliente(
        nome=customer_schema.nome,
        cpf=customer_schema.cpf,
        telefone=customer_schema.telefone,
        email=customer_schema.email,
        senha_hash=senha_criptografada,
        endereco=customer_schema.endereco
    )

    session.add(novo_cliente)
    session.commit()

    return {
        "mensagem": (
            f"Cliente cadastrado com sucesso: "
            f"{customer_schema.email}"
        )
    }


@auth_router.post("/login")
async def login(login_schema: LoginSchema,session: Session = Depends(get_session)):

    cliente = session.query(Cliente).filter(Cliente.email == login_schema.email).first()

    if not cliente:
        raise HTTPException(status_code=401,detail="E-mail ou senha incorretos")

    senha_correta = verify_password(login_schema.senha,cliente.senha_hash)

    if not senha_correta:
        raise HTTPException(status_code=401,detail="E-mail ou senha incorretos")

   
    token = criar_token(cliente.id_cliente)

    return {
        "mensagem": "Login efetuado com sucesso",
        "access_token": token,
        "token_type": "bearer"
    }


@auth_router.get("/me")
async def obter_usuario(
    credenciais: HTTPAuthorizationCredentials = Depends(seguranca)
):
    token = credenciais.credentials

    id_cliente = validar_token(token)

    if id_cliente is None:
        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado"
        )

    return {
        "mensagem": "Usuário autenticado",
        "id_cliente": id_cliente
    }

