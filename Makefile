.PHONY: test coverage clean

VENV := .venv
PYTHON := $(VENV)/bin/python
COVERAGE := $(VENV)/bin/coverage

# Ejecutar tests con cobertura y reporte
test:
	$(COVERAGE) run -m unittest discover -s tests -p "test_*.py"
	$(COVERAGE) report -m

# Ejecutar solo reporte de cobertura (asumiendo que ya se ejecutó test)
coverage:
	$(COVERAGE) report -m

# Limpiar archivos de cobertura
clean:
	rm -f .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} +
