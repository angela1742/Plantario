from sqlalchemy import Column, Integer, String, Date
from database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

class Planta(Base):
    __tablename__ = "Plantas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    especie = Column(String, nullable=False)
    data_plantio = Column(Date, nullable=False)
    local = Column(String, nullable=False)
    
class RegistroCrescimento(Base):
    __tablename__ = "Registro_Crescimento"

    id_registro = Column(Integer, primary_key=True, index=True)
    data_registro = Column(Date, nullable=False)
    altura = Column(Integer, nullable=True)
    descricao = Column(String, nullable=False)

    planta_id = Column(
        Integer,
        ForeignKey("Plantas.id"),
        primary_key=True
    )

    planta = relationship("Planta", backref=backref("registros", cascade="all, delete-orphan"))

