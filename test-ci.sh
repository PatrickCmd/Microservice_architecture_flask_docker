#!/bin/bash


env=$1
fails=""

inspect() {
    if [ $1 -ne 0 ]; then
        fails="${fails} $2"
    fi
}

# run client and server-side tests
dev() {
    # run unit and integration tests
    docker-compose up -d --build
    docker-compose exec users python manage.py test-cov
    inspect $? users
    docker-compose exec users black project
    docker-compose exec users flake8 --max-line-length=100 project
    inspect $? users-lint
    docker-compose exec client react-scripts test --coverage --watchAll=false
    inspect $? client
    docker-compose down
}

# run e2e tests
e2e(){
    docker-compose -f docker-compose-prod.yml up -d --build
    docker-compose -f docker-compose-prod.yml exec users python manage.py recreate_db
    docker-compose -f docker-compose-prod.yml exec users python manage.py seed_db
    ./node_modules/.bin/cypress run --config baseUrl=http://localhost
    inspect $? e2e
    docker-compose -f docker-compose-prod.yml down
}

# run appropriate tests
if [[ "${env}" == "devel" ]]; then
    echo "\n"
    echo "Running client and server-side tests!\n"
    dev
elif [[ "${env}" == "staging" ]]; then
    echo "\n"
    echo "Running e2e tests!\n"
    e2e stage
elif [[ "${env}" == "production" ]]; then
    echo "\n"
    echo "Running e2e tests!\n"
    e2e prod
else
    echo "\n"
    echo "Running all tests!\n"
    dev
fi

# return proper code
if [ -n "${fails}" ]; then
    echo "\n"
    echo "Tests failed: ${fails}"
    exit 1
else
    echo "\n"
    echo "Tests passed!"
    exit 0
fi
