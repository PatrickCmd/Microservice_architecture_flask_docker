# Microservice Architecture Flask React and Docker

[![Build Status](https://travis-ci.com/PatrickCmd/Microservice_architecture_flask_docker.svg?token=5DLmUBR4W3LuNvxXHAap&branch=devel)](https://travis-ci.com/PatrickCmd/Microservice_architecture_flask_docker)


## Work Flow
The following commands are for spinning up all the containers.
### Development
#### Environment Variables
```python
import binascii
import os
binascii.hexlify(os.urandom(24))
b'f9ce7926e1b11a1f5e64c152a5a900f5335739224d073ce1'
```
```
$ export SECRET_KEY=f9ce7926e1b11a1f5e64c152a5a900f5335739224d073ce1
```
Export REACT APP URL
```
export REACT_APP_USERS_SERVICE_URL=http://localhost
```
Build the images:
```
$ docker-compose build
```
Run the containers:
```
$ docker-compose up -d
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
Run the e2e tests
```
$ ./node_modules/.bin/cypress open --config baseUrl=http://localhost
```

### Staging setup with Docker machine (AWS)
Create remote host with docker machine
```
$ docker-machine create --driver amazonec2 --amazonec2-open-port 8000 --amazonec2-region us-east-2 microservice-architecture-flask-staging
```
Get remote host IP
```
docker-machine ip microservice-architecture-flask-staging
```
Point docker-machine to the staging server
```
$ docker-machine env microservice-architecture-flask-staging
$ eval $(docker-machine env microservice-architecture-flask-staging)
```
#### Environment Variables
```python
import binascii
import os
binascii.hexlify(os.urandom(24))
b'f9ce7926e1b11a1f5e64c152a5a900f5335739224d073ce1'
```
```
$ export SECRET_KEY=f9ce7926e1b11a1f5e64c152a5a900f5335739224d073ce1
```
Export REACT APP URL
```
export REACT_APP_USERS_SERVICE_URL=http://DOCKER_MACHINE_STAGING_IP
```
Build the images and run the containers
```
$ docker-compose -f docker-compose-stage.yml up -d --build
```
Create database tables
```
$ docker-compose -f docker-compose-stage.yml exec users python manage.py recreate_db
```
Seed the database
```
$ docker-compose -f docker-compose-stage.yml exec users python manage.py seed_db
```
Run tests
```
docker-compose -f docker-compose-stage.yml exec users python manage.py test
```
Run the e2e tests
```
$ ./node_modules/.bin/cypress open --config baseUrl=http://DOCKER_MACHINE_STAGING_IP
```

### Production setup with Docker machine (AWS)
Create remote host with docker machine
```
$ docker-machine create --driver amazonec2 --amazonec2-open-port 8000 --amazonec2-region us-east-2 microservice-architecture-flask
```
Get remote host IP
```
docker-machine ip microservice-architecture-flask
```
Point docker-machine to the production server
```
$ docker-machine env microservice-architecture-flask
$ eval $(docker-machine env microservice-architecture-flask)
```
#### Environment Variables
```python
import binascii
import os
binascii.hexlify(os.urandom(24))
b'f9ce7926e1b11a1f5e64c152a5a900f5335739224d073ce1'
```
```
$ export SECRET_KEY=f9ce7926e1b11a1f5e64c152a5a900f5335739224d073ce1
```
Export REACT APP URL
```
export REACT_APP_USERS_SERVICE_URL=http://DOCKER_MACHINE_IP
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
Run tests
```
docker-compose -f docker-compose-prod.yml exec users python manage.py test
```
Run the e2e tests
```
$ ./node_modules/.bin/cypress open --config baseUrl=http://DOCKER_MACHINE_IP
```

## Test Script
#### Run server-side unit and integration tests (against dev):
```
$ sh test.sh server
```
#### Run client-side unit and integration tests (against dev):
```
$ sh test.sh client
```
#### Run Cypress-based end-to-end tests (against prod)
```
$ sh test e2e
```
#### Run all tests
Run the bash script to run all tests.
```
$ sh test.sh all
```


## Individual Services
The following commands are for spinning up individual containers.

### Users DB
Build and run:
```
$ docker-compose up -d --build users-db
```
Test:
```
$ docker-compose exec users-db psql -U postgres
```
### Users
Build and run:
```
$ docker-compose up -d --build users
```
To test, navigate to http://localhost:5001/users/ping in your browser.

Create and seed the database:
```
$ docker-compose exec users python manage.py recreate_db
$ docker-compose exec users python manage.py seed_db
```
To test, navigate to http://localhost:5001/users in your browser.

Run the unit and integration tests:
```
$ docker-compose exec users python manage.py test
```
Lint:
```
$ docker-compose exec users flake8 --max-line-length=100 project
$ docker-compose exec users black project
```
### Client
Set env variable:
```
$ export REACT_APP_USERS_SERVICE_URL=http://localhost
```
Build and run:
```
$ docker-compose up -d --build client
```
To test, navigate to http://localhost:3007 in your browser.

Keep in mind that you won't be able to register or log in until Nginx is set up.

Run the client-side tests:
```
$ docker-compose exec client npm test -- --verbose
```
### Swagger
Update swagger.json:
```
$ python services/swagger/update-spec.py http://localhost
```
Build and run:
```
$ docker-compose up -d --build swagger
```
To test, navigate to http://localhost:3008 in your browser.

### Nginx
Build and run:
```
$ docker-compose up -d --build nginx
```
With the other services up, you can test by navigating to http://localhost in your browser.

Also, run the e2e tests:
```
$ ./node_modules/.bin/cypress open --config baseUrl=http://localhost
```
#### Aliases
To save some precious keystrokes, let's create aliases for both the docker-compose and docker-machine commands —dc and dm, respectively.

Simply add the following lines to your .bashrc file:
```
alias dc='docker-compose'
alias dm='docker-machine'
```
Save the file, then execute it:
```
$ source ~/.bashrc
```
Test them out!

On Windows? You will first need to create a PowerShell Profile (if you don't already have one), and then you can add the aliases to it using Set-Alias—i.e., Set-Alias dc docker-compose.

### "Saved" State
Using Docker Machine for local development? Is the VM stuck in a "Saved" state?
```
$ docker-machine ls

NAME                                     ACTIVE   DRIVER       STATE     URL                        SWARM    DOCKER     ERRORS
microservice-architecture-flask-prod   *        amazonec2    Running   tcp://34.207.173.181:2376          v18.09.2
microservice-architecture-flask-dev       -        virtualbox   Saved                                        Unknown
```
First, try:
```
$ docker-machine start testdriven-dev
```
If that doesn't work, to break out of this, you'll need to power off the VM. For example, if you're using VirtualBox as your Hypervisor, you can:

1. Start virtualbox: virtualbox
2. Select the VM and click "start"
3. Exit the VM and select "Power off the machine"
4. Exit virtualbox
The VM should now have a "Stopped" state:
```
$ docker-machine ls

NAME                                  ACTIVE   DRIVER       STATE     URL                        SWARM   DOCKER     ERRORS
microservice-architecture-flask-prod   *        amazonec2    Running   tcp://34.207.173.181:2376          v18.09.2
microservice-architecture-flask-dev    -        virtualbox   Stopped
```
Now you can start the machine:
```
$ docker-machine start testdriven-dev
```
It should be "Running":
```
$ docker-machine ls

NAME                                  ACTIVE    DRIVER       STATE     URL                        SWARM   DOCKER     ERRORS
microservice-architecture-flask-prod   *        amazonec2    Running   tcp://34.207.173.181:2376          v18.09.2
microservice-architecture-flask-dev    -        virtualbox   Running   tcp://192.168.99.100:2376          v18.09.2
```
Restart the Machine and then start over:
```
$ docker-machine restart microservice-architecture-flask-dev
$ docker-machine env microservice-architecture-flask-dev
$ eval $(docker-machine env microservice-architecture-flask-dev)
$ docker-compose up -d --build
```

## Other commands
Stop the containers:
```
$ docker-compose stop
```
Run down the containers:
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
Reset Docker environment to localhost, unsetting all Docker environment variables:
```
$ eval $(docker-machine env -u)
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