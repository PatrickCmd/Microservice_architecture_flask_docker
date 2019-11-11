# Microservice_architecture_flask_docker

docker-compose up -d --build (docker-compose build && docker-compose up -d)
docker-compose exec users-db psql -U postgres
docker-compose exec users python manage.py recreate_db
docker-compose exec users python manage.py seed_db
docker-compose exec users python manage.py test

docker-compose exec users python manage.py shell
docker-compose exec users python manage.py routes
