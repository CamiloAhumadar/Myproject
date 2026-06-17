from contextlib import contextmanager, asynccontextmanager
from fastapi import FastAPI
from config.database import Base, engine
from controller import auth_controller, task_controller 

from controller.auth_controller import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield

app = FastAPI(
    title="My task proyect",
    version="0.1",
    lifespan=lifespan
)

app.include_router(auth_router)

app.include_router(task_controller.router)

@app.get("/")
async def welcome():
    return {"mensaje": "¡Bienvenido a mi primera API con FastAPI!"}   


