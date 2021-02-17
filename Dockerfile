# pull official base image
FROM python:3.8.3-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
RUN mkdir /code
WORKDIR /code

# install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv
ADD Pipfile Pipfile.lock /code/
RUN pipenv install 
RUN pipenv install --dev

# copy project
ADD . /code/
RUN pipenv run MoneyTracker/manage.py collectstatic
