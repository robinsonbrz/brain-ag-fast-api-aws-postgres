import pytest
from sqlalchemy.orm import Session
from brain_app.models.models import Cultura
from brain_app.repositories.cultura_repository import CulturaRepository
from brain_app.schemas.cultura_schema import CulturaCreateSchema, CulturaUpdateSchema


class TestCulturaRepository:
    def test_get_by_id_mocked(self, db_session, monkeypatch):

        repo = CulturaRepository(db_session)
        mock_cultura = Cultura(id=1, fazenda_id=1, nome_cultura="Soja", ano_safra=2023, area_plantada=50.0)
        def mock_query(*args, **kwargs):
            '''
            Substitui o comportamento real do SQLAlchemy por:
            mock que sempre retorna a mock_cultura.
            Simula a cadeia de chamadas: session.query().filter().first().
            '''
            class MockQuery:
                def filter(*args, **kwargs):
                    class MockFilter:
                        def first(*args, **kwargs):
                            return mock_cultura
                    return MockFilter()
            return MockQuery()

        monkeypatch.setattr(db_session, "query", mock_query)
        result = repo.get_by_id(1)

        assert result == mock_cultura
        assert result.id == 1
        assert result.nome_cultura == "Soja"

    def test_get_all(self, db_session, monkeypatch):
        repo = CulturaRepository(db_session)
        mock_culturas = [
            Cultura(id=1, fazenda_id=1, nome_cultura="Soja", ano_safra=2023, area_plantada=50.0),
            Cultura(id=2, fazenda_id=1, nome_cultura="Milho", ano_safra=2023, area_plantada=30.0)
        ]
        def mock_query(*args, **kwargs):
            class MockQuery:
                def offset(*args, **kwargs):
                    return MockQuery()
                def limit(*args, **kwargs):
                    return MockQuery()
                def all(*args, **kwargs):
                    return mock_culturas
            return MockQuery()
        
        monkeypatch.setattr(db_session, "query", mock_query)
        result = repo.get_all()
        
        assert result == mock_culturas
        assert len(result) == 2
        assert result[0].nome_cultura == "Soja"
        assert result[1].nome_cultura == "Milho"

    def test_create(self, db_session, monkeypatch):

        repo = CulturaRepository(db_session)
        cultura_create = CulturaCreateSchema(
            fazenda_id=1,
            nome_cultura="Café",
            ano_safra=2024,
            area_plantada=25.0
        )
        
        calls = []
        
        def mock_add(cultura):
            calls.append(("add", cultura))
            cultura.id = 1
        
        def mock_commit():
            calls.append(("commit",))
        
        def mock_refresh(cultura):
            calls.append(("refresh", cultura))
        
        monkeypatch.setattr(db_session, "add", mock_add)
        monkeypatch.setattr(db_session, "commit", mock_commit)
        monkeypatch.setattr(db_session, "refresh", mock_refresh)
        
        result = repo.create(cultura_create)
        
        assert result.id == 1
        assert result.fazenda_id == cultura_create.fazenda_id
        assert result.nome_cultura == cultura_create.nome_cultura
        assert result.ano_safra == cultura_create.ano_safra
        assert result.area_plantada == cultura_create.area_plantada
        assert calls == [("add", result), ("commit",), ("refresh", result)]

    def test_update(self, db_session, monkeypatch):
        repo = CulturaRepository(db_session)
        cultura_db = Cultura(id=1, fazenda_id=1, nome_cultura="Soja", ano_safra=2023, area_plantada=50.0)
        cultura_update = CulturaUpdateSchema(nome_cultura="Milho", ano_safra=2024, area_plantada=60.0)

        calls = []
        
        def mock_commit():
            calls.append(("commit",))
        
        def mock_refresh(cultura):
            calls.append(("refresh", cultura))
        
        monkeypatch.setattr(db_session, "commit", mock_commit)
        monkeypatch.setattr(db_session, "refresh", mock_refresh)

        result = repo.update(cultura_db, cultura_update)
        
        assert result == cultura_db
        assert result.nome_cultura == "Milho"
        assert result.ano_safra == 2024
        assert result.area_plantada == 60.0
        assert calls == [("commit",), ("refresh", cultura_db)]

    def test_delete(self, db_session, monkeypatch):
        repo = CulturaRepository(db_session)
        cultura_db = Cultura(id=1, fazenda_id=1, nome_cultura="Soja", ano_safra=2023, area_plantada=50.0)
        
        calls = []
        
        def mock_delete(cultura):
            calls.append(("delete", cultura))
        
        def mock_commit():
            calls.append(("commit",))
        
        monkeypatch.setattr(db_session, "delete", mock_delete)
        monkeypatch.setattr(db_session, "commit", mock_commit)
        
        repo.delete(cultura_db)
        
        assert calls == [("delete", cultura_db), ("commit",)]

    def test_get_by_fazenda_id(self, db_session, monkeypatch):
        repo = CulturaRepository(db_session)
        mock_culturas = [
            Cultura(id=1, fazenda_id=1, nome_cultura="Soja", ano_safra=2023, area_plantada=50.0),
            Cultura(id=2, fazenda_id=1, nome_cultura="Milho", ano_safra=2023, area_plantada=30.0)
        ]

        def mock_query(*args, **kwargs):
            class MockQuery:
                def filter(*args, **kwargs):
                    return MockQuery()
                def offset(*args, **kwargs):
                    return MockQuery()
                def limit(*args, **kwargs):
                    return MockQuery()
                def all(*args, **kwargs):
                    return mock_culturas
            return MockQuery()
        
        monkeypatch.setattr(db_session, "query", mock_query)
        
        result = repo.get_by_fazenda_id(1)

        assert result == mock_culturas
        assert len(result) == 2
        assert result[0].nome_cultura == "Soja"
        assert result[1].nome_cultura == "Milho"