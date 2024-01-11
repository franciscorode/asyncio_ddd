-include .env
export
export PYTHONPATH := $(shell pwd)
export PROJECT_NAME = asyncio_ddd

.PHONY: help

help:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

install:
	python3 -m pip install --upgrade pip
	pip3 install -r requirements/requirements-app.txt -r requirements/requirements-dev.txt -r requirements/requirements-test.txt

install-app:
	python3 -m pip install --upgrade pip
	pip3 install -r requirements/requirements-app.txt

uninstall:
	pip3 freeze | xargs pip3 uninstall -y

test:
	pytest tests

format:
	ruff --fix ${PROJECT_NAME} tests
	black ${PROJECT_NAME} tests

lint:
	black ${PROJECT_NAME} tests --check
	mypy ${PROJECT_NAME} tests
	ruff check ${PROJECT_NAME} tests  || true

clean:
	rm -rf .idea
	rm -rf .pytest_cache
	rm -f .coverage
	rm -rf output
	rm -rf .mypy_cache
	rm -rf .ruff_cache


run:
	python3 -m uvicorn asyncio_ddd.application:app --reload

coverage:
	pytest --cov-report term-missing --cov=${PROJECT_NAME}

wait-postgres:
	while ! curl http://localhost:${EXTERNAL_POSTGRES_PORT}/ 2>&1 | grep -q '52'; do sleep 1; done;

wait-rabbitmq:
	while ! curl -s localhost:15672 > /dev/null; do sleep 1; done;

###############################
###     DOCKER HELPERS      ###
###############################

up:
	docker-compose ${DOCKER_COMPOSE_FILES} up --build -d

down:
	docker-compose ${DOCKER_COMPOSE_FILES} down

downup: down up

###############################
### DB MIGRATIONS MANAGEMENT ##
###############################

create-migration:
	alembic revision --autogenerate -m "$(m)"

run-migrations:
	alembic upgrade head