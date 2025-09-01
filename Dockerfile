FROM python:3.13
ENV PYTHONUNBUFFERED 1
RUN apt-get update
RUN apt-get install -y swig libssl-dev dpkg-dev

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files.
ADD pyproject.toml /code/
ADD uv.lock* /code/
WORKDIR /code

# Install dependencies at system level.
RUN uv sync --frozen --no-dev

ADD misc/dokku/CHECKS /app/
ADD misc/dokku/* /code/

COPY . /code/
RUN /code/manage.py collectstatic --noinput
