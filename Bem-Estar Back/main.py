from fastapi import FastAPI

app = FastAPI()

from routes.auth import auth_router

app.include_router(auth_router)

from database.database import Base, engine
from database import models

Base.metadata.create_all(bind=engine)