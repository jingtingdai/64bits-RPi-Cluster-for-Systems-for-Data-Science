## ZOOKEEPER installation
1. download and install zookeeper in each node.
~~~bash
wget https://dlcdn.apache.org/zookeeper/zookeeper-3.8.4/apache-zookeeper-3.8.4-bin.tar.gz
tar -zxzf apache-zookeeper-3.8.4-bin.tar.gz
sudo mv apache-zookeeper-3.8.4-bin /opt/zookeeper
~~~

2. configuration.
    - zoo.cfg
    ~~~bash
    mkdir -p /opt/zookeeper/data
    
    cd /opt/zookeeper/conf
    cp zoo_sample.cfg zoo.cfg
    nano zoo.cfg
    dataDir=/opt/zookeeper/data
    clientPort=2181
    initLimit=10
    syncLimit=5
    tickTime=2000
    server.1=rpi0:2888:3888
    server.2=rpi1:2888:3888
    server.3=rpi2:2888:3888
    server.4=rpi3:2888:3888
    ~~~
    replace rpi0,rpi1,rpi2,rpi3 with 0.0.0.0 in each node (for example, 'server.1=0.0.0.0:2888:3888 server.2=rpi1:2888:3888 server.3=rpi2:2888:3888 server.4=rpi3:2888:3888' for rpi0)

    - myid
    ~~~bash
    echo "1" | sudo tee /opt/zookeeper/data/myid  
    ~~~
    use 1/2/3/4 for rpi0/1/2/3 

3. start zookeeper.
~~~bash
cd /opt/zookeeper/bin
./zkServer.sh start
./zkServer.sh status
~~~
