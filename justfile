all: frontend backend

ci: frontend tests

tests:
	uv run pytest

frontend:
	npm install tailwindcss @tailwindcss/cli --yes
	npm install --save-dev typescript --yes
	npx @tailwindcss/cli -i ./static/tw.css -o ./static/output.css
	npx tsc

backend:
	uv run fastapi run app/main.py
