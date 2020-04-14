all: build test push deploy

.PHONY: build test push deploy run deploy

build:
	pipenv lock --requirements > docker/requirements.txt
	cp -r src docker/
	docker-compose build
	rm -rf docker/requirements.txt docker/src

test:
	echo no tests yet

push:
	docker push amackillop/aio-app

deploy:
	kubectl apply -f kubernetes/deployment.yaml

run:
	bash -c "trap 'docker-compose down --remove-orphans' EXIT; \
		docker-compose up --scale app=3"

# deploy:
# 	docker stack deploy -c docker/docker-compose.yaml aio-app
