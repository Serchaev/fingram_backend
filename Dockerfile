FROM python:3.10

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

RUN openssl genrsa -out jwt-private.pem 2048
RUN openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem

RUN pip install --upgrade pip
RUN pip install poetry

COPY poetry.lock pyproject.toml /usr/src/app/
RUN poetry install --no-dev

COPY . /usr/src/app/
