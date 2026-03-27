from sqlalchemy import Column, Integer, String, Float, Boolean,DateTime
from database.db import Base
from datetime import datetime


class Kanji(Base):
    __tablename__ = "kanji"

    id = Column(Integer, primary_key=True)
    caracter = Column(String, unique=True, nullable=False)
    significado = Column(String, nullable=False)
    pista=Column(String, nullable=False)
    historia = Column(String, nullable=True)

    nivel = Column(Integer, nullable=False)
    modulo = Column(Integer, nullable=False)
    orden_en_modulo = Column(Integer, nullable=False)
    orden_global = Column(Integer, nullable=False, unique=True)

    visto = Column(Boolean, default=False)
    
    ultima_vez = Column(DateTime, default=datetime.utcnow)
    intervalo = Column(Float, default=0)  # en días
    facilidad = Column(Float, default=2.5)  # tipo Anki (ease factor)
    repeticiones = Column(Integer, default=0)

    def __repr__(self):
        return f"<Kanji {self.caracter} - {self.significado}>"