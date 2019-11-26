all: build test push deploy

.PHONY: build test push deploy run deploy

build:
	cp -r Pipfile* src docker/
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
		docker-compose -f docker/docker-compose.yaml up --scale app=3"

deploy:
	docker stack deploy -c docker/docker-compose.yaml aio-app
