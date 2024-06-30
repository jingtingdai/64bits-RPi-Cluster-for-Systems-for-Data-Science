# Raspberry Pi Hadoop Cluster Installation Guide
We use the same static IP settings from RPiSetup section as in the table below.

|   Node        |    Hostname   | IP Address     |
| ------------- |:-------------:| :-------------:|
| master        | rpi0          | 192.168.1.114  |
| slave         | rpi1          | 192.168.1.115  |
| slave         | rpi2          | 192.168.1.116  |
| slave         | rpi3          | 192.168.1.117  |


## Install Java

As of March 2024, Hadoop version 3.3 and upper only supports Java 8 and Java 11 (runtime only) according to the [Hadoop wiki](https://cwiki.apache.org/confluence/display/HADOOP/Hadoop+Java+Versions). However, the default JDK installed in Debian 12 Bookworm is JDK 17 as stated from the [Debian wiki](https://wiki.debian.org/Java). Therefore, we need to manually download and install Java 8 to ensure Hadoop operates correctly.

1. transfer the file provided in the git repository to raspberry pi node, extract and move java to target directory.
~~~bash
tar -zxvf zulu8.78.0.19-ca-jdk8.0.412-linux_aarch64.tar.gz
sudo mkdir -p /usr/lib/jvm
sudo mv zulu8.78.0.19-ca-jdk8.0.412-linux_aarch64 /usr/lib/jvm/
~~~

2. Configure java.
~~~bash
sudo update-alternatives --install /usr/bin/java java /usr/lib/jvm/zulu8.78.0.19-ca-jdk8.0.412-linux_aarch64/bin/java 1
sudo update-alternatives --install /usr/bin/javac javac /usr/lib/jvm/zulu8.78.0.19-ca-jdk8.0.412-linux_aarch64/bin/javac 1 
~~~

3. Check if successfully installed.
~~~bash
java -version
~~~

4. Set the environment variables.
~~~bash
nano ~/.bashrc
export JAVA_HOME=/usr/lib/jvm/zulu8.78.0.19-ca-jdk8.0.412-linux_aarch64
export PATH=$PATH:$JAVA_HOME/bin
source ~/.bashrc
~~~

## Install Hadoop
1. Manually download Hadoop 3.3.6 64bit and transfer the file into each raspberry pi node.
~~~bash
wget https://dlcdn.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6-aarch64.tar.gz
~~~

2. Extract hadoop and move to target directory. 
~~~bash
tar -zxvf hadoop-3.3.6-aarch64.tar.gz
sudo mv hadoop-3.3.6 /opt/Hadoop
~~~

3. Set the environment variables.
~~~bash
nano ~/.bashrc
export HADOOP_HOME=/opt/Hadoop
export PATH=$PATH:$HADOOP_HOME/bin
export HADOOP_CONF_DIR=${HADOOP_HOME}/etc/hadoop
export PDSH_RCMD_TYPE=ssh
source ~/.bashrc
~~~

4. Check if successfully installed.
~~~bash
hadoop version
~~~

### Configure Hadoop in each node
Go to the configuration directory using ```cd $HADOOP_CONF_DIR```
- hadoop-env.sh (make ‘logs’ directory in /opt/Hadoop)
~~~bash
export JAVA_HOME=/usr/lib/jvm/zulu8.78.0.19-ca-jdk8.0.412-linux_aarch64
export HADOOP_HOME=/opt/Hadoop
export HADOOP_CONF_DIR=${HADOOP_HOME}/etc/hadoop
export HADOOP_LOG_DIR=${HADOOP_HOME}/logs 
~~~

- core-site.xml
~~~bash
  <property>
    <name>fs.defaultFS</name>
    <value>hdfs://rpi0:8020</value>
  </property>
~~~

- hdfs-site.xml
    - rpi0: make ‘data’ directory in /opt/Hadoop, make ‘namenode’, ‘secondarynamenode’ (include ‘checkpoint’ and ‘editlog’ directories) directories inside ‘data’.
    ~~~bash
      <property>
        <name>dfs.namenode.name.dir</name>
        <value>/opt/Hadoop/data/namenode</value>
      </property>
      <property>
        <name>dfs.namenode.rpc-bind-host</name>
        <value>0.0.0.0</value>
      </property>
      <property>
        <name>dfs.namenode.servicerpc-bind-host</name>
        <value>0.0.0.0</value>
      </property>
      <property>
        <name>dfs.namenode.http-bind-host</name>
        <value>0.0.0.0</value>
      </property>
      <property>
        <name>dfs.namenode.checkpoint.dir</name>
        <value>/opt/Hadoop/data/secondarynamenode/checkpoint</value>
      </property>
      <property>
        <name>dfs.namenode.checkpoint.edits.dir</name>
        <value>/opt/Hadoop/data/secondarynamenode/editlog</value>
      </property>
      <property>
        <name>dfs.namenode.rpc-address</name>
        <value>rpi0:8020</value>
      </property>
    ~~~

    - rpi1, rpi2, rpi3: make ‘data’ directory in /opt/Hadoop, make ‘datanode’ and ‘nodemanager’ directories in ‘data’.
    ~~~bash
      <property>
        <name>dfs.datanode.data.dir</name>
        <value>>/opt/Hadoop/data/datanode</value>
      </property>
      <property>
        <name>dfs.replication</name>
        <value>3</value>
      </property>
    ~~~

- yarn-site.xml

    - rpi0:  
    ~~~bash
      <property>
        <name>yarn.resourcemanager.hostname</name>
        <value>rpi0</value>
      </property>
      <property>
        <name>yarn.resourcemanager.webapp.address</name>
        <value>0.0.0.0:8088</value>
      </property>
      <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
      </property>
      <property>
        <name>yarn.nodemanager.aux-services.mapreduce_shuffle.class</name>
        <value>org.apache.hadoop.mapred.ShuffleHandler</value>
      </property>

    ~~~

    - rpi1,rpi2,rpi3: 
    ~~~bash
      <property>
        <name>yarn.resourcemanager.hostname</name>
        <value>rpi0</value>
      </property>
      <property>
        <name>yarn.resourcemanager.webapp.address</name>
        <value>0.0.0.0:8088</value>
      </property>
      <property>
        <name>yarn.nodemanager.local-dirs</name>
        <value>/opt/Hadoop/data/nodemanager</value>
      </property>
      <property>
        <name>yarn.nodemanager.log-dirs</name>
        <value>/opt/Hadoop/logs</value>
      </property>
      <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
      </property>
      <property>
        <name>yarn.nodemanager.aux-services.mapreduce_shuffle.class</name>
        <value>org.apache.hadoop.mapred.ShuffleHandler</value>
      </property>
    ~~~

- workers (only set in rpi0):
~~~bash
pi@rpi1
pi@rpi2
pi@rpi3
~~~

- mapred-site.xml:
~~~bash
  <property>
    <name>mapreduce.framework.name</name>
    <value>yarn</value>
  </property>
  <property>
    <name>mapreduce.jobhistory.address</name>
    <value>rpi0:10020</value>
  </property>
  <property>
    <name>mapreduce.jobhistory.webapp.address</name>
    <value>0.0.0.0:19888</value>
  </property>
  <property>
    <name>mapreduce.map.env</name>
    <value>HADOOP_MAPRED_HOME=${HADOOP_HOME}</value>
  </property>
  <property>
    <name>mapreduce.reduce.env</name>
    <value>HADOOP_MAPRED_HOME=${HADOOP_HOME}</value>
  </property>
  <property>
    <name>yarn.app.mapreduce.am.env</name>
    <value>HADOOP_MAPRED_HOME=${HADOOP_HOME}</value>
  </property>
~~~

### Change permission of hadoop directories
For all the nodes:
~~~bash
sudo chmod 777 -R /opt/Hadoop/
~~~

### change /etc/hosts in each node
change line '127.0.0.1   rpix' to:
~~~bash
    192.168.1.114	rpi0
    192.168.1.115	rpi1
    192.168.1.116	rpi2
    192.168.1.117	rpi3
~~~

### format the namenode in rpi0
~~~bash
hdfs namenode -format
~~~

### start Hadoop service in /opt/Hadoop/sbin of rpi0
~~~bash
./start-dfs.sh
./start-yarn.sh
~~~

To check if the configuration is correct, enter `jps` on the master node the following should be present:
- NameNode
- SecondayNameNode
- RessourceManager
- JPS

On the worker nodes, enter `jps` on the master node the following should be present:
- DataNode
- NodeManager
- JPS

A web interface is also available at http://rpi0:9870/

To stop the cluster from running, use
~~~bash
./stop-dfs.sh
./stop-yarn.sh
~~~

### If DataNodes are not running
If the NameNode undergoes reformatting multiple times, the DataNodes may fail to automatically update the new information from the reformatted NameNode. Consequently, the DataNodes are unable to establish a cluster connection with the NameNode and JPS or the web interface does not show any working DataNode.

Referring to this [stackoverflow answer](https://stackoverflow.com/a/44999865), by manually update new clusterID to the DataNodes, the problem can be solved.