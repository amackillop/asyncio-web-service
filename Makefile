all: build test push deploy

.PHONY: build
build:
	pipenv lock --requirements > docker/requirements.txt
	cp -r src docker/
	docker-compose build
	rm -rf docker/requirements.txt docker/src

.PHONY: test
test:
	# Type Checking
	mypy src
	# Running Tests
	pytest src

.PHONY: push
push:
	docker push amackillop/aio-app

.PHONY: deploy
deploy:
	kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
	kubectl apply -f kubernetes/deployment.yaml

.PHONY: teardown
teardown:
	kubectl delete -f kubernetes/deployment.yaml

.PHONY: run
run:
	bash -c "trap 'docker-compose down --remove-orphans' EXIT; \
		docker-compose up --scale app=3"

# Weird bug with this
# deploy:
# 	docker stack deploy --orchestrator=kubernetes -c docker-compose.yaml aio-app
