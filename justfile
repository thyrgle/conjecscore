flags := if os_family() == "windows" { "--host 127.0.0.1" } else { "" }

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
	uv run fastapi run {{flags}} app/main.py
