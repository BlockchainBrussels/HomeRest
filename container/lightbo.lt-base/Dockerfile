FROM ubuntu:20.04
#Install python and other programs required to run our app
RUN DEBIAN_FRONTEND=noninteractive TZ=Europe/Brussels apt-get update && \
    DEBIAN_FRONTEND=noninteractive TZ=Europe/Brussels apt-get -y upgrade && \
    DEBIAN_FRONTEND=noninteractive TZ=Europe/Brussels apt-get -y install apt-utils && \
    DEBIAN_FRONTEND=noninteractive TZ=Europe/Brussels apt-get -y install git python3 python3-pip wait-for-it vim net-tools && \
    pip3 install --upgrade pip setuptools && \
    pip3 install --upgrade wheel && \
    pip3 install --upgrade flask-ext flask-mysql flask-basicauth && \
    pip3 install --upgrade uwsgi && \
    pip3 install --upgrade APScheduler && \
    touch /tmp/aha2
