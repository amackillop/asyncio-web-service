all: build test push deploy

.PHONY: build test push deploy run up down

build:
	cp -r Pipfile* src docker/
	docker build -t amackillop/aio-app docker/
	rm -rf docker/Pipfile* docker/src

test:
	echo no tests yet

push:
	docker push amackillop/aio-app

deploy:
	kubectl apply -f kubernetes/deployment.yaml

run:
	bash -c "trap 'docker-compose -f docker/docker-compose.yaml down' EXIT; \
		docker-compose -f docker/docker-compose.yaml up"
