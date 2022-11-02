
build:
	docker-compose build

start-server: build
	docker-compose up

kill-server:
	docker-compose stop -t 1
	docker-compose down

new-server: kill-server start-server

test-server:
	docker-compose run --rm -e ENV_NAME="TEST" proy1-backend poetry run pytest

