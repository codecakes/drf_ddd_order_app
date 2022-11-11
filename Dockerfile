FROM python:3.10.2

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y && apt-get install -y --no-install-recommends libsqlite3-dev && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN python3 -m pip install -U pip && python3 -m pip install --no-cache-dir poetry gunicorn

WORKDIR /app

COPY order_app /app/order_app
COPY *.toml /app/
COPY poetry.lock /app

ENV PYTHONPATH /app
RUN export PYTHONPATH=$PYTHONPATH:/app/order_app
RUN poetry install

CMD poetry run gunicorn order_app.infrastructure.order_mgmt.wsgi:application