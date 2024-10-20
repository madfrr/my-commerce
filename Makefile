HOST_NAME=southamerica-east1-docker.pkg.dev
PROJECT_NAME = my-commerce-api

PROD_GCP_PROJECT_ID = awesome-lotus-439201-k2
PROD_DESTINATION = $(HOST_NAME)/$(PROD_GCP_PROJECT_ID)/$(PROJECT_NAME)

NON_PROD_GCP_PROJECT_ID = awesome-lotus-439201-k2
NON_PROD_DESTINATION = $(HOST_NAME)/$(NON_PROD_GCP_PROJECT_ID)/$(PROJECT_NAME)

VERSION=$(shell (git rev-parse HEAD))

develop:
	uvicorn --app-dir=./src server:api --reload --port 5000

develop-docker:
	docker compose up --build

check:
	ruff check --fix --no-cache ./src

format:
	ruff format ./src

develop-docker-build:
	@make build
	docker run --rm -t \
	--env-file .env \
	-p 5000:5000 \
	-v `pwd`/src:/api \
	--name $(PROJECT_NAME)  \
	$(PROJECT_NAME):$(VERSION)

build:
	docker build --tag $(PROJECT_NAME):$(VERSION) .

stop:
	docker stop $(PROJECT_NAME)

deploy:
	@echo "Version ID: $(VERSION)";
	docker build --tag $(PROD_DESTINATION)/$(VERSION) .
	docker push $(PROD_DESTINATION)/$(VERSION)
