start:
	docker run -d -i --name=foobar mosavid

test:
	docker exec -t foobar black main.py project tests
	docker exec -t foobar mypy main.py project tests
	docker exec -t foobar python -m pytest

test-only:
	docker exec -t python -m pytest $(TARGET)

build:
	docker build -t mosavid -f Dockerfile-test .

stop:
	docker stop foobar
	docker container rm foobar