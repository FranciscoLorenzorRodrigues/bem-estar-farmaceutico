
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

BASE_DIR = Path(__file__).resolve().parent.parent

# Carrega o .env e prioriza suas configurações
load_dotenv(BASE_DIR / ".env", override=True)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./bem_estar.db"
)

# Configurações específicas para SQLite
if DATABASE_URL.startswith("sqlite"):
    if DATABASE_URL.startswith("sqlite:///./"):
        nome_banco = DATABASE_URL.removeprefix("sqlite:///./")
        caminho_banco = (BASE_DIR / nome_banco).resolve()
        DATABASE_URL = f"sqlite:///{caminho_banco.as_posix()}"

    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
