all: build test deploy

.PHONY: build test deploy run

build:
	cp -r Pipfile* src docker/
	docker build -t amackillop/aio-app docker/
	rm -rf docker/Pipfile* docker/src

test:
	echo no tests yet

deploy:
	echo no deployment yet

push:
	docker push amackillop/aio-app

run:
	docker run -p 8000:8000 amackillop/aio-app