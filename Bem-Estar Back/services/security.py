
import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

if not JWT_SECRET_KEY:
    raise RuntimeError(
        "JWT_SECRET_KEY não configurada no arquivo .env"
    )

JWT_ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password
    )

def criar_token(id_cliente: int) -> str:
    expiracao = datetime.now(timezone.utc) + timedelta(
        minutes=TOKEN_EXPIRE_MINUTES
    )

    dados = {
        "sub": str(id_cliente),
        "exp": expiracao
    }

    token = jwt.encode(
        dados,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )

    return token


def validar_token(token: str) -> int | None:
    try:
        dados = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM]
        )

        return int(dados["sub"])

    except (InvalidTokenError, KeyError, ValueError, TypeError):
        return None
