import pytest
from sqlalchemy.exc import IntegrityError
from brain_app.models.models import Cultura, Fazenda
from brain_app.repositories.cultura_repository import CulturaRepository
from brain_app.schemas.cultura_schema import CulturaCreateSchema

class TestCulturaRepositoryIntegration:
    @pytest.fixture
    def setup_data(self, db_session):
        """Fixture para criar dados iniciais de teste"""
        # Cria uma fazenda de teste
        fazenda = Fazenda(
            nome="Fazenda Teste",
            area_total=1000.0,
            area_agricultavel=500.0
        )
        db_session.add(fazenda)
        db_session.commit()
        
        yield fazenda 
        db_session.query(Cultura).delete()
        db_session.query(Fazenda).delete()
        db_session.commit()

    def test_create_cultura_success(self, db_session, setup_data):

        repo = CulturaRepository(db_session)
        cultura_data = CulturaCreateSchema(
            fazenda_id=setup_data.id,
            nome_cultura="Soja",
            ano_safra=2023,
            area_plantada=100.0
        )

        result = repo.create_cultura(cultura_data)

        assert result.id is not None
        assert result.nome_cultura == "Soja"
        

        db_cultura = db_session.query(Cultura).filter_by(id=result.id).first()
        assert db_cultura is not None
        assert db_cultura.area_plantada == 100.0

    # def test_create_cultura_fazenda_nao_encontrada(self, db_session):
    #     # Arrange
    #     repo = CulturaRepository(db_session)
    #     cultura_data = CulturaCreateSchema(
    #         fazenda_id=999,  # ID inexistente
    #         nome_cultura="Soja",
    #         ano_safra=2023,
    #         area_plantada=100.0
    #     )

    #     # Act & Assert
    #     with pytest.raises(ValueError, match="Fazenda não encontrada"):
    #         repo.create_cultura(cultura_data)

    # def test_create_cultura_area_excedente(self, db_session, setup_data):
    #     # Arrange
    #     repo = CulturaRepository(db_session)
        
    #     # Primeiro cria uma cultura que ocupa quase toda a área
    #     cultura_existente = Cultura(
    #         fazenda_id=setup_data.id,
    #         nome_cultura="Milho",
    #         ano_safra=2023,
    #         area_plantada=450.0
    #     )
    #     db_session.add(cultura_existente)
    #     db_session.commit()

    #     # Tenta criar outra cultura que excede o limite
    #     cultura_data = CulturaCreateSchema(
    #         fazenda_id=setup_data.id,
    #         nome_cultura="Soja",
    #         ano_safra=2023,
    #         area_plantada=100.0  # Total seria 550 > 500 (limite)
    #     )

    #     # Act & Assert
    #     with pytest.raises(ValueError) as exc_info:
    #         repo.create_cultura(cultura_data)
    #     assert "ultrapassa a área agricultável" in str(exc_info.value)

    # def test_create_cultura_duplicada(self, db_session, setup_data):
    #     # Arrange
    #     repo = CulturaRepository(db_session)
    #     cultura_data = CulturaCreateSchema(
    #         fazenda_id=setup_data.id,
    #         nome_cultura="Soja",
    #         ano_safra=2023,
    #         area_plantada=100.0
    #     )

    #     # Cria a primeira cultura (sucesso)
    #     repo.create_cultura(cultura_data)

    #     # Tenta criar a mesma cultura novamente
    #     with pytest.raises(ValueError, match="já cadastrada"):
    #         repo.create_cultura(cultura_data)

    # def test_create_method(self, db_session, setup_data):
    #     # Arrange
    #     repo = CulturaRepository(db_session)
    #     cultura_data = CulturaCreateSchema(
    #         fazenda_id=setup_data.id,
    #         nome_cultura="Algodão",
    #         ano_safra=2024,
    #         area_plantada=75.0
    #     )

    #     # Act
    #     result = repo.create(cultura_data)

    #     # Assert
    #     assert result.id is not None
    #     assert db_session.query(Cultura).count() == 1
        
    #     # Verifica os valores persistidos
    #     db_cultura = db_session.query(Cultura).first()
    #     assert db_cultura.nome_cultura == "Algodão"
    #     assert db_cultura.ano_safra == 2024