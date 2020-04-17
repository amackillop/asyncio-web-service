all: build test push deploy

.PHONY: build
build:
	pipenv lock --requirements > docker/requirements.txt
	cp -r src docker/
	docker-compose build
	rm -rf docker/requirements.txt docker/src

.PHONY: test
test:
	# Lint Check
	# stop the build if there are Python syntax errors or undefined names
	pipenv run flake8 src --count --select=E9,F63,F7,F82 --show-source --statistics
	# Type Check
	pipenv run mypy src
	# Run Tests
	pipenv run pytest src

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

.PHONY: setup-ci
setup-ci:
	python -m pip install --upgrade pip
	python -m pip install pipenv
	pipenv sync --dev