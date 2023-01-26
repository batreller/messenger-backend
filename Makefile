run:
	python -m package
docker-up:
	docker compose up
test:
	PYTEST_ENV=true python -m pytest tests/ -s
