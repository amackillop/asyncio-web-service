all: wheels app

wheels:
	rm -f .dist/*
	pipenv lock --requirements > docker/builder/requirements.txt
	./docker/builder/build_image.sh aio-app-builder
	docker run -v $(realpath .dist):/.dist aio-app-builder
	rm docker/builder/requirements.txt

app:
	if ! [ -d ".dist" ]; then echo "Can't find wheels, run \`make wheels\` first." && exit 1; fi
	cp -r .dist docker/app/.dist
	cp -r src docker/app/src
	./docker/app/build_image.sh aio-app
	rm -r docker/app/.dist
	rm -r docker/app/src
