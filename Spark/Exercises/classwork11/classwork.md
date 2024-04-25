

## Classwork 11




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

3. For this exercise, we are using the machine learning library ML of Apache Spark. Instructions on how to set up the environment are provided in the Jupyter notebook `SparkML.ipynb`: for Google Colab, on your own systems, and on Databricks. And download the csv files from OLAT and upload the files into HDFS.
```
hdfs dfs -put diabetes.csv /data/
hdfs dfs -put iris.csv /data/
```


4. Once all of the steps described above have been completed, you are ready to start the actual exercise.

    - The first exercise (in `SparkML.ipynb`) is about classifying two types of irises (the flowers) using some typical characteristics. This is mainly about following the instructions in the notebook. After completing the notebook, go back to the grid search section and try to find some parameters for which the model will perform better.

    - For the second exercise, we use the Kaggle dataset Pima Indians Diabetes Database, available here (and on OLAT as a csv-file)
[Pima Indians Diabetes Database](https://www.kaggle.com/uciml/pima-indians-diabetes-database)
about diagnostically predicting whether a patient has diabetes or not. Create your own Jupyter notebook and use the techniques employed in the iris-notebook (or any other technique you want to try out) to build a logistic regression classifier for the diabetes dataset.

### Note
Some changes that need to be taken in the jupyter notebook:
- substitute the file path to `hdfs://rpi0:8020/data/xxx.csv` 

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
