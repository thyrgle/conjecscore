all: frontend backend

ci: frontend tests

tests:
	uv run pytest

frontend:
	npm install
	npx @tailwindcss/cli -i ./static/tw.css -o ./static/output.css
	npx tsc

backend:
	uv run fastapi dev app/main.py
