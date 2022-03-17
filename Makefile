all: stylecheck test

stylecheck:
	flake8 ganttly/*.py
	flake8 ganttly/tests/*.py

test:
	pytest --cov-report term-missing --cov=ganttly ganttly/tests/ --cov-branch
