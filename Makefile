.DEFAULT_GOAL := environment
COMPOSE_SERVICE = python
COMPOSE_SHELL = ash
COMPOSE_COMMAND = docker-compose -f docker/docker-compose.yml
COMPOSE_RUN = ${COMPOSE_COMMAND} run --rm
PROJECT = $(shell basename $(shell pwd))
CI_IMAGE_TAG = local/${PROJECT}
TESTS = /python-testing/bin/pytest --cov-report=term-missing --cov=index tests

environment:
	${COMPOSE_COMMAND} build

shell:
	${COMPOSE_RUN} ${COMPOSE_SERVICE} ${COMPOSE_SHELL}

root:
	${COMPOSE_RUN} -u root ${COMPOSE_SERVICE} ${COMPOSE_SHELL}

clean:
	${COMPOSE_COMMAND} down --rmi=local --volumes
	rm -rf .pytest_cache .coverage python/__pycache__ tests/__pycache__

.PHONY: python
python:
	${COMPOSE_RUN} ${COMPOSE_SERVICE} python

.PHONY: tests
tests:
	${COMPOSE_RUN} ${COMPOSE_SERVICE} ${TESTS}

tests-actual:
	PYTHONPATH=/python-testing/lib/python3.6/site-packages:/home/app/project/python \
	AWS_DEFAULT_REGION=us-east-1 \
	${TESTS}
