.PHONY: help install install-dev test lint format clean run

help:
	@echo "File Organizer - Development Commands"
	@echo ""
	@echo "make install      - Install production dependencies"
	@echo "make install-dev  - Install development dependencies"
	@echo "make test         - Run tests"
	@echo "make lint         - Run linting checks"
	@echo "make format       - Format code with black and isort"
	@echo "make clean        - Remove build artifacts and cache"
	@echo "make run          - Run the application"

install:
	pip install -e .

install-dev:
	pip install -r requirements-dev.txt
	pip install -e .

test:
	python -m unittest discover tests -v

lint:
	@echo "Checking code syntax..."
	python -m py_compile main.py
	@echo "Code syntax OK!"

format:
	@echo "Formatting code..."
	@command -v black >/dev/null 2>&1 && black main.py || echo "black not installed"
	@command -v isort >/dev/null 2>&1 && isort main.py || echo "isort not installed"

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	rm -rf build/ dist/ *.egg-info .pytest_cache/ .mypy_cache/

run:
	python main.py
