## KAFKA installation
1. download and install kafka in each node.
~~~bash
wget https://downloads.apache.org/kafka/3.7.0/kafka_2.13-3.7.0.tgz
tar -zxvf kafka_2.13-3.7.0.tgz
sudo mv kafka_2.13-3.7.0 /opt/kafka
~~~

2. configuration in each node.
    - zookeeper.properties
    ~~~bash
    cd /opt/kafka/config
    nano zookeeper.properties
    dataDir=/opt/zookeeper/data
    ~~~

    - server.properties
    ~~~bash
    nano server.properties
    broker.id=1
    ~~~
    set broker.id=1 for rpi0, use 2/3/4 for rpi1/2/3

3. start kafka in each node.
~~~bash
cd /opt/kafka/bin
./zookeeper-server-start.sh -daemon /opt/kafka/config/zookeeper.properties
./kafka-server-start.sh -daemon /opt/kafka/config/server.properties
~~~