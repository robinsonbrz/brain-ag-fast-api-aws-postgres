.PHONY: build start test coverage open-coverage


build:
	docker-compose down && docker-compose up -d --build

stop:
	docker-compose down

test:
	docker-compose run api pytest -sv

coverage:
	docker-compose run api pytest --cov=brain_app --cov-report=html tests/
	@echo "Abrindo relatório de coverage em htmlcov/index.html"
	xdg-open htmlcov/index.html || open htmlcov/index.html || echo "Abra htmlcov/index.html manualmente"
