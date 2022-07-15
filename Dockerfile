FROM python:3.9

RUN mkdir /app
WORKDIR /app

RUN apt update
RUN apt install uwsgi-plugin-python3 -y

COPY ./Pipfile /app/Pipfile
COPY ./Pipfile.lock /app/Pipfile.lock

RUN pip install pipenv
RUN pipenv install
RUN pipenv install uwsgi