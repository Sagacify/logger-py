FROM python:3.5-alpine

WORKDIR /var/www

COPY ./requirements-dev.txt /var/www/requirements-dev.txt
RUN pip install -r requirements-dev.txt

COPY ./src /var/www/src
COPY ./test /var/www/test
