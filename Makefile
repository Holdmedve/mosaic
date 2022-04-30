up:
	echo $(GOOGLE_APPLICATION_CREDENTIALS)
	docker run -d -i -v $(GOOGLE_APPLICATION_CREDENTIALS):/secret/key.json -e GOOGLE_APPLICATION_CREDENTIALS=/secret/key.json --name=foobar mosavid

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