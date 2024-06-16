.PHONY: install run test docker

install:
	pip install -r requirements.txt

run:
	uvicorn app.main:app --reload

test:
	pytest -q

docker:
	docker compose up --build
