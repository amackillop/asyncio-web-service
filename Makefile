all: build test deploy

.PHONY: build test deploy push run

build:
	cp -r Pipfile* src docker/
	docker build -t amackillop/aio-app docker/
	rm -rf docker/Pipfile* docker/src

test:
	echo no tests yet

deploy:
	kubectl apply -f kubernetes/deployment.yaml

push:
	docker push amackillop/aio-app

run:
	docker run --rm --name aio-app -d -p 8000:8000 amackillop/aio-app