.PHONY: build start test coverage open-coverage

start:
	docker-compose -f docker-compose-dev.yml down
	docker-compose -f docker-compose-dev.yml up -d --build
	docker exec -ti brain-ag-api uvicorn brain_app.main:app --host 0.0.0.0 --port 8000 --reload

stop:
	docker-compose -f docker-compose-dev.yml down

test:
	docker-compose -f docker-compose-dev.yml up -d && docker exec -ti brain-ag-api pytest -sv

cov:
	docker exec -ti brain-ag-api python -m pytest . --cov -x
	
opencoverage:
	docker exec -ti brain-ag-api python -m pytest --cov-report html
	@echo "Abrindo relatório de coverage em htmlcov/index.html"
	xdg-open htmlcov/index.html || open htmlcov/index.html || echo "Abra htmlcov/index.html manualmente"

dockerexec:
	docker exec -ti brain-ag-api bash

lint:
	@echo "\n---------- Runs isort, black and flake8. Organizing and linting code. -----------\n"
	@echo "\n-------------------------------- Running flake8. --------------------------------\n"
	docker exec -ti brain-ag-api flake8 .
	@echo "\n--------------------------------- Running black ---------------------------------\n"
	docker exec -ti brain-ag-api black .
	@echo "------------------------------- Running isort -----------------------------------\n"
	docker exec -ti brain-ag-api isort .