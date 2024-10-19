develop:
	uvicorn --app-dir=./src server:api --reload --port 5000
