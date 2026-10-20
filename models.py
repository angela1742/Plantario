from sqlalchemy import Column, Integer, String, Date
from database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Planta(Base):
    __tablename__ = "Plantas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    especie = Column(String, nullable=False)
    data_plantio = Column(Date, nullable=False)
    local = Column(String, nullable=False)
    

class RegistroCrescimento(Base):
    __tablename__ = "Registro_Crescimento"

    id = Column(Integer, primary_key=True, index=True)
    data_registro = Column(Date, nullable=False)
    altura = Column(Integer, nullable=True)
    descricao = Column(String, nullable=False)

    planta_id = Column(Integer, ForeignKey("Plantas.id"), nullable=False)
    planta = relationship("Planta", backref="registros")
