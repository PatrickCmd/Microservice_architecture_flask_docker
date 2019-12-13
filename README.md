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

# AWS(ECS)
## What is Container Orchestration?
As you move from deploying containers on a single machine to deploying them across a number of machines, you will need an orchestration tool to manage the arrangement and coordination of the containers across the entire system. This is where ECS fits in along with a number of other orchestration tools, like [Kubernetes](https://kubernetes.io/), [Mesos](https://mesos.apache.org/), and [Docker Swarm](https://docs.docker.com/engine/swarm/).

![kubernetes vs docker swarm vs mesos](https://testdriven.io/static/images/courses/microservices/05_kubernetes-vs-docker-swarm-vs-mesos.png)

## Why ECS?
ECS is simpler to set up and easier to use and you have the full power of AWS behind it, so you can easily integrate it into other AWS services (which we will be doing shortly). In short, you get scheduling, service discovery, load balancing, and auto-scaling out-of-the-box. Plus, you can take full advantage of EC2's multiple availability-zones.

If you're already on AWS and have no desire to leave, then it makes sense to use AWS.

Keep in mind, that ECS is often lagging behind Kubernetes, in terms of features, though. If you're looking for the most features and portability and you don't mind installing and managing the tool, then Kubernetes, Docker Swarm, or Mesos may be right for you.

One last thing to take note of is that since ECS is closed-source, there isn't a true way to run an environment locally in order to achieve development-to-production parity.

> For more, review the [Choosing the Right Containerization and Cluster Management Tool](https://blog.kublr.com/choosing-the-right-containerization-and-cluster-management-tool-fdfcec5700df) blog post.

## Orchestration Feature Wish-List
Most orchestration tools come with a core set of features. You can find those features below along with the associated AWS service...

|Feature|Info|AWS Service |
|-------|:--|:-----------|
|Health checks |Verify when a task is ready to accept traffic |ALB
|Path-based routing |Forward requests based on the URL path |ALB
|Dynamic port-mapping |Assign ports dynamically when a new container is spun up |ALB
|Zero-downtime deployments |Deployments do not disrupt the users |ALB
|Service discovery |Automatic detection of new containers and services |ALB, ECS
|High availability |Containers are evenly distributed across Availability Zones	|ECS
|Auto scaling |Scaling resources up or down automatically based on fluctuations in traffic patterns or metrics (like CPU usage)	  |ECS
|Provisioning |New containers should select hosts based on resources and configuration |ECS
|Container storage |Private image storage and management  |ECR
|Container logs |Centralized storage of container logs |CloudWatch
|Monitoring |Ability to monitor basic stats like CPU usage, memory, I/O, and network usage as well as set alarms and create events |CloudWatch
|Secrets management |Sensitive info should be encrypted and stored in a centralized store |Parameter Store, KMS, IAM
Review the [Getting Started with Amazon ECS guide](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ECS_GetStarted.html).

# IAM
IAM is used to manage access to AWS services:

- WHO is trying to access (authentication)
- WHICH service are they trying to access (authorization)
- WHAT are they trying to do (authorization)
> Review the [Understanding How IAM Works guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/intro-structure.html).

Although not required, it's a good idea to set up another new IAM User and Role specifically for container instances and set up Multi Factor Authentication (MFA) for this new account along with the root account. For more, review the [Create an IAM User](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/get-set-up-for-amazon-ecs.html#create-an-iam-user) and Using [Multi-Factor Authentication (MFA) in AWS](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa.html) guides, respectively.

# Elastic Container Registry
## Image Registry
A container image registry is used to store and distribute container images. [Docker Hub](https://docs.docker.com/docker-hub/) is one of the more popular image registry services for public images—basically GitHub for Docker images.

> Review the following Stack Overflow [article](https://stackoverflow.com/a/34004418/1799408) for more info on Docker Hub and image registries in general.

## ECR
Why [Elastic Container Registry](https://aws.amazon.com/ecr/)?

1. We do not want to add any sensitive info to the images on Docker Hub since they are publicly available
2. ECR plays nice with the [Elastic Container Service](https://aws.amazon.com/ecs/) (which we'll be setting up shortly)

Navigate to [Amazon ECS](https://console.aws.amazon.com/ecs), click "Repositories", and then add four new repositories:

1. test-driven-users
2. test-driven-users_db
3. test-driven-client
4. test-driven-swagger
> Why only four images? We’ll use the [Application Load Balancer](https://aws.amazon.com/elasticloadbalancing/features/#Details_for_Elastic_Load_Balancing_Products) instead of Nginx in our stack so we won’t need that image or container.

You can also create a new repository with the [AWS CLI](https://docs.aws.amazon.com/AmazonECR/latest/userguide/ECR_AWSCLI.html#AWSCLI_create_repository):
```
$ aws ecr create-repository --repository-name REPOSITORY_NAME --region us-east-2
```
So, if the branch is either staging or production and it's not a pull request, we download the AWS CLI, log in to AWS, and then set the appropriate TAG and REPO.

Grab your AWS credentials from the ~/.aws/credentials file:
```
$ cat ~/.aws/credentials
```
Set them as environment variables within the Repository Settings of your testdriven-app on Travis:

1. AWS_ACCOUNT_ID - YOUR_ACCOUNT_ID
2. AWS_ACCESS_KEY_ID - YOUR_ACCCES_KEY_ID
3. AWS_SECRET_ACCESS_KEY - YOUR_SECRET_ACCESS_KEY


In .travis.yml do you notice the COMMIT variable?
```
COMMIT=${TRAVIS_COMMIT::8}
```
This sets a new environment variable, which contains the first 8 characters of the git commit hash. We not only have a unique name with the image, we can now tie it back to a commit in case we need to troubleshoot the code in the image.