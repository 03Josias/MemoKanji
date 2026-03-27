from sqlalchemy import Column, Integer, Boolean
from database.db import Base


class ModuloProgreso(Base):
    __tablename__ = "modulo_progreso"

    id = Column(Integer, primary_key=True)
    nivel = Column(Integer, nullable=False)
    modulo = Column(Integer, nullable=False)

    desbloqueado = Column(Boolean, default=False)
    completado = Column(Boolean, default=False)

    mejor_puntaje = Column(Integer, default=0)
    estrellas = Column(Integer, default=0)

class NivelProgreso(Base):
    __tablename__ = "nivel_progreso"

    nivel = Column(Integer, primary_key=True)

    desbloqueado = Column(Boolean, default=False)
    completado = Column(Boolean, default=False)
    
    mejor_puntaje = Column(Integer, default=0)
    estrellas_examen = Column(Integer, default=0)    
    estrellas = Column(Integer, default=0)

class PracticaProgreso(Base):
    __tablename__="practica_progreso"
    id = Column(Integer, primary_key=True)
    record_maximo = Column(Integer, default=0)