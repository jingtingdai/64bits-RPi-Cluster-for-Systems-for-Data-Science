## HIVE installation
1. download and install in all the nodes:
~~~bash
wget https://dlcdn.apache.org/hive/hive-4.0.0/apache-hive-4.0.0-bin.tar.gz
tar -zxvf apache-hive-4.0.0-bin.tar.gz
sudo mv apache-hive-4.0.0-bin /opt/hive
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

    2. secure the user named ‘postgres’ (in rpi0):
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

    3. configure PostgreSQL to allow remote connections from the other nodes (in rpi0):
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

    5. prepare the PostgreSQL database (in rpi0):
    ~~~bash
    sudo -i -u postgres
    psql
    CREATE DATABASE hive_metastore;
    CREATE USER hiveuser WITH PASSWORD '12345';
    GRANT ALL PRIVILEGES ON DATABASE hive_metastore TO hiveuser;
    \q
    exit
    ~~~

    6. download PostgreSQL JDBC driver and put in hive lib directory (in rpi0):
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

5. Lib guava - conflict issue (in rpi0)
~~~bash
rm /opt/hive/lib/guava-22.0.jar
cp /opt/Hadoop/share/hadoop/common/lib/guava-27.0-jre.jar /opt/hive/lib/
cp /opt/hive/conf/hive-env.sh.template  /opt/hive/conf/hive-env.sh
~~~

6. configure hive to use postgresql (in rpi0):
- hive-site.xml
~~~bash
cd /opt/hive/conf
touch hive-site.xml
nano hive-site.xml
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
  <property>
    <name>hive.exec.mode.local.auto</name>
    <value>false</value>
  </property>
  <property>
    <name>mapreduce.framework.name</name>
    <value>yarn</value>
  </property>
  <property>
    <name>yarn.resourcemanager.address</name>
    <value>rpi0:8032</value>
  </property>
  <property>
    <name>fs.defaultFS</name>
    <value>hdfs://rpi0:8020</value>
  </property>
</configuration>
~~~
also copy the hive-site.xml to /opt/spark/conf.
```
cp hive-site.xml /opt/spark/conf/
```

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

- add these to /opt/spark/conf/spark-defaults.conf
```
spark.jars                       /opt/hive/lib/hive-exec-4.0.0.jar,/opt/hive/lib/hive-metastore-4.0.0.jar,/opt/hive/lib/hive-common-4.0.0.jar,/opt/hive/lib/libthrift-0.16.0.jar,/opt/hive/lib/hive-serde-4.0.0.jar,/opt/hive/lib/hive-service-4.0.0.jar
spark.sql.warehouse.dir          /user/hive/warehouse
spark.hadoop.hive.metastore.uris thrift://rpi0:9083
```


7. Configure schema init permission (in rpi0):
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

8. start hive (in rpi0).
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
