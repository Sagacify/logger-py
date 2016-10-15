FROM python:3.5-alpine

WORKDIR /var/www

COPY ./dev-requirements.txt /var/www/requirements-dev.txt
RUN pip install -r dev-requirements-dev.txt

COPY ./src /var/www/src
