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

build-web:
	make -C web

format: install
	poetry run black .
	poetry run isort . --profile black

lint: install
	poetry run black . --diff --check
	poetry run isort . --profile black --check
	poetry run pylint --jobs=$(CPU_CORES) debouncer tests
	poetry run mypy debouncer

test: install
	mkdir -p web/dist/assets
	poetry run pytest -n $(CPU_CORES) --color=yes -v --cov=debouncer tests

run: install
	poetry run uvicorn debouncer:app --port 4000 --reload

ci-publish:
	poetry publish --no-interaction --build

release: lint test
	bash scripts/release.sh

docker:
	docker build -t ghcr.io/jooola/debouncer .
