
PORT := 8080
HOST := 0.0.0.0

.SILENT:

start-server:
	poetry run uvicorn "app.main:app" --host $(HOST) --port $(PORT)
