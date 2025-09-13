FROM python:3.9

WORKDIR /code
RUN pip install --no-cache-dir uv
COPY pyproject.toml /code/pyproject.toml
COPY uv.lock /code/uv.lock
COPY templates/*.j2 /code/templates
COPY app/*.py /code/app
COPY static/* /code/static
RUN python -m uv sync
