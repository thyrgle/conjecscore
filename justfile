all: frontend backend

ci: frontend tests

tests:
	uv run pytest

frontend:
	npm install tailwindcss
	npx @tailwindcss/cli -i ./static/tw.css -o ./static/output.css
	npm install typescript
	npx tsc

backend:
	uv run fastapi run app/main.py
