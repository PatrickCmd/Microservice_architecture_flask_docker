# Microservice_architecture_flask_docker

docker-compose up -d --build (docker-compose build && docker-compose up -d)
docker-compose exec users-db psql -U postgres
docker-compose exec users python manage.py recreate_db
docker-compose exec users python manage.py seed_db
docker-compose exec users python manage.py test

docker-compose exec users python manage.py shell
docker-compose exec users python manage.py routes


## Production
docker-machine create --driver amazonec2 --amazonec2-open-port 8000 --amazonec2-region us-east-2 microservice-architecture-flask
docker-compose -f docker-compose-prod.yml exec users python manage.py seed_db
docker-compose -f docker-compose-prod.yml up -d --build
docker-compose -f docker-compose-prod.yml exec users python manage.py recreate_db
docker-compose -f docker-compose-prod.yml exec users env

docker-machine ip microservice-architecture-flask

docker-compose -f docker-compose-prod.yml up -d --build nginx

## Point docker-machine to active remote hoste
docker-machine env testdriven-prod
eval $(docker-machine env testdriven-prod)

## Point docker-machine back to localhost
eval $(docker-machine env -u)