## ZOOKEEPER installation
1. Download and install zookeeper in each node.
~~~bash
wget https://dlcdn.apache.org/zookeeper/zookeeper-3.8.4/apache-zookeeper-3.8.4-bin.tar.gz
tar -zxzf apache-zookeeper-3.8.4-bin.tar.gz
mv apache-zookeeper-3.8.4-bin /opt/zookeeper
mkdir -p /opt/zookeeper/data
~~~

2. Make sure /etc/hosts in each node contains information below:
~~~bash
    192.168.1.114	rpi0
    192.168.1.115	rpi1
    192.168.1.116	rpi2
    192.168.1.117	rpi3
~~~

3. Configure ZooKeeper by editing the conf/zoo.cfg file, an create server ID in the folder we just created.
    - zoo.cfg
    ~~~bash
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

    - myid
    ~~~bash
    echo "1" | sudo tee /opt/zookeeper/data/myid  
    ~~~
    use 1/2/3/4 for rpi0/1/2/3 

4. Start zookeeper and check the status.
~~~bash
cd /opt/zookeeper/bin
./zkServer.sh start
./zkServer.sh status
~~~
It will show Mode: leader or Mode: follower if it's running properly.

5. Remember to stop Zookeeper after finishing the exercises.
~~~bash
./zkServer.sh stop
~~~