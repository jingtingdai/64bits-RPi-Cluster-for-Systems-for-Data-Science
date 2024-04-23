## HBASE installation
1. download and extract hbase in all the nodes.
~~~bash
wget https://dlcdn.apache.org/hbase/2.5.8/hbase-2.5.8-hadoop3-bin.tar.gz
tar -zxvf hbase-2.5.8-hadoop3-bin.tar.gz
sudo mv hbase-2.5.8-hadoop3 /opt/hbase
~~~

2. configuration in rpi0.
- hbase-site.xml
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
export JAVA_HOME=/usr/lib/jvm/jdk-11.0.21+9
export HADOOP_HOME=/opt/Hadoop
export HBASE_CLASSPATH=/opt/Hadoop/etc/hadoop
export HBASE_MANAGES_ZK=false
~~~

- set environment variables (also need to be configured in rpi1/2/3)
~~~bash
nano ~/.bashrc
export HBASE_HOME=/opt/hbase
export PATH=$PATH:$HBASE_HOME/bin
source ~/.bashrc
~~~

- substitute all the jar package start with 'hadoop' in /opt/hbase/lib with the corresponding one which is in different version in /opt/Hadoop.

3. start hbase. Remember to start zookeeper before start hbase.
~~~bash
cd /opt/hbase/bin
./start-hbase.sh
~~~
can check if successfully start via command `jps`.
