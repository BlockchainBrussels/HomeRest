# Docker container

Go inside each lightbo.lt folder and build the container with ````docker build -t linoxbe/lightbo.lt-CNT:latest /opt/lightbo.lt/container/lightbo.lt-CNT````.

## lightbo.lt-db

lightbo.lt-db is the database container, based on MariaDB. Running on port 3306. Reachable on port 13306 from the host.

## ligthbo.lt-base

lightbo.lt-base is the base container, with Python, but without the Python code.

## lightbo.lt-app

lihtbo.lt-app is the application container, base on lightbo.lt-base, adding the Python code to lightbo.lt-base.
Running uwsgi on port 3000. Reachable on port 13000 from the host.

## Run everything

Once the containers are built, start them with ````docker-compose up -d````.

## PS: I will not explain how Docker works :-D

Nope!
