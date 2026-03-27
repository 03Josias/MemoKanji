from sqlalchemy import Column, Integer, String, ForeignKey
from database.db import Base


class Radical(Base):
    __tablename__ = "radical"

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    simbolo = Column(String, nullable=False)
    explicacion = Column(String, nullable=False)

    orden = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Radical {self.nombre}>"
