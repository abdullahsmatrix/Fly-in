POETRY := poetry
.PHONY: install run debug clean lint lint-strict

install:
	$(POETRY) install

run:
	$(POETRY) run python3 main.py

test-scripts:
	$(POETRY) run python3 -m pytest Test_scripts/

debug:
	$(POETRY) run python3 -m pdb main.py

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -prune -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -prune -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

lint:
	$(POETRY) run flake8 .
	$(POETRY) run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(POETRY) run flake8 .
	$(POETRY) run mypy . --strict
