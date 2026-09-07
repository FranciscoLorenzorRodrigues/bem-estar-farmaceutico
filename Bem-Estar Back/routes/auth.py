from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/login")
async def login():
    return{
        "mensagem": "Login efetuado com sucesso"
    }