test:
	black main.py project tests
	mypy main.py project tests
	python -m pytest

test-only:
	python -m pytest $(TARGET)