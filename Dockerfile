FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN apt-get update
RUN apt-get install -y swig libssl-dev dpkg-dev netcat

RUN pip install -U --pre pip poetry
ADD poetry.lock /code/
ADD pyproject.toml /code/
RUN poetry config virtualenvs.create false
WORKDIR /code
RUN /bin/bash -c '[[ -z "${IN_DOCKER}" ]] && poetry install --no-interaction --no-root || poetry install --no-dev --no-interaction --no-root'

ADD misc/dokku/CHECKS /app/
ADD misc/dokku/* /code/

COPY . /code/
RUN /code/manage.py collectstatic --noinput
