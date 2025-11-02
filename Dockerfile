FROM python:3.14
ENV PYTHONUNBUFFERED=1
RUN apt-get update
RUN apt-get install -y swig libssl-dev dpkg-dev

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files.
ADD pyproject.toml /code/
ADD uv.lock* /code/
WORKDIR /code

# Install dependencies at system level.
RUN uv export --format requirements.txt -o requirements.txt
RUN uv pip install --system -r requirements.txt

COPY . /code/
RUN /code/manage.py collectstatic --noinput
