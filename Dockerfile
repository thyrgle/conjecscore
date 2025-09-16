FROM ghcr.io/astral-sh/uv:alpine

RUN apk update && apk add nodejs npm

WORKDIR /code
COPY pyproject.toml /code/pyproject.toml
COPY tailwind.config.js /code/tailwind.config.js
COPY tsconfig.json /code/tsconfig.json
COPY eslint.config.mts /code/eslint.config.mts
COPY package.json /code/package.json
COPY ./templates /code/templates
COPY ./static /code/static
COPY ./app /code/app
RUN npm install
RUN npx @tailwindcss/cli -i ./static/tw.css -o ./static/output.css
RUN npx tsc
CMD ["uv", "run", "fastapi", "run", "app/main.py"]
