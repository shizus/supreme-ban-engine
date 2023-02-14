# Gamer ban


## Pre-requisites
- virtualenv
- python3
- pip 19.0.3
- PostgreSQL

## Installation

```
virtualenv venv -p /location/to/python3
pip install -r requirements.txt
```

## Database environment variables

The following environment variables must be set up to let the app connect
a database. Default engine is PosgreSQL engine, default host is localhost and
default PORT is 5432.

```shell script
DB_ENGINE
DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT
```

## Running migrations

```
python manage.py migrate
```

# Running dev environment

```
python manage.py runserver
```

# Tests
```
python manage.py test
```

## Documentation
An online API documentation is available at:
http://127.0.0.1:8000/swagger/


## SECRET_KEY
The project has a default SECRET_KEY. Make sure to set it up for a production environment.

## ALLOWED_HOSTS
The project has a default ALLOWED_HOSTS. Make sure to set it up for a production environment.

## AWS environment variables

```shell script
$ export AWS_ACCESS_KEY_ID="YOUR_AWS_ACCESS_KEY_ID"
$ export AWS_SECRET_ACCESS_KEY="YOUR_AWS_SECRET_ACCESS_KEY"
```

## Docker

### Build the container
```shell script
docker build -t gamerban .
```

### Run the container

```
docker run \
    -p 8007:8000 \
    --name gamerban-run \
    gamerban \
    gunicorn gamerban.wsgi:application --bind 0.0.0.0:8000
```

### Stop the container

```shell script
docker stop gamerban-run
```

### Remove the container

```shell script
docker rm gamerban-run
```
