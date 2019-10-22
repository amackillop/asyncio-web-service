all: build test deploy

.PHONY: wheels
build:
	cp Pipfile* docker/
	cp -r src docker/src
	docker build -t aio-app docker/
	rm docker/Pipfile*
	rm -r docker/src

.PHONY: test
test:
	echo no tests yet


.PHONY: deploy
deploy:
	echo no deployment yet