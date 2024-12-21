# app/database.py
from app.configs.mongo_config import db

def get_db():
    return db