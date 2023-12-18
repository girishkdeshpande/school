from fastapi import FastAPI
import logging.config
from core.config import settings, log_config

from db.session import engine
from db.base import Base
from apis.base import api_router


def create_tables():
    Base.metadata.create_all(bind=engine)


def include_router(app):
    app.include_router(api_router)


def start_app():
    log_config()
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    create_tables()
    include_router(app)
    return app


app = start_app()


@app.get("/")
def hello_school():
    return {"msg": "Welcome to School"}
