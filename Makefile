PYTHON_VERSION ?= 3.12

.PHONY: venv sync run test format
venv:
	uv venv --python $(PYTHON_VERSION) .venv

sync:
	uv sync

run:
	uv run python easy_apply_bot.py

test:
	@tests="$$(find . -type f \( -name 'test_*.py' -o -name '*_test.py' \) \
		! -path './.venv/*' \
		! -path './debug/*' \
		! -path './logs/*' \
		! -path './results/*')"; \
	if [ -z "$$tests" ]; then \
		echo "No tests found."; \
		exit 0; \
	fi; \
	echo "Running tests:"; \
	echo "$$tests"; \
	uv run --with pytest pytest -q $$tests

format:
	uv run --with ruff ruff format .
