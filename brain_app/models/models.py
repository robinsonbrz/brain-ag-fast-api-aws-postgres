from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from brain_app.core.database import Base

class Produtor(Base):
    __tablename__ = "produtores"

    id = Column(Integer, primary_key=True, index=True)
    cpf_cnpj = Column(String(20), unique=True, nullable=False)
    nome_produtor = Column(String(100), nullable=False)

    fazendas = relationship("Fazenda", back_populates="produtor")


class Fazenda(Base):
    __tablename__ = "fazendas"

    id = Column(Integer, primary_key=True, index=True)
    produtor_id = Column(Integer, ForeignKey("produtores.id"), nullable=False)
    nome_fazenda = Column(String(100), nullable=False)
    cidade = Column(String(100), nullable=False)
    estado = Column(String(2), nullable=False)
    area_total = Column(Numeric(precision=12, scale=2), nullable=False)
    area_agricultavel = Column(Numeric(precision=12, scale=2), nullable=False)
    area_vegetacao = Column(Numeric(precision=12, scale=2), nullable=False)

    produtor = relationship("Produtor", back_populates="fazendas")
    culturas = relationship("Cultura", back_populates="fazenda")  # Alterado de plantios para culturas


class Cultura(Base):
    __tablename__ = "culturas"

    id = Column(Integer, primary_key=True, index=True)
    fazenda_id = Column(Integer, ForeignKey("fazendas.id"), nullable=False)
    area_plantada = Column(Numeric(precision=12, scale=2), nullable=False)
    ano_safra = Column(Integer, nullable=False)
    nome_cultura = Column(String(100), nullable=False)

    fazenda = relationship("Fazenda", back_populates="culturas")

    __table_args__ = (
        UniqueConstraint('nome_cultura', 'ano_safra', 'fazenda_id', name='_culturas_ano_fazenda_uc'),
    )
