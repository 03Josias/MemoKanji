
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

def get_db_path():
    if getattr(sys, 'frozen', False):
        # Ejecutable PyInstaller → misma carpeta que el .exe
        base_path = os.path.dirname(sys.executable)
    else:
        # Desarrollo → carpeta raíz del proyecto
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, "MemoKanji.db")

DATABASE_URL = f"sqlite:///{get_db_path()}"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def create_tables():
    Base.metadata.create_all(engine)