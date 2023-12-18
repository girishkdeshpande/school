# This file contains basic configuration of database, dependancy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import re
import os
from dotenv import load_dotenv
import logging
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


# Database setting configuration
class Settings:
    PROJECT_NAME = "School Management System"
    PROJECT_VERSION = "1.0.0"

    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)
    POSTGRES_DB = os.getenv("POSTGRES_DB", "school")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"


settings = Settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


# Dependancy
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# Special string for checking special characters in string
special_str = re.compile('[@_!#$%^&*()<>?\/}|{~:]')


# Logger configuration
def log_config():
    logger = logging.getLogger('school')
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler('D:\school\logs\school.log', mode='w')
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger
