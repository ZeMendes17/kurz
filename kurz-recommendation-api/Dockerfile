FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml /app/

RUN pip install --no-cache-dir poetry

RUN poetry install --no-root

COPY . /app

EXPOSE 8000

CMD ["poetry", "run", "start"]