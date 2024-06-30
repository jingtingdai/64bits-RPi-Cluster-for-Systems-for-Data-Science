## Classwork 13

For this exercise, we are using Raspberry Pi (RPi) clusters. 

1. Start the raspberry pi cluster.

    `
    ssh pi@192.168.1.11x
    `
    (where x=4, 5, 6, and 7 for rpi0, rpi1, rpi2, rpi3. The password is raspberry)

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
    jupyter lab --ip=192.168.1.114
    ```
    it would return a URL that you can use in browser to get into the JupyterLab, plus you can also check about Spark in `http://rpi0:8080`

3. Download the dataset and upload the file into HDFS.
```
wget http://files.grouplens.org/datasets/movielens/ml-20m.zip
unzip ml-20m.zip
hdfs dfs -put ml-20m /data/
```

4. Once all of the steps described above have been completed, you are ready to start the actual exercise, which can be found here: [Exercise](https://github.com/DocSeven/PiCluster/tree/master/Exercises). 


    

