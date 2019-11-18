# Microservice_architecture_flask_react_docker

[![Build Status](https://travis-ci.com/PatrickCmd/Microservice_architecture_flask_docker.svg?token=5DLmUBR4W3LuNvxXHAap&branch=devel)](https://travis-ci.com/PatrickCmd/Microservice_architecture_flask_docker)


## Common Commands
Build the images:
```
$ docker-compose build
```
Run the containers:
```
$ docker-compose up -d
```
Build images and run the containers with Nginx
```
docker-compose up -d --build nginx
```
Initialize database and run migrations
```
$ docker-compose exec users python manage.py db init

$ docker-compose exec users python manage.py db migrate

$ docker-compose exec users python manage.py db upgrade
```
Update database tables and upgrade
```
$ docker-compose exec users python manage.py db migrate

$ docker-compose exec users python manage.py db upgrade
```
Re-create the database:
```
$ docker-compose exec users python manage.py recreate_db
```
Seed the database:
```
$ docker-compose exec users python manage.py seed_db
```
Run the tests:
```
$ docker-compose exec users python manage.py test
```
Run the tests with coverage
```
$ docker-compose exec users python manage.py test-cov
```
Code quality and linting
```
$ docker-compose exec users flake8 --max-line-length=100 project
$ docker-compose exec users black project
```

## Other commands
To stop the containers:
```
$ docker-compose stop
```
To bring down the containers:
```
$ docker-compose down
```
Want to force a build?
```
$ docker-compose build --no-cache
```
Remove images:
```
$ docker rmi $(docker images -q)
```

## Postgres
Want to access the database via psql?
```
$ docker-compose exec users-db psql -U postgres
```
Then, you can connect to the database and run SQL queries. For example:
```
# \c users_dev
# select * from users;
```
Access application interactive shell
```
docker-compose exec users python manage.py shell
```
Show application URL routes
```
docker-compose exec users python manage.py routes
```

## Production setup with Docker machine (AWS)
Create remote host with docker machine
```
$ docker-machine create --driver amazonec2 --amazonec2-open-port 8000 --amazonec2-region us-east-2 microservice-architecture-flask
```
Build remote host image
```
$ docker-compose -f docker-compose-prod.yml up -d --build
```
Create database tables
```
$ docker-compose -f docker-compose-prod.yml exec users python manage.py recreate_db
```
Seed the database
```
$ docker-compose -f docker-compose-prod.yml exec users python manage.py seed_db
```
Point docker-machine to active remote hoste
```
$ docker-machine env microservice-architecture-flask
$ eval $(docker-machine env microservice-architecture-flask)
```
Run tests
```
docker-compose exec users python manage.py test
```
Get remote host IP
```
docker-machine ip microservice-architecture-flask
```

## Point docker-machine back to localhost
```
eval $(docker-machine env -u)
```