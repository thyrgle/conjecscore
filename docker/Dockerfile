FROM python:3.9

WORKDIR /code
RUN pip install --no-cache-dir uv
COPY pyproject.toml /code/pyproject.toml
COPY uv.lock /code/uv.lock
COPY templates/ /code/templates
COPY app/ /code/app
COPY static/ /code/static
RUN python -m uv sync
CMD ['python', '-m', 'uv', 'run', 'fastapi', 'run', 'app/main.py']
