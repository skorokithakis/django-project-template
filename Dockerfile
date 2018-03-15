FROM python:3
ENV PYTHONUNBUFFERED 1
RUN apt-get update
RUN apt-get install -y swig libssl-dev dpkg-dev netcat

RUN pip install -U pip pipenv
ADD Pipfile* /code/
WORKDIR /code
RUN pipenv install --system --ignore-pipfile

ADD misc/dokku/CHECKS /app/
ADD misc/dokku/* /code/

COPY . /code/
RUN /code/manage.py collectstatic --noinput
