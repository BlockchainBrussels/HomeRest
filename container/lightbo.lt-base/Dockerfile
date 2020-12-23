FROM ubuntu:20.04
#Install python and other programs required to run our app
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive TZ=Europe/Brussels apt-get -y install git python3 python3-pip wait-for-it logrotate vim apt-utils && \
    pip3 install --upgrade pip setuptools && \
    pip3 install --upgrade wheel && \
    pip3 install --upgrade flask-ext flask-mysql flask-basicauth && \
    pip3 install --upgrade uwsgi
