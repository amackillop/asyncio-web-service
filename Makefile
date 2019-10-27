all: build test deploy

.PHONY: build test deploy

build:
	cp -r Pipfile* src docker/
	docker build -t aio-app docker/
	rm -rf docker/Pipfile* docker/src

test:
	echo no tests yet

deploy:
	echo no deployment yet