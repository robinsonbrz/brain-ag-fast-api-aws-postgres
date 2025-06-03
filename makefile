.PHONY: build start test coverage open-coverage

start:
	docker-compose -f docker-compose-dev.yml down && docker-compose -f docker-compose-dev.yml up -d --build && docker exec -ti brain-ag-api uvicorn brain_app.main:app --host 0.0.0.0 --port 8000 --reload

stop:
	docker-compose -f docker-compose-dev.yml down

test:
	docker exec -ti brain-ag-api pytest -sv

coverage:
	docker exec -ti brain-ag-api pytest --cov=brain_app --cov-report=html tests/
	@echo "Abrindo relatório de coverage em htmlcov/index.html"
	xdg-open htmlcov/index.html || open htmlcov/index.html || echo "Abra htmlcov/index.html manualmente"
