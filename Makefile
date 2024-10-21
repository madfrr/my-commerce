HOST_NAME=southamerica-east1-docker.pkg.dev
PROJECT_NAME = my-commerce-api

PROD_GCP_PROJECT_ID = awesome-lotus-439201-k2
PROD_DESTINATION = $(HOST_NAME)/$(PROD_GCP_PROJECT_ID)/$(PROJECT_NAME)

NON_PROD_GCP_PROJECT_ID = awesome-lotus-439201-k2
NON_PROD_DESTINATION = $(HOST_NAME)/$(NON_PROD_GCP_PROJECT_ID)/$(PROJECT_NAME)

VERSION=$(shell (git rev-parse HEAD))

setup-local-dev-environment:
	python3 -m venv venv && . ./venv/bin/activate && pip install -r requirements-dev.txt

develop:
	uvicorn --app-dir=./src server:api --reload --port 5000

develop-docker:
	docker compose up --build

lint:
	ruff check --output-format=github ./src

format:
	ruff format -v ./src

test:
	pytest tests --cov=src

test-html:
	pytest tests --cov=src --cov-report html

deploy:
	@echo "Version ID: $(VERSION)";
	docker build --tag $(PROD_DESTINATION)/$(VERSION) .
	docker push $(PROD_DESTINATION)/$(VERSION)
