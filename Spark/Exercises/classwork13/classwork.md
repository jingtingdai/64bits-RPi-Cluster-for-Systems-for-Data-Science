## Classwork 13

For this exercise, we are using Raspberry Pi (RPi) clusters. Essentially, there are two options to do this exercise:
- You show up on Wednesday afternoon for the practical exercise and work in small groups with one of the clusters. You will need to connect to a cluster using an Ethernet cable, so we need to make sure that enough people have an Ethernet port on their machine (at least one per group, I will bring a few USB-to-Ethernet adapters with me). Also, you will need to connect via SSH to the RPis.

- The other option is to create an RPi cluster at home. Instructions on how to do this can be found here: [Rpi Setup Instruction](https://github.com/DocSeven/PiCluster)

1. Start the raspberry pi cluster.
    - In order to get started, you need to connect the cluster via the Ethernet cable to your machine. The setup we use is to create a private network (usually used for sharing WiFi with other machines over Ethernet). The RPis in the cluster have fixed IP-addresses in the network 10.42.0.0/24: 10.42.0.250 (master), 10.42.0.251, 10.42.0.252, and 10.42.0.253. If the wired network created by you uses another address space, you have to change it to the address space 10.42.0.0./24. Network settings can be found here:
        - MacOS: under System Preferences → Internet and Network

        - Windows: under Settings → Network \& Internet

    - The RPis in the clusters are powered over Ethernet (PoE), which means that you only have to plug in the switch. You need to wait a bit until all RPis have booted. Before continuing, you may also have to connect to each RPi via SSH in turn:
    `
    ssh pi@10.42.0.25x
    `
    (where x=0, 1, 2, and 3. The password is raspberry)

2. Start Spark and jupyterLab.
    - Start Hadoop and Spark.
        - in rpi0:
        ```
        cd /opt/Hadoop/sbin
        ./start-dfs.sh
        ./start-yarn.sh
        start-master.sh
        ```
        - in worker nodes:
        ```
        start-worker.sh spark://rpi0:7077
        ```

    - Start JupyterLab (in rpi0).
    ```
    cd /opt/spark
    source myjupyterenv/bin/activate
    jupyter lab --ip=10.42.0.250
    ```
    it would return a URL that you can use in browser to get into the JupyterLab, plus you can also check about Spark in `http://rpi0:8080`

3. Download the dataset and upload the file into HDFS.
```
wget http://files.grouplens.org/datasets/movielens/ml-20m.zip
unzip ml-20m.zip
hdfs dfs -put ml-20m /data/
```

4. Once all of the steps described above have been completed, you are ready to start the actual exercise, which can be found here: [Exercise](https://github.com/DocSeven/PiCluster/tree/master/Exercises). Some changes that need to be taken in the jupyter notebook:
    - substitute the file path to `hdfs://rpi0:8020/data/ml-20m/xxx.csv` 

    - when start a spark session, using code:
    ```
    import os
    os.environ["JAVA_HOME"] = "/usr/lib/jvm/jdk-11.0.21+9"
    os.environ["SPARK_HOME"] = "/opt/spark"

    from pyspark.sql import SparkSession

    spark = SparkSession.builder \
        .master("spark://rpi0:7077") \
        .appName("MyApp") \
        .getOrCreate()
    sc = spark.sparkContext
    ```
    

