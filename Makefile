start:
	docker run -d -i --name=foobar mosavid

test:
	docker exec foobar ls
	docker exec foobar black main.py project tests
	docker exec foobar mypy main.py project tests
	docker exec foobar python -m pytest

test-only:
	docker exec python -m pytest $(TARGET)

build:
	docker build -t mosavid -f Dockerfile-test .

stop:
	docker stop foobar