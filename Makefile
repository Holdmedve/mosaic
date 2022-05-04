up:
	docker-compose up -d --remove-orphans test

test-e2e:
	docker-compose run -w /home/tests test "cypress run"

test:
	docker-compose run test "black ."
	docker-compose run test "mypy main.py project tests"
	docker-compose run test pytest

test-only:
	docker exec -t python3 -m pytest $(TARGET)

build:
	docker build -t mosavid -f Dockerfile.test .

stop:
	docker stop foobar
	docker container rm foobar