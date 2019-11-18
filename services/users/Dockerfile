# base image  # Since Flask-Bcrypt depends on some libraries that need to be compiled,
              # we'll use a different starter image in the Dockerfile.
FROM python:3.7.2-slim

# install netcat
RUN apt-get update && \
    apt-get -y install netcat gcc && \
    apt-get clean

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# add and install requirements
RUN pip install pipenv
COPY Pipfile* /usr/src/app
RUN pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt

# add entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# add app
COPY . /usr/src/app

# run server
CMD ["/usr/src/app/entrypoint.sh"]