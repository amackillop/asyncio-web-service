all: build test deploy

.PHONY: build
build:
	cp -r Pipfile* src docker/
	docker build -t aio-app docker/
	rm -rf docker/Pipfile* docker/src

.PHONY: test
test:
	echo no tests yet


.PHONY: deploy
deploy:
	echo no deployment yet