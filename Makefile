up:
	docker-compose up -d --remove-orphans test

test-e2e:
	docker-compose run -w /home/app/tests test "cypress run"

test:
	docker-compose run test "black ."
	docker-compose run test "mypy main.py project tests"
	docker-compose run test pytest

test-only:
	docker-compose run test "pytest $(TARGET)"

build:
	docker-compose build test

build-shell:
	docker-compose build shell

run-shell:
	docker-compose run shell

stop:
	docker stop foobar
	docker container rm foobar