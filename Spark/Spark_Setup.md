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
    spark.jars                       /opt/hive/lib/hive-exec-4.0.0-beta-1.jar,/opt/hive/lib/hive-metastore-4.0.0-beta-1.jar,/opt/hive/lib/hive-common-4.0.0-beta-1.jar,/opt/hive/lib/libthrift-0.16.0.jar,/opt/hive/lib/hive-serde-4.0.0-beta-1.jar,/opt/hive/lib/hive-service-4.0.0-beta-1.jar
    spark.sql.warehouse.dir          /user/hive/warehouse
    spark.hadoop.hive.metastore.uris thrift://rpi0:9083
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

    also copy the hive-site.xml from /opt/hive/conf, and place it in /opt/spark/conf.

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

6. installing JupyterLab in rpi0:

    - install it in an isolated environment:
    ```
    cd /opt/spark
    sudo apt-get update
    sudo apt-get upgrade -y
    python3 -m venv myjupyterenv
    source myjupyterenv/bin/activate
    pip install jupyterlab
    pip install pyspark
    ```
    can use `deactivate` to exit the virtual environment.

    - configure PySpark to work with JupyterLab:
    ```
    export PYSPARK_DRIVER_PYTHON=jupyter
    export PYSPARK_DRIVER_PYTHON_OPTS='lab'
    ```

    - start JupyterLab.
    ```
    source myjupyterenv/bin/activate
    jupyter lab --ip=192.168.1.114
    ```
    and then you would get an URL which you can use to open the JupyterLab.