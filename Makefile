# Note: We need sudo for Makefile.
ci: build-tests test

all: build-run run

clean:
	sudo docker compose down --remove-orphans

build-tests:
	sudo docker compose build tests

#Note: nginx is reserved for deployment, not for local testing.
build-run:
	sudo docker compose build app

run:
	sudo docker compose up app
	sudo docker compose down --remove-orphans

test:
	sudo docker compose run tests
	sudo docker compose down --remove-orphans
