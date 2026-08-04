PYTHON := python3
VENV := .venv
PIP := $(VENV)/bin/pip
UV := $(VENV)/bin/uv
PY := $(VENV)/bin/python

.PHONY: install dev clean run

install: $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install uv
	$(UV) pip install .

dev: $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -e .[dev]

run: $(VENV)
	$(PY) -m alkaApps

$(VENV):
	$(PYTHON) -m venv $(VENV)

clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
