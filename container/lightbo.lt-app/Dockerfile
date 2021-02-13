FROM linoxbe/lightbo.lt-base:latest
#Copy our files to the container
RUN cd /opt && \
    git clone https://github.com/BlockchainBrussels/LIGHTBO.LT.git && \
    mv /opt/LIGHTBO.LT /opt/lightbo.lt && \
    chown -R www-data.www-data /opt/lightbo.lt && \
    mkdir -p /var/log/uwsgi/ && \
    mkdir -p /run/uwsgi/ && \
    chown www-data.www-data /var/log/uwsgi/ && \
    chown www-data.www-data /run/uwsgi/ && \
    cp /opt/lightbo.lt/nginx/default /etc/nginx/sites-available/ && \
    mkdir -p /var/log/supervisor/ && \
    chown www-data.www-data /var/log/supervisor/ && \
    touch /tmp/aha12
#Change the working directory
WORKDIR /opt/lightbo.lt/server
#Run uwsgi with the configuration in the .ini file
CMD  /usr/bin/supervisord --configuration=/opt/lightbo.lt/supervisor/supervisord.conf

#Expose port 90 of the container to the outside
EXPOSE 3000
