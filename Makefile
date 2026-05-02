VERSION ?= 3.11

.PHONY: py-version

run: py-run

py-run:
	@export PYTHONPATH=src:src/genpb && \
	 export PYTHONDONTWRITEBYTECODE=1 && \
	 uv run python src/app/main.py

smith-run:
	@PYTHONDONTWRITEBYTECODE=1 uv run langgraph dev

py-version:
	@uv python install $(VERSION)
	@uv python pin $(VERSION)
	$(MAKE) reinstall-deps

reinstall-deps:
	@rm -rf .venv
	@uv venv
	@uv sync

gen-pb:
	@mkdir -p src/genpb
	@uv run python -m grpc_tools.protoc \
		-I protos \
		--python_out=src/genpb \
		--grpc_python_out=src/genpb \
		--pyi_out=src/genpb \
		protos/chat/v1/*.proto
	
	@touch src/__init__.py
	@touch src/genpb/__init__.py
	@find src/genpb -type d -exec touch {}/__init__.py \;
