## Basic Installation

### OS installation
 Download the Raspberry Pi Imager from the Raspberry Pi website and use it to flash the Raspberry Pi OS onto each microSD card while set all of the username to be 'pi' and set the hostname as 'rpi0'/'rpi1'/'rpi2'/'rpi3' seperately.

### static IP address set up
on each node:
~~~bash
sudo nmcli c show
sudo nmcli c mod 'Wired connection 1' ipv4.addresses 192.168.1.11x/24 ipv4.method manual
sudo nmcli con mod 'Wired connection 1' ipv4.gateway 192.168.1.1
sudo nmcli con mod 'Wired connection 1' ipv4.dns "192.168.1.1"
sudo nmcli c down 'Wired connection 1' && sudo nmcli c up 'Wired connection 1'
~~~
1. substitute 'Wired connection 1' with the internet connection name you used
2. substitute '192.168.1.11x' with:
    - '192.168.1.114' for rpi0
    - '192.168.1.115' for rpi1
    - '192.168.1.116' for rpi2
    - '192.168.1.117' for rpi3

### set up passwordless SSH among the rpi nodes
1. Generate SSH keys on each node. (Press enter to accept the default file location and press enter to leave the passphrase blank for no passphrase)
~~~bash
ssh-keygen -t rsa
~~~
2. Copy the public key to every node include itself.
~~~bash
ssh-copy-id pi@hostname
~~~
3. Check if there is 4 public keys inside ~/.ssh/authorized_keys file and try to SSH into the target node.
~~~bash
ssh pi@hostname
~~~

## HADOOP installation

### JAVA installation
1. Manually download Java 64bit the latest version and transfer the file into each raspberry pi node.
2. Extract java and move to target directory. (substitute <java_archive_file>/ <java_version_directory> with your own java directory name)
~~~bash
tar -zxvf <java_archive_file>.tar.gz
sudo mkdir -p /usr/lib/jvm
sudo mv <java_version_directory> /usr/lib/jvm/
~~~
3. Set the environment variables. (substitute <java_directory> with your own java directory name)
~~~bash
sudo update-alternatives --install /usr/bin/java java /usr/lib/jvm/<java_directory>/bin/java 1
sudo update-alternatives --install /usr/bin/javac javac /usr/lib/jvm/<java_directory>/bin/javac 1
sudo update-alternatives --config java 
nano ~/.bashrc
export JAVA_HOME=/usr/lib/jvm/<java_ directory>
export PATH=$PATH:$JAVA_HOME/bin
source ~/.bashrc
~~~
4. Check if successfully installed.
~~~bash
java -version
~~~

### Hadoop installation
1. Manually download Hadoop 3.3.6 64bit and transfer the file into each raspberry pi node.
2. Extract hadoop and move to target directory. (substitute <hadoop_archive_file>/ <hadoop_version_directory> with your own hadoop directory name)
~~~bash
tar -zxvf <hadoop_archive_file>.tar.gz
sudo mv <hadoop_version_directory> /opt/Hadoop
~~~
3. Set the environment variables.
~~~bash
nano ~/.bashrc
export HADOOP_HOME=/opt/Hadoop
export PATH=$PATH:$HADOOP_HOME/bin
source ~/.bashrc
~~~
4. Check if successfully installed.
~~~bash
hadoop version
~~~

### Configure Hadoop in each node
Typically, one machine(rpi0) in the cluster is designated as the NameNode and the ResourceManager. This is masters. Other services like MapReduce Job History Server (rpi0) are usually run either on dedicated hardware or on shared infrastructure. The rest of the machine in the cluster act as both DataNode and NodeManager. Configure the cluster through files in /opt/Hadoop/etc/hadoop.


- hadoop-env.sh (make ‘logs’ directory in /opt/Hadoop)
~~~bash
export JAVA_HOME=/usr/lib/jvm/<java_directory>
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

### change the permission of hadoop directories
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

If sucessfully start hdfs, can check in each node use command 'jps' or check in http://rpi0:9870/.

### HDFS 
make new directory in HDFS:
~~~bash
hdfs dfs -mkdir /directory
~~~
check content in HDFS:
~~~bash
hdfs dfs -ls /
~~~
put file into HDFS:
~~~bash
hadoop fs -copyFromLocal /local/path/to/example.txt /hdfs/path/where/to/save/
~~~
kill a datanode (get PID using command 'jps'):
~~~bash
kill -9 PID
~~~

## SPARK installation
1. download and install in all the nodes:
~~~bash
wget https://archive.apache.org/dist/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz
tar -zxvf spark-3.5.0-bin-hadoop3.tgz
sudo mv spark-3.5.0-bin-hadoop3 /opt/spark
~~~

2. set environment variables in all the nodes:
~~~bash
nano ~/.bashrc
export SPARK_HOME=/opt/spark
export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
export PYSPARK_PYTHON=python3
source ~/.bashrc
~~~

3. configuration only in rpi0:
    - spark-defaults.conf
    ~~~bash
    cd /opt/spark/conf
    cp spark-defaults.conf.template spark-defaults.conf
    sudo nano spark-defaults.conf
    spark.master                     spark://rpi0:7077
    spark.eventLog.enabled           true
    spark.eventLog.dir               hdfs://rpi0:8020/sparkEventLog
    spark.serializer                 org.apache.spark.serializer.KryoSerializer
    hdfs dfs -mkdir /sparkEventLog
    ~~~

    - spark-env.sh
    ~~~bash
    cp spark-env.sh.template spark-env.sh
    sudo nano spark-env.sh
    export SPARK_MASTER_HOST=rpi0
    export JAVA_HOME=/usr/lib/jvm/jdk-11.0.21+9
    ~~~

    - workers
    ~~~bash
    cp workers.template workers
    sudo nano workers
    pi@rpi1
    pi@rpi2
    pi@rpi3
    ~~~

4. start SPARK.
    - in rpi0:
    ~~~bash
    start-master.sh
    ~~~
    - in worker nodes:
    ~~~bash
    start-worker.sh spark://rpi0:7077
    ~~~
    Can check spark in http://rpi0:8080.

5. can run a simply python script to test spark.
~~~bash
pyspark --master spark://rpi0:7077
~~~
~~~python
rdd = sc.parallelize([1,2,3,4,5])
rdd.reduce(lambda a, b: a+b)
~~~

6. installing JupyterLab in rpi0
- install it in an isolated environment:
~~~bash
sudo apt-get update
sudo apt-get upgrade -y
python3 -m venv myjupyterenv
source myjupyterenv/bin/activate
pip install jupyterlab
~~~
-configure PySpark to work with JupyterLab:
~~~bash
nano ~/.bashrc
export PYSPARK_DRIVER_PYTHON=jupyter
export PYSPARK_DRIVER_PYTHON_OPTS='lab'
source ~/.bashrc
~~~
-start JupyterLab.
~~~bash
source myjupyterenv/bin/activate
jupyter lab --ip=192.168.1.114
~~~
and then you would get an URL which you can use to open the JupyterLab.



## HIVE installation
1. download and install in all the nodes:
~~~bash
wget https://dlcdn.apache.org/hive/hive-4.0.0-beta-1/apache-hive-4.0.0-beta-1-bin.tar.gz
tar -zxvf apache-hive-4.0.0-beta-1-bin.tar.gz
sudo mv apache-hive-4.0.0-beta-1-bin /opt/hive
~~~

2. set environment variables in all the nodes:
~~~bash
nano ~/.bashrc
export HIVE_HOME=/opt/hive
export HIVE_CONF_DIR=/opt/hive/conf
export PATH=$PATH:$HIVE_HOME/bin
source ~/.bashrc
~~~

3. install PostgreSQL.
    1. install PostgreSQL in rpi0
    ~~~bash
    sudo apt update
    sudo apt install postgresql postgresql-contrib -y
    sudo systemctl enable postgresql
    sudo systemctl start postgresql
    ~~~

    2. secure the user named ‘postgres’ :
    ~~~bash
    sudo -i -u postgres
    psql
    \password postgres
    ~~~
    Repeat input password twice: 12345
    ~~~bash
    \q
    exit
    ~~~

    3. configure PostgreSQL to allow remote connections from the other nodes:
    ~~~bash
    sudo nano /etc/postgresql/15/main/postgresql.conf
    ~~~
    change the line ‘#listen_addresses = 'localhost'’ to:
    ~~~bash
    listen_addresses = '*'
    ~~~
    ~~~bash
    sudo nano /etc/postgresql/15/main/pg_hba.conf
    ~~~
    add the line in the end of the file: 
    ~~~bash
    host    all             all             0.0.0.0/0               md5
    ~~~
    restart:
    ~~~bash
    sudo systemctl restart postgresql
    ~~~

    4. install PostgreSQL client version in each worker node and connect to postgresql server:
    ~~~bash
    sudo apt update
    sudo apt-get install postgresql-client
    psql -h rpi0 -U postgres -d postgres
    ~~~

    5. prepare the PostgreSQL database:
    ~~~bash
    sudo -i -u postgres
    psql
    CREATE DATABASE hive_metastore;
    CREATE USER hiveuser WITH PASSWORD '12345';
    GRANT ALL PRIVILEGES ON DATABASE hive_metastore TO hiveuser;
    \q
    exit
    ~~~

    6. download PostgreSQL JDBC driver and put in hive lib directory:
    ~~~bash
    wget https://jdbc.postgresql.org/download/postgresql-42.7.2.jar
    mv postgresql-42.7.2.jar /opt/hive/lib
    ~~~

4. create data warehouse on HDFS
~~~bash
hdfs dfs -mkdir -p /user/hive/warehouse
hdfs dfs -chmod g+w /user/hive/warehouse
hdfs dfs -mkdir -p /tmp
hdfs dfs -chmod g+w /tmp
~~~

5. Lib guava - conflict issue
~~~bash
$ rm /opt/hive/lib/guava-22.0.jar
$ cp /opt/Hadoop/share/hadoop/common/lib/guava-27.0-jre.jar /opt/hive/lib/
cp /opt/hive/conf/hive-env.sh.template  /opt/hive/conf/hive-env.sh
~~~

6. configure hive to use postgresql:
- hive-site.xml
~~~bash
cd /opt/hive/conf
touch hive-site.xml
sudo nano hive-site.xml
<configuration>
  <property>
    <name>javax.jdo.option.ConnectionURL</name>
    <value>jdbc:postgresql://rpi0:5432/hive_metastore</value>
  </property>
  <property>
    <name>javax.jdo.option.ConnectionDriverName</name>
    <value>org.postgresql.Driver</value>
  </property>
  <property>
    <name>javax.jdo.option.ConnectionUserName</name>
    <value>hiveuser</value>
  </property>
  <property>
    <name>javax.jdo.option.ConnectionPassword</name>
    <value>12345</value>
  </property>
  <property>
    <name>datanucleus.autoCreateSchema</name>
    <value>false</value>
	</property>
	<property>
		<name>datanucleus.fixedDatastore</name>
		<value>true</value>
	</property>
	<property>
		<name>datanucleus.autoStartMechanism</name> 
		<value>SchemaTable</value>
	</property> 
	<property>
		<name>hive.metastore.event.db.notification.api.auth</name>
		<value>false</value>
	</property>
  <property>
		<name>hive.metastore.uris</name>
		<value>thrift://rpi0:9083</value>
	</property>
	<property>
		<name>hive.server2.authentication</name>
		<value>NONE</value>
	</property>
  <property>
    <name>hive.server2.enable.doAs</name>
    <value>false</value>
  </property>
</configuration>
~~~

- hive-env.sh
~~~bash
export HADOOP_HOME=/opt/Hadoop
export HIVE_HOME=/opt/hive
export HIVE_CONF_DIR=$HIVE_HOME/conf
~~~

- core-site.xml in /opt/Hadoop/etc/hadoop, add following config (substitute 'pi' with your local user):
~~~bash
  <property>
		<name>hadoop.proxyuser.pi.hosts</name>
		<value>*</value>
	</property>
	<property>
		<name>hadoop.proxyuser.pi.groups</name>
		<value>*</value>
	</property>
~~~

7. Configure schema init permission:
~~~bash
sudo -i -u postgres
psql -U postgres -d hive_metastore
GRANT USAGE ON SCHEMA public TO hiveuser;
GRANT CREATE ON SCHEMA public TO hiveuser;
GRANT ALL PRIVILEGES ON SCHEMA public TO hiveuser;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO hiveuser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO hiveuser;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO hiveuser;
~~~

8. start hive.
~~~bash
schematool -dbType postgres -initSchema
nohup hive --service metastore &
nohup hive --service hiveserver2 &
beeline
!connect jdbc:hive2://rpi0:10000/default
~~~
enter skip input username and password.

9. can try hive with following command in postgresql:
~~~sql
SHOW DATABASES;
~~~
or try check in http://rpi0:10002/.

## ZOOKEEPER installation
1. download and install zookeeper in each node.
~~~bash
wget https://dlcdn.apache.org/zookeeper/zookeeper-3.8.3/apache-zookeeper-3.8.3-bin.tar.gz
tar -zxzf apache-zookeeper-3.8.3-bin.tar.gz
sudo mv apache-zookeeper-3.8.3-bin /opt/zookeeper
~~~

2. configuration.
    - zoo.cfg
    ~~~bash
    sudo mkdir -p /opt/zookeeper/data
    cd /opt/zookeeper/conf
    cp zoo_sample.cfg zoo.cfg
    nano zoo.cfg
    dataDir=/opt/zookeeper/data
    #clientPort=2181
    #initLimit=5
    #syncLimit=2
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

3. start zookeeper.
~~~bash
cd /opt/zookeeper/bin
./zkServer.sh start
./zkServer.sh status
~~~


## HBASE installation
1. download and extract hbase in all the nodes.
~~~bash
wget https://dlcdn.apache.org/hbase/2.5.7/hbase-2.5.7-bin.tar.gz
tar -zxvf hbase-2.5.7-bin.tar.gz
sudo mv hbase-2.5.7 /opt/hbase
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
    <name>hbase.zookeeper.property.dataDir</name>
    <value>/opt/zookeeper/data</value>
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
~~~

- set environment variables
~~~bash
nano ~/.bashrc
export HBASE_HOME=/opt/hbase
export PATH=$PATH:$HBASE_HOME/bin
source ~/.bashrc
~~~

3. start hbase.
~~~bash
cd /opt/hbase/bin
./start-hbase.sh
~~~
can check if successfully start via command 'jps'.





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


## REDIS installation
1. install redis and change file permission in each node.
~~~bash
sudo apt-get install redis-server -y
sudo chmod 755 /etc/redis -R
~~~

2. configuration.
~~~bash
sudo nano /etc/redis/redis.conf
~~~

- in rpi0:
    - change line ‘bind 127.0.0.1 -::1’ to ‘bind 127.0.0.1 -::1 192.168.1.114’
        
    - change ‘protected-mode yes’ to ‘protected-mode no’

- in worker nodes:
    - change line ‘bind 127.0.0.1 -::1’ to ‘bind 127.0.0.1 -::1 192.168.1.11x’ x=5/6/7 for rpi1/2/3

    - Find the line ‘# replicaof <masterip> <masterport>’ and replace as ‘replicaof 192.168.1.114 6379’

    - change ‘protected-mode yes’ to ‘protected-mode no’

3. restart redis in every node.
~~~bash
sudo systemctl restart redis.service
~~~

4. test in master node.
~~~bash
redis-cli
INFO replication
~~~
should show the info of 3 connected slaves.
