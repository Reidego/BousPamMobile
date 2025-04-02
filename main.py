from fastapi import Depends, FastAPI, HTTPException, APIRouter
import os
import models
from app.terminals import terminal_router
from app.tg import tg_router
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

root = os.path.dirname(os.path.abspath(__file__))

app.include_router(tg_router)
app.include_router(terminal_router)
