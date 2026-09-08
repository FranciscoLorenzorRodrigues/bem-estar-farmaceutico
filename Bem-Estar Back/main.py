from fastapi import FastAPI

app = FastAPI()

from routes.auth import auth_router
from routes.medicines import medicines_router
from routes.pharmacies import pharmacies_router
from routes.orders import orders_router
from routes.order_medicines import order_medicines_router

app.include_router(auth_router)
app.include_router(medicines_router)
app.include_router(pharmacies_router)
app.include_router(orders_router)
app.include_router(order_medicines_router)


from database.database import Base, engine
from database import models


Base.metadata.create_all(bind=engine)