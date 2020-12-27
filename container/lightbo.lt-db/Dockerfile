FROM mariadb:10.5
ADD ./homerest.sql /docker-entrypoint-initdb.d/
RUN touch /tmp/aha1
#Expose port 90 of the container to the outside
EXPOSE 3306
