up:
	docker-compose up -d --remove-orphans test

test:
	docker-compose run test pytest

test-only:
	docker-compose run test "pytest $(TARGET)"

build:
	docker-compose build test

build-shell:
	docker-compose build shell

run-shell:
	docker-compose run shell

code-format:
	docker-compose run test "autoflake --in-place --remove-all-unused-imports --remove-unused-variables -r tests project main.py"
	docker-compose run test "black ."
	docker-compose run test "mypy ."

stop:
	docker stop foobar
	docker container rm foobar

profile:
	python -m cProfile -o snakeviz.prof profiler.py

profile-result:
	snakeviz snakeviz.prof