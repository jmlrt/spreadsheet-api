QUART_APP := spreadsheet_api.app:app
QUART_CONFIG := $$(pwd)/config-example.py
QUART_ENV := development

.PHONY: run
run:
	poetry install
	QUART_APP=$(QUART_APP) QUART_CONFIG=$(QUART_CONFIG) QUART_ENV=$(QUART_ENV) poetry run quart run

.PHONY: clean
clean:
	find . -type d -name __pycache__ -exec rm -r {} \+

.PHONY: pre-commit
pre-commit:
	poetry run pre-commit run --all-files
