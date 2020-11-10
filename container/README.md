# Docker container

Go inside each lightbo.lt folder and build the container with ````docker build -t lightbo.lt:latest /opt/lightbo.lt/container/lightbo.lt-*````.

## lightbo.lt-db

lightbo.lt-db is the database container, based on MariaDB. Running on port 3306. Reachable on port 13306 from the host.

## lightbo.lt-base

lightbo.lt-base is the application container, with Python code. Running uwsgi on port 3000. Reachable on port 13000 from the host.

## Run everything

Once the containers are built, start them with ````docker-compose up -d````.

## PS: I will not explain how Docker works :-D

Nope!
