from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import router

from app.database.db import init_db

from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI(title="CRM_study")


# Инициализация базы данных
init_db(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

