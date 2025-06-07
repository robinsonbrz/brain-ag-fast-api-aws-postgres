import pytest
from sqlalchemy.orm import Session

from brain_app.models.models import Cultura, Fazenda, Produtor
from brain_app.repositories.cultura_repository import CulturaRepository
from brain_app.schemas.cultura_schema import CulturaCreateSchema


@pytest.fixture
def produtor(db_session: Session) -> Produtor:
    produtor = Produtor(
        cpf_cnpj="690.692.120-72",
        nome_produtor="Produtor Teste",
    )
    db_session.add(produtor)
    db_session.commit()
    return produtor


@pytest.fixture
def fazenda(db_session: Session, produtor: Produtor) -> Fazenda:
    fazenda = Fazenda(
        produtor_id=produtor.id,
        nome_fazenda="Fazenda Teste",
        area_total=1000.0,
        area_agricultavel=500.0,
        cidade="São Paulo",
        estado="SP",
        area_vegetacao=400.0,
    )
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
        cultura_data = CulturaCreateSchema(
            fazenda_id=fazenda.id, nome_cultura="Soja", ano_safra=2023, area_plantada=100.0
        )
        result = repo.create(cultura_data)

        assert result.id is not None
        assert result.nome_cultura == "Soja"
        assert result.ano_safra == 2023
        assert result.area_plantada == 100.0

        db_cultura = db_session.query(Cultura).filter_by(id=result.id).first()
        assert db_cultura is not None
        assert db_cultura.nome_cultura == "Soja"
        assert db_cultura.area_plantada == 100.0

    def test_create_cultura_fazenda_nao_encontrada(self, db_session: Session):
        repo = CulturaRepository(db_session)
        cultura_data = CulturaCreateSchema(
            fazenda_id=999, nome_cultura="Soja", ano_safra=2023, area_plantada=100.0
        )

        with pytest.raises(ValueError, match="Fazenda não encontrada"):
            repo.create(cultura_data)

    def test_create_method(self, db_session: Session, fazenda: Fazenda):

        repo = CulturaRepository(db_session)
        cultura_data = CulturaCreateSchema(
            fazenda_id=fazenda.id, nome_cultura="Algodão", ano_safra=2024, area_plantada=75.0
        )

        result = repo.create(cultura_data)

        assert result.id is not None
        assert db_session.query(Cultura).count() == 1

        db_cultura = db_session.query(Cultura).first()
        assert db_cultura.nome_cultura == "Algodão"
        assert db_cultura.ano_safra == 2024
