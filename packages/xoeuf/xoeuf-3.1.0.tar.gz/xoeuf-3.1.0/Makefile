CARGO_HOME ?= $(HOME)/.cargo
PATH := $(HOME)/.rye/shims:$(HOME)/.local/bin:$(CARGO_HOME)/bin:$(PATH)

SHELL := /bin/bash

PYTHON_FILES := $(shell find src/ -type f -name '*.py')

UV := uv
UV_RUN := $(UV) run
RUN ?= $(UV_RUN)

ODOO_VERSION ?= 12.0
PYTHON_VERSION ?= 3.8.17

REQUIRED_UV_VERSION ?= 0.5.31
bootstrap:
	@INSTALLED_UV_VERSION=$$(uv --version 2>/dev/null | awk '{print $$2}' || echo "0.0.0"); \
    UV_VERSION=$$(printf '%s\n' "$(REQUIRED_UV_VERSION)" "$$INSTALLED_UV_VERSION" | sort -V | head -n1); \
	if [ "$$UV_VERSION" != "$(REQUIRED_UV_VERSION)" ]; then \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	fi
	echo $(PYTHON_VERSION) > .python-version
.PHONY: bootstrap

sync install: bootstrap src/odoo-$(ODOO_VERSION)
	@$(UV) sync --frozen
.PHONY: install sync

lock: bootstrap
ifdef update_all
	@$(UV) lock -U
else
	@$(UV) lock
endif
.PHONY: lock

update: bootstrap
	@$(MAKE) lock update_all=1
.PHONY: update

format: sync
	@$(RUN) ruff check --fix src/
	@$(RUN) isort src/
	@$(RUN) ruff format src/
.PHONY: format-python

lint: sync
	@$(RUN) ruff check src/
	@$(RUN) ruff format --check src/
	@$(RUN) isort --check src/
.PHONY: lint

SPHINXOPTS ?= -W
docs/build:
	@$(MAKE) SPHINXOPTS=$(SPHINXOPTS) SPHINXBUILD="$(RUN) sphinx-build" -C docs html
.PHONY: docs/build

DOC_SERVER_PORT ?= 6942
docs/browse: docs/build
	@$(RUN) python -m http.server  \
                       --directory $(PWD)/docs/build/html $(DOC_SERVER_PORT)
.PHONY: docs/browse


# You can tweak these defaults in '.envrc' or by passing them to 'make'.
POSTGRES_USER ?= $(USER)
POSTGRES_PASSWORD ?= $(USER)
POSTGRES_HOST ?= pg
ODOO_MIRROR ?= https://gitlab.merchise.org/merchise/odoo.git
DOCKER_NETWORK_ARG ?= --network=host

test_addons ?=
test_tags ?=
test_extra_args ?=
RUN_UV_ARG ?= --run-uv

test:
	if [ -n "$(test_addons)" ]; then \
		addons="$(test_addons)"; \
    else \
		addons=$$(ls src/tests/ | grep '^test_' | xargs | tr " " ","); \
	fi; \
	if [ -n "$(test_tags)" ]; then \
		tags="--test-tags $(test_addons)"; \
    else \
		tags=""; \
	fi; \
	./runtests-odoo.sh $(RUN_UV_ARG) -i $$addons $$tags $(test_extra_args)
.PHONY: test

DEFAULT_DB_NAME ?= xoeuf

RUNSERVER_CMD ?=
RUNSERVER_DB ?= -d $(DEFAULT_DB_NAME)
RUNSERVER_PG_ARGS ?=
RUNSERVER_WORKERS ?= --workers=0 --max-cron-threads=1
RUNSERVER_LIMITS ?= --limit-time-cpu=600 --limit-time-real=650 --limit-time-real-cron=600
RUNSERVER_UPDATE ?=
RUNSERVER_DEV_MODE ?= --dev=ipdb,reload,qweb,werkzeug,xml
RUNSERVER_LOG_LEVEL ?= --log-level=debug_rpc
RUNSERVER_ADDONS_PATHS ?= --addons-path $(PWD)/src/tests
RUNSERVER_ARGS ?= $(RUNSERVER_CMD) $(RUNSERVER_DB) $(RUNSERVER_PG_ARGS) \
  $(RUNSERVER_LOG_LEVEL) $(RUNSERVER_DEV_MODE) $(RUNSERVER_WORKERS) \
  $(RUNSERVER_LIMITS) $(RUNSERVER_UPDATE) \
  $(RUNSERVER_ADDONS_PATHS)
run:
ifndef NOSYNC
	@$(MAKE) sync
endif
	@$(RUN) xoeuf $(RUNSERVER_ARGS)
.PHONY: run

migrate:
	@$(MAKE) run RUNSERVER_UPDATE="-u all --stop-after-init" RUNSERVER_DEV_MODE=
.PHONY: migrate


TEMPLATE1_PSQL_EXTRA_ARGS ?=
template1:
	@psql -d template1 $(TEMPLATE1_PSQL_EXTRA_ARGS) -c "CREATE EXTENSION unaccent" || true
	@psql -d template1 $(TEMPLATE1_PSQL_EXTRA_ARGS) -c "CREATE EXTENSION postgis" || true


INITIALIZE_DESTROY_DB ?= 1
INITIALIZE_LIMITS ?= $(RUNSERVER_LIMITS)
INITIALIZE_WORKERS ?= --workers=0 --max-cron-threads=1
INITIALIZE_DB ?= -d $(DEFAULT_DB_NAME)
INITIALIZE_PG_ARGS ?= $(RUNSERVER_PG_ARGS)
INITIALIZE_INIT_ADDONS ?= $(shell ls src/tests/ | grep '^test_' | xargs | tr " " ",")
INITIALIZE_DB_TEMPLATE ?= --db-template=template1
INITIALIZE_DEV_MODE ?=
INITIALIZE_WITHOUT_DEMO ?=
INITIALIZE_EXTRA_ARGS ?= --stop-after-init
INITIALIZE_LOG_LEVEL ?= --log-level=warn

initialize:
ifndef NOSYNC
	@$(MAKE) sync
endif
	@if [ -n "$(INITIALIZE_DESTROY_DB)" ]; then echo "Destroying DB '$(DEFAULT_DB_NAME)'"; dropdb $(DEFAULT_DB_NAME) 2>/dev/null || true; echo "Done!"; fi
	@echo "Initializing DB '$(DEFAULT_DB_NAME)'"
	@$(RUN) xoeuf $(INITIALIZE_DB) $(INITIALIZE_PG_ARGS) $(INITIALIZE_WORKERS) \
        $(RUNSERVER_ADDONS_PATHS) \
	    $(INITIALIZE_LIMITS) $(INITIALIZE_DEV_MODE) $(INITIALIZE_LOG_LEVEL) \
        $(INITIALIZE_WITHOUT_DEMO) \
        $(INITIALIZE_DB_TEMPLATE) $(INITIALIZE_EXTRA_ARGS) \
        -i "$(INITIALIZE_INIT_ADDONS)" \
        -u "$(INITIALIZE_INIT_ADDONS)"
.PHONY: initialize template1

py:
	@$(RUN) ipython
.PHONY: py

shell:
	@$(MAKE) run RUNSERVER_CMD="shell"
.PHONY: shell


docker/build:
	docker build -t xoeuf \
	    --build-arg PYTHON_VERSION=$(PYTHON_VERSION) \
	    --build-arg ODOO_VERSION=$(ODOO_VERSION) \
	    --build-arg ODOO_MIRROR=$(ODOO_MIRROR) \
        .
.PHONY: docker/build

docker/test: docker/build
	docker run --rm -it xoeuf /src/xoeuf/runtests-odoo.sh \
        -i $(ls src/tests/ | grep '^test_' | xargs | tr " " ",") \
		$(DOCKER_NETWORK_ARG) \
        --db_host=$(POSTGRES_HOST) \
        --db_user=$(POSTGRES_USER) \
        --db_password=$(POSTGRES_PASSWORD)
.PHONY: docker/test docker/build


ODOO_MIRROR ?= https://gitlab.merchise.org/merchise/odoo.git

src/odoo-$(ODOO_VERSION):
ifndef lite
	@if [ ! -d src/odoo-$(ODOO_VERSION) ]; then \
		git clone --depth 1 -b merchise-develop-$(ODOO_VERSION) \
           $(ODOO_MIRROR) \
           src/odoo-$(ODOO_VERSION); \
    else \
        cd src/odoo-$(ODOO_VERSION); git pull; \
		cd ../../; \
    fi; \
	rm -rf src/odoo-$(ODOO_VERSION)/pyproject.toml; \
	rm -rf src/odoo; \
	cd src; ln -s odoo-$(ODOO_VERSION) odoo; \
	cd odoo; ln -s ../../extra/pyproject-odoo-$(ODOO_VERSION).toml pyproject.toml
endif
.PHONY: src/odoo-$(ODOO_VERSION)
