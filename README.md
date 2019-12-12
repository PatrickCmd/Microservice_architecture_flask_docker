# Microservice Architecture Flask React and Docker

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
When you get the error Target database is not up to date, try:
```
$ docker-compose exec users python manage.py db stamp heads
$ docker-compose exec users python manage.py db current
$ docker-compose exec users python manage.py db migrate
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
Run the client react tests
```
$ docker-compose exec client npm test
```
Run the client react tests with verbosity
```
$ docker-compose exec client npm test -- --verbose
```
Run the client react tests with coverage
```
$ docker-compose exec client react-scripts test --coverage --watchAll=false --verbose
```
Run End to end tests
```
$ ./node_modules/.bin/cypress open
```
Run End to end tests on production build
```
$ docker-compose -f docker-compose-prod.yml up -d --build

$ docker-compose -f docker-compose-prod.yml exec users python manage.py recreate_db

$ docker-compose -f docker-compose-prod.yml exec users python manage.py seed_db
$ ./node_modules/.bin/cypress open --config baseUrl=http://localhost
```

## Automated testing
#### Run server-side tests
```
$ sh test.sh server
```
#### Run client-side tests
```
$ sh test.sh client
```
#### Run e2e tests
```
$ sh test e2e
```
#### Run all tests
Run the bash script to run all tests.
```
$ sh test.sh all
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
$ \c users_dev
$ select * from users
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
Export REACT APP URL
```
export REACT_APP_USERS_SERVICE_URL=http://DOCKER_MACHINE_IP
```

## Point docker-machine back to localhost
```
eval $(docker-machine env -u)
```

## Flask and Extensions
- [Flask]()
- [API](https://flask.palletsprojects.com/en/1.1.x/api/)
- [Flask Blueprints](https://flask.palletsprojects.com/en/1.1.x/blueprints/)
- [Flask Restful](https://flask-restful.readthedocs.io/en/latest/index.html)
- [Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/en/latest/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
- [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/13/index.html)

## Nginx
- [Nginx Reverse Proxy](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/)
- [Proxying WebSockets with Nginx](https://chrislea.com/2013/02/23/proxying-websockets-with-nginx/)


## Authentication and Authorization
- [Wiki](https://en.wikipedia.org/wiki/Authentication#Authorization)
- [Geeks](https://www.geeksforgeeks.org/difference-between-authentication-and-authorization/)
- [JWT TOKENS](https://jwt.io/introduction/)
- [Cookie vs Token-Base Authentication](https://dzone.com/articles/cookies-vs-tokens-the-definitive-guide)
- [CSRF Attacks Demystified](https://www.gnucitizen.org/blog/csrf-demystified/)
- [SWT vs JWT](https://www.networknt.com/architecture/swt-vs-jwt/)

## Docker for Desktop
- Docker
- Docker Machine
- Docker-Compose
- Docker Daemon
- Kubernetes

## Registries
- GCR, Docker Hub, ECR, ACR

## Docker Docs
- [Docker](https://docs.docker.com/get-started/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Docker Machine](https://docs.docker.com/machine/)

## React App
- [Create React App](https://create-react-app.dev/)

## Axios
- [Axios Blog](https://blog.logrocket.com/how-to-make-http-requests-like-a-pro-with-axios/)
- [Flaviocopes](https://flaviocopes.com/axios/)
- [alligator.io](https://alligator.io/react/axios-react/)
- [Github](https://github.com/axios/axios)

## Bulma Css
- [Bulma.io](https://bulma.io/)

## React Router
- [React-Router](https://reacttraining.com/react-router/web/guides/quick-start)

## React Testing
- [Jest](https://jestjs.io/docs/en/getting-started)
- [Enzyme](https://airbnb.io/enzyme/https://airbnb.io/enzyme/https://airbnb.io/enzyme/)
- [Router Testing Guide](https://github.com/ReactTraining/react-router/blob/master/packages/react-router/docs/guides/testing.md)
- [React Testing Library - Works best with hooks](https://github.com/testing-library/react-testing-library)

## End to End Testing
- [Cypress](https://www.cypress.io/)
- [Cypress API](https://docs.cypress.io/api/api/table-of-contents.html)

## Swagger
- [OPENAPI(OAI)](https://www.openapis.org/)
- [SWagger](https://swagger.io/docs/specification/about/)
- [Swagger Specification](https://swagger.io/specification/)
- [JSON to YAML / YAML to JSON](https://www.json2yaml.com/)