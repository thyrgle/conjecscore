all: frontend backend

frontend:
	npx @tailwindcss/cli -i ./static/tw.css -o ./static/output.css
	npx tsc

backend:
	uv run fastapi dev app/main.py
