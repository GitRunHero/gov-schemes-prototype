from sqlmodel import SQLModel, create_engine, Session
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data.db")
_engine = None

def get_engine(database_url: str = None):
    global _engine
    if _engine:
        return _engine
    if database_url is None:
        database_url = DATABASE_URL
    _engine = create_engine(database_url, echo=False)
    return _engine

def create_db_and_tables(engine=None):
    if engine is None:
        engine = get_engine()
    SQLModel.metadata.create_all(engine)

def get_session():
    engine = get_engine()
    return Session(engine)
