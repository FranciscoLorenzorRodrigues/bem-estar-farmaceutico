
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.database import Base, engine
from database import models

from routes.auth import auth_router
from routes.medicines import medicines_router
from routes.pharmacies import pharmacies_router
from routes.orders import orders_router
from routes.order_medicines import order_medicines_router
from routes.checkout import checkout_router

app = FastAPI(title="Bem-Estar Farmacêutico API")

# Permitir comunicação com o frontend local
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ "http://127.0.0.1:5500", "http://localhost:5500",],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(auth_router)
app.include_router(medicines_router)
app.include_router(pharmacies_router)
app.include_router(orders_router)
app.include_router(order_medicines_router)
app.include_router(checkout_router)

Base.metadata.create_all(bind=engine)
