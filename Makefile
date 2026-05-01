VERSION ?= 3.11

.PHONY: py-version

run:
	@PYTHONDONTWRITEBYTECODE=1 uv run python -m src.app.main

py-version:
	@uv python install $(VERSION)
	@uv python pin $(VERSION)
	$(MAKE) reinstall-deps

reinstall-deps:
	@rm -rf .venv
	@uv venv
	@uv sync
