# base image
FROM python:3.7.2-alpine

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# add and install requirements
RUN pip install pipenv
COPY Pipfile* /usr/src/app
RUN pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt

# add app
COPY . /usr/src/app

# run server
CMD python manage.py run -h 0.0.0.0