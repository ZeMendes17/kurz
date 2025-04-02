FROM python:3.10

WORKDIR /app

RUN apt update && apt install -y wget

COPY . .

RUN pip install poetry

RUN poetry install

CMD ["poetry", "run", "python3", "src/kurz/mac.py"]