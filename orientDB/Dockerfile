FROM openjdk:8-jdk

ENV ORIENTDB_VERSION 3.2.8
ENV ORIENTDB_ROOT_PASSWORD 0000
RUN mkdir /orientdb
COPY orientdb-community-$ORIENTDB_VERSION.zip .
RUN unzip orientdb-community-$ORIENTDB_VERSION.zip -d /orientdb
RUN rm orientdb-community-$ORIENTDB_VERSION.zip
RUN rm -rf /orientdb/databases/*

ENV PATH /orientdb/bin:$PATH
ADD databases /orientdb/databases
ADD config /orientdb/config
VOLUME ["/orientdb/backup", "/orientdb/databases", "/orientdb/config"]
WORKDIR /orientdb
RUN printenv PATH
#OrientDb binary
EXPOSE 2424
#OrientDb http
EXPOSE 2480
# Default command start the server
RUN chmod +x bin/server.sh
CMD ["bin/server.sh"]