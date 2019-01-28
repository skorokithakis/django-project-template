FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN apt-get update
RUN apt-get install -y swig libssl-dev dpkg-dev netcat

RUN pip install -U pip poetry
ADD poetry.lock /code/
ADD pyproject.toml /code/
RUN poetry config settings.virtualenvs.create false
WORKDIR /code
RUN poetry install --no-dev --no-interaction

ADD misc/dokku/CHECKS /app/
ADD misc/dokku/* /code/

COPY . /code/
RUN /code/manage.py collectstatic --noinput
