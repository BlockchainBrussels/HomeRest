FROM linoxbe/lightbo.lt-base:latest
#Copy our files to the container
RUN cd /opt && \
    git clone https://github.com/BlockchainBrussels/LIGHTBO.LT.git && \
    mv /opt/LIGHTBO.LT /opt/lightbo.lt && \
    chmod a+x /opt/lightbo.lt/container/lightbo.lt-base/create_files.sh && \
    /opt/lightbo.lt/container/lightbo.lt-base/create_files.sh && \
    chown -R www-data.www-data /opt/lightbo.lt && \
    mkdir -p /var/log/uwsgi/ && \
    mkdir -p /run/uwsgi/
#Change the working directory
WORKDIR /opt/lightbo.lt/server
#Run uwsgi with the configuration in the .ini file
#CMD /usr/local/bin/uwsgi --emperor /opt/lightbo.lt/uwsgi/sites/ --uid=www-data --gid=www-data
CMD [ "uwsgi", "--http", "0.0.0.0:3000", \
               "--uid", "www-data", \
               "--gid", "www-data", \
               "--protocol", "uwsgi", \
               "--wsgi", "wsgi:application", \
               "--ini", "/opt/lightbo.lt/uwsgi/sites/app.ini" ]

#Expose port 90 of the container to the outside
EXPOSE 3000
