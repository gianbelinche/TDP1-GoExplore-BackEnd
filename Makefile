
start-server:
	docker-compose up --build

kill-server:
	docker-compose stop -t 1
	docker-compose down

new-server: kill-server start-server
