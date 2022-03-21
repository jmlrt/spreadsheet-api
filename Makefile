CONFIG_FILE := config-test.toml

.PHONY: run
run:
	poetry install
	QUART_ENV="development" poetry run spreadsheet-api -c $$(pwd)/$(CONFIG_FILE)

.PHONY: clean
clean:
	find . -type d -name __pycache__ -exec rm -r {} \+

.PHONY: pre-commit
pre-commit:
	poetry run pre-commit run --all-files
