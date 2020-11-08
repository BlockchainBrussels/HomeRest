FROM ubuntu:20.04
#Install python and other programs required to run our app
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive TZ=Europe/Brussels apt-get -y install git python3 python3-pip && \
    pip3 install --upgrade pip setuptools && \
    pip3 install --upgrade wheel && \
    pip3 install --upgrade flask-ext flask-mysql flask-basicauth && \
    pip3 install --upgrade uwsgi
#Copy our files to the container
RUN cd /opt && \
    git clone https://github.com/BlockchainBrussels/LIGHTBO.LT.git && \
    mv /opt/LIGHTBO.LT /opt/lightbo.lt && \
    chmod a+x /opt/lightbo.lt/container/create_files.sh && \
    /opt/lightbo.lt/container/create_files.sh && \
    chown -R www-data.www-data /opt/lightbo.lt
#Change the working directory
WORKDIR /opt/lightbo.lt/server
#Run uwsgi with the configuration in the .ini file
#CMD /usr/local/bin/uwsgi --emperor /opt/lightbo.lt/uwsgi/sites/ --uid=www-data --gid=www-data
CMD [ "uwsgi", "--socket", "0.0.0.0:3000", \
               "--uid", "www-data", \
               "--gid", "www-data", \
               "--protocol", "uwsgi", \
               "--wsgi", "wsgi:application" ]
#Expose port 90 of the container to the outside
EXPOSE 3000
