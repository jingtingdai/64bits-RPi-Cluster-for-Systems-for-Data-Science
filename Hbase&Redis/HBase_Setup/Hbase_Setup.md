## HBASE installation
1. download and extract hbase in all the nodes.
~~~bash
wget https://dlcdn.apache.org/hbase/2.6.0/hbase-2.6.0-hadoop3-bin.tar.gz
tar -zxvf hbase-2.6.0-hadoop3-bin.tar.gz
sudo mv hbase-2.6.0-hadoop3 /opt/hbase
~~~

2. configuration in rpi0.
- hbase-site.xml (delete all the old properties in the file)
~~~bash
hdfs dfs -mkdir /hbase
cd /opt/hbase/conf
nano hbase-site.xml
<configuration>
  <property>
    <name>hbase.rootdir</name>
    <value>hdfs://rpi0:8020/hbase</value>
  </property>
  <property>
    <name>hbase.cluster.distributed</name>
    <value>true</value>
  </property>
  <property>
    <name>hbase.zookeeper.quorum</name>
    <value>rpi0,rpi1,rpi2,rpi3</value>
  </property>
  <property>
    <name>hbase.zookeeper.property.clientPort</name>
    <value>2181</value>
  </property>
</configuration>
~~~
copy hbase-site.xml to all worker nodes.

Also add these properties to hbase-site.xml in rpi0:
```
  <property>
    <name>hbase.master.ha.automatic.recovery</name>
    <value>true</value>
  </property>
  <property>
    <name>hbase.master.port</name>
    <value>16000</value>
  </property>
  <property>
    <name>hbase.master.info.port</name>
    <value>16010</value>
  </property>
  <property>
    <name>hbase.wal.provider</name>
    <value>filesystem</value>
  </property>
```

- regionservers
~~~bash
nano regionservers
pi@rpi1
pi@rpi2
pi@rpi3
~~~

- hbase-env.sh (also need to be configured in rpi1/2/3)
~~~bash
nano hbase-env.sh
export JAVA_HOME=/usr/lib/jvm/zulu8.78.0.19-ca-jdk8.0.412-linux_aarch64
export HADOOP_HOME=/opt/Hadoop
export HBASE_CLASSPATH=/opt/Hadoop/etc/hadoop
export HBASE_MANAGES_ZK=false
~~~

- Set environment variables (also need to be configured in rpi1/2/3)
~~~bash
nano ~/.bashrc
export HBASE_HOME=/opt/hbase
export PATH=$PATH:$HBASE_HOME/bin
source ~/.bashrc
~~~

- Substitute all the jar package start with 'hadoop' in /opt/hbase/lib with the corresponding one which is in different version in /opt/Hadoop and also substitute all the jar package start with 'zookeeper' with those in /opt/zookeeper/lib in all the nodes. For package that cannot find substitute in /opt/Hadoop, leave the original package untouched. This is to avoid SLF4J warning about multiple bindings, where more than one SLF4J implementation is in the classpath, leading to ambiguity about which logging framework to use. It can cause unexpected logging behavior but is usually not critical.

- copy hdfs-site.xml in /opt/Hadoop/etc/hadoop to /opt/hbase/conf in all the nodes.

3. start hbase. Remember to start zookeeper before start hbase. (start zookeeper in all the nodes and start hbase in rpi0)
~~~bash
cd /opt/zookeeper/bin
./zkServer.sh start

cd /opt/hbase/bin
./start-hbase.sh
~~~

To check if the configuration is correct, enter `jps` on the master node the following should be present:
- NameNode
- SecondayNameNode
- RessourceManager
- JPS
- HMaster

On the worker nodes, enter `jps` on the master node the following should be present:
- DataNode
- NodeManager
- JPS
- HRegionServer
