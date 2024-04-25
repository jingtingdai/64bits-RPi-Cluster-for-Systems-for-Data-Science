## Classwork 10

This exercise uses Apache Spark. Similar to the previous exercise, there are two different ways to use Spark:

- Either you download the Jupyter notebooks (files ending in .ipynb) from the course web page, upload them to the Google Drive connected to your Gmail account, and open them there. (Google Drive may ask you which app to connect them to: you have to connect them to colab.) Once you have done this, you can start with the exercises. This is the simplest option and it should work out of the box.

- For the second variant you can use the raspberry pi clusters we offered. The instruction to use it for this exercise:

    - Start the raspberry pi cluster.
        - In order to get started, you need to connect the cluster via the Ethernet cable to your machine. The setup we use is to create a private network (usually used for sharing WiFi with other machines over Ethernet). The RPis in the cluster have fixed IP-addresses in the network 10.42.0.0/24: 10.42.0.250 (master), 10.42.0.251, 10.42.0.252, and 10.42.0.253. If the wired network created by you uses another address space, you have to change it to the address space 10.42.0.0./24. Network settings can be found here:
            - MacOS: under System Preferences → Internet and Network

            - Windows: under Settings → Network \& Internet

        - The RPis in the clusters are powered over Ethernet (PoE), which means that you only have to plug in the switch. You need to wait a bit until all RPis have booted. Before continuing, you may also have to connect to each RPi via SSH in turn:
        `
        ssh pi@10.42.0.25x
        `
        (where x=0, 1, 2, and 3. The password is raspberry)

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
        you can also check about Spark in `http://rpi0:8080`

    You then have to run the operators in the Python shell of Spark, which you start with `pyspark --master spark://rpi0:7077` . In order to make it easier to copy/paste the commands from the Jupyter notebook into the shell, an html-version of the notebook is available. If you use this option, you can skip the set-up and configuration instructions in the notebook (and also do not need to upload the data file). And if you encounter error 
    ```
    env:`jupyter`: No such file or directory
    ```
    can manually change the enviroment variables:
    ```
    unset export PYSPARK_DRIVER_PYTHON
    unset PYSPARK_DRIVER_PYTHON_OPTS
    ```


You are now ready to do the exercise, which (again) involves running a Jupyter notebook and writing small snippets of code.

1. Download the notebook `SparkDemo.ipynb` (or, if using Spark locally, `SparkDemo.html`) and the files `2015-summary.csv` & `data.tar.gz` from OLAT and follow the instructions above to get it up and running. Then follow the instructions in the notebook. During this introduction to Spark, you will learn about Spark in a more general (offline) context as well as in the context of a streaming application.

**Note**: put data files to HDFS using command `hdfs dfs -put /path/to/file /data` and using them in jupyter notebook with path `hdfs://rpi0:8020/data/xxx.csv`


