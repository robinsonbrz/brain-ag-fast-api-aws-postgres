import pytest
from sqlalchemy.orm import Session

from brain_app.models.models import Cultura, Fazenda, Produtor
from brain_app.repositories.cultura_repository import CulturaRepository
from brain_app.schemas.cultura_schema import CulturaCreateSchema
from tests.utils.payloads import cultura_payload, fazenda_payload, produtor_payload


@pytest.fixture
def produtor(db_session: Session) -> Produtor:
    produtor = Produtor(**produtor_payload())
    db_session.add(produtor)
    db_session.commit()
    return produtor


@pytest.fixture
def fazenda(db_session: Session, produtor: Produtor) -> Fazenda:
    fazenda = Fazenda(**fazenda_payload(produtor.id))
    db_session.add(fazenda)
    db_session.commit()
    return fazenda


@pytest.fixture(autouse=True)
def cleanup(db_session: Session):
    yield
    db_session.query(Cultura).delete()
    db_session.query(Fazenda).delete()
    db_session.query(Produtor).delete()
    db_session.commit()


class TestCulturaRepository:

    def test_create_cultura_success(self, db_session: Session, fazenda: Fazenda):
        repo = CulturaRepository(db_session)
        cultura_data = CulturaCreateSchema(**cultura_payload(fazenda.id))
        result = repo.create(cultura_data)

        assert result.id is not None
        assert result.nome_cultura == cultura_data.nome_cultura
        assert result.ano_safra == cultura_data.ano_safra
        assert result.area_plantada == cultura_data.area_plantada

        db_cultura = db_session.query(Cultura).filter_by(id=result.id).first()
        assert db_cultura is not None
        assert db_cultura.nome_cultura == cultura_data.nome_cultura
        assert db_cultura.area_plantada == cultura_data.area_plantada

    def test_create_cultura_fazenda_nao_encontrada(self, db_session: Session):
        repo = CulturaRepository(db_session)
        cultura_data = CulturaCreateSchema(**cultura_payload(999))
        with pytest.raises(ValueError, match="Fazenda não encontrada"):
            repo.create(cultura_data)
