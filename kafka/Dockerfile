# Kafka and Zookeeper

FROM java:openjdk-8-jre

ENV DEBIAN_FRONTEND noninteractive
ENV SCALA_VERSION 2.11
ENV KAFKA_VERSION 0.10.2.1
ENV KAFKA_HOME /opt/kafka_"$SCALA_VERSION"-"$KAFKA_VERSION"

# Install Kafka, Zookeeper and other needed things
RUN apt-get update
RUN apt-get install -y zookeeper wget supervisor dnsutils
RUN rm -rf /var/lib/apt/lists/*
RUN apt-get clean
RUN wget -q http://apache.mirrors.spacedump.net/kafka/"$KAFKA_VERSION"/kafka_"$SCALA_VERSION"-"$KAFKA_VERSION".tgz -O /tmp/kafka_"$SCALA_VERSION"-"$KAFKA_VERSION".tgz 
RUN tar xfz /tmp/kafka_"$SCALA_VERSION"-"$KAFKA_VERSION".tgz -C /opt
RUN rm /tmp/kafka_"$SCALA_VERSION"-"$KAFKA_VERSION".tgz

ADD scripts/start-kafka.sh /usr/bin/start-kafka.sh
COPY ./requirements.txt /requirements.txt
COPY ./certcheck.py /certcheck.py
RUN apt-get update
RUN apt-get install python
RUN apt-get install -y python3-pip
RUN apt-get update && \
    apt-get -t jessie-backports install -y apache2-dev libssl-dev libffi-dev gcc postgresql-client libpq-dev python3 python3-dev python3-pip wget --no-install-recommends
RUN pip3 install psycopg2
RUN pip3 install -r /requirements.txt
ADD scripts/start-kafka.sh /usr/bin/start-kafka.sh


# Supervisor config
ADD supervisor/kafka.conf supervisor/zookeeper.conf /etc/supervisor/conf.d/

# 2181 is zookeeper, 9092 is kafka
EXPOSE 2181 9092

CMD ["supervisord", "-n"]


