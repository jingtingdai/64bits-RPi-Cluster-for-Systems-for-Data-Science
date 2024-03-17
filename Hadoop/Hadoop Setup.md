# Raspberry Pi Hadoop Cluster Installation Guide
We use the same static IP settings from RPiSetup section as in the table below.

|   Node        |    Hostname   | IP Address     |
| ------------- |:-------------:| :-------------:|
| master        | rpi0          | 192.168.1.114  |
| slave         | rpi1          | 192.168.1.115  |
| slave         | rpi2          | 192.168.1.116  |
| slave         | rpi3          | 192.168.1.117  |

## Set up Passwordless SSH
1. On each node, install OpenSSH Server
~~~bash
sudo apt install ssh pdsh openssh-server openssh-client
~~~
2. Generate SSH keys on each node. (Press enter to accept the default file location and press enter to leave the passphrase blank for no passphrase)
~~~bash
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
~~~
3. Copy the public key to every node include itself.
~~~bash
ssh-copy-id username@hostname # For example, pi@rpi0
~~~
4. Check if there is 4 public keys inside ~/.ssh/authorized_keys file and try to SSH into the target node.
~~~bash
ssh username@hostname
~~~

## Install Java

As of March 2024, Hadoop version 3.3 and upper only supports Java 8 and Java 11 (runtime only) according to the [Hadoop wiki](https://cwiki.apache.org/confluence/display/HADOOP/Hadoop+Java+Versions). However, the default JDK installed in Debian 12 Bookworm is JDK 17 as stated from the [Debian wiki](https://wiki.debian.org/Java). Therefore, we need to manually download and install Java 8 to ensure Hadoop operates correctly.

1. Download and install the 64-bit OpenJDK 8 from Debian archive.
~~~bash
wget http://ftp.us.debian.org/debian/pool/main/o/openjdk-8/openjdk-8-jdk-headless_8u402-ga-2+b1_arm64.deb
wget http://ftp.us.debian.org/debian/pool/main/o/openjdk-8/openjdk-8-jre-headless_8u402-ga-2+b1_arm64.deb

sudo dpkg -i *.deb
~~~
2. Set OpenJDK 8 as the default JAVA version. These commands show the list of all Java versions installed on your machine, set the one as default by entering the selection number.
~~~bash
sudo update-alternatives --config java
sudo update-alternatives --config javac
~~~
3. Verify the installation.
~~~bash
java -version
~~~

4. Set the the Java directory to environment variables. Add the path to the end of .bashrc file.
~~~bash
nano ~/.bashrc
export JAVA_HOME=/usr/lib/jvm/<java_directory>
export PATH=$PATH:$JAVA_HOME/bin
source ~/.bashrc
~~~

## Install Hadoop
1. Manually download 64-bit binary Hadoop 3.3.6 on each raspberry pi node.
~~~bash
wget https://dlcdn.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6-aarch64.tar.gz
~~~
2. Extract hadoop and move to target directory. (substitute <hadoop_archive_file>/ <hadoop_version_directory> with your own hadoop directory name)
~~~bash
tar -zxvf <hadoop_archive_file>.tar.gz
sudo mv <hadoop_version_directory> /opt/Hadoop
~~~
3. Set the environment variables.
~~~bash
nano ~/.bashrc
export HADOOP_HOME=/opt/Hadoop
export HADOOP_CONF_DIR=${HADOOP_HOME}/etc/hadoop
export PATH=$PATH:$HADOOP_HOME/bin
export PDSH_RCMD_TYPE=ssh
source ~/.bashrc
~~~
4. Verify the installation.
~~~bash
hadoop version
~~~

### Configure Hadoop in each node
Go to the configuration directory
~~~bash
cd $HADOOP_CONF_DIR
~~~ 

- hadoop-env.sh (make ‘logs’ directory in /opt/Hadoop)
~~~bash
export JAVA_HOME=/usr/lib/jvm/<java_directory>
export HADOOP_HOME=/opt/Hadoop
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
        <value>/opt/Hadoop/data/datanode</value>
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

### Prepare and boot HDFS and YARN
From the master node(rpi0), format the NameNode and start HDFS and YARN.

~~~bash
hdfs namenode -format
cd $HADOOP_HOME/sbin
./start-dfs.sh
./start-yarn.sh
~~~

To check if the configuration is correct, enter `jps` on the master node the following should be present:
- NameNode
- SecondayNameNode
- NodeManager
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