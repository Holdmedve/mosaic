up:
	echo $(GOOGLE_APPLICATION_CREDENTIALS)
	docker run -d -i \
		-v $(GOOGLE_APPLICATION_CREDENTIALS):/secret/key.json \
		-e GOOGLE_APPLICATION_CREDENTIALS=/secret/key.json \
		--name=foobar \
		--entrypoint=/bin/bash \
		mosavid

test:
	docker exec -t foobar black main.py project tests
	docker exec -t foobar mypy main.py project tests
	docker exec -t foobar python3 -m pytest

test-only:
	docker exec -t python3 -m pytest $(TARGET)

build:
	docker build -t mosavid -f Dockerfile-test .

stop:
	docker stop foobar
	docker container rm foobar