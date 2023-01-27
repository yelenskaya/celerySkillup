FROM python:3.11

WORKDIR /usr/src/app

EXPOSE 80

RUN pip install poetry

COPY pyproject.toml poetry.lock /usr/src/app/
RUN poetry install

COPY . /usr/src/app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
