# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

WORKDIR /app

COPY . .

RUN pip install pipenv

RUN pipenv install --system

RUN pytest

CMD [ "python3", "-m", "coding_assignment" ]