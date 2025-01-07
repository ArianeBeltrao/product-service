test:
	pytest -v -s

lint:
	pylint . --ignore=venv

setup:
	pip3 install -r requirements.txt

run:
	docker compose up --build product-service

