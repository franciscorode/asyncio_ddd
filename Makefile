-include .env
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
	pycln ${PROJECT_NAME} tests
	isort ${PROJECT_NAME} tests
	black ${PROJECT_NAME} tests

lint:
	pycln ${PROJECT_NAME} tests --check
	flake8 ${PROJECT_NAME} tests
	isort ${PROJECT_NAME} tests --check-only
	black ${PROJECT_NAME} tests --check
	mypy ${PROJECT_NAME} tests
	pylint ${PROJECT_NAME} tests --recursive=y --exit-zero

clean:
	rm -rf .idea
	rm -rf .pytest_cache
	rm -f .coverage
	rm -rf output
	rm -rf .mypy_cache


run:
	python3 -m uvicorn asyncio_ddd.application:app --reload

###############################
###     DOCKER HELPERS      ###
###############################

up:
	docker-compose ${DOCKER_COMPOSE_FILES} up --build -d

down:
	docker-compose ${DOCKER_COMPOSE_FILES} down

downup: down up