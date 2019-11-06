all: build test push deploy

.PHONY: build test push deploy run start stop

build:
	cp -r Pipfile* src docker/
	# docker build -t amackillop/aio-app docker/
	docker-compose -f docker/docker-compose.yaml build
	rm -rf docker/Pipfile* docker/src

test:
	echo no tests yet

push:
	docker push amackillop/aio-app

deploy:
	kubectl apply -f kubernetes/deployment.yaml

run:
	bash -c "trap 'docker-compose -f docker/docker-compose.yaml down --remove-orphans' EXIT; \
		docker-compose -f docker/docker-compose.yaml up --scale app=10"

start:
	docker-compose -f docker/docker-compose.yaml up -d --scale app=10

stop:
	docker-compose -f docker/docker-compose.yaml down --remove-orphans

