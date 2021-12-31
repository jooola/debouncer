.PHONY: install format lint test

SHELL = bash
CPU_CORES = $(shell nproc)

all: install format lint test

install-poetry:
	curl -sSL https://install.python-poetry.org | python3 -

INSTALL_STAMP := .installed
install: $(INSTALL_STAMP)
$(INSTALL_STAMP):
	poetry install
	touch $(INSTALL_STAMP)

format: install
	poetry run black .
	poetry run isort . --profile black

lint: install
	poetry run black . --diff --check
	poetry run isort . --profile black --check
	poetry run pylint funnel tests
	poetry run mypy funnel

test: install
	poetry run pytest -n $(CPU_CORES) --color=yes -v --cov=funnel tests

run: install
	poetry run funnel

ci-publish:
	poetry publish --no-interaction --build

release: lint test
	bash scripts/release.sh
