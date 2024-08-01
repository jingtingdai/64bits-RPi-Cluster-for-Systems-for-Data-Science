

## Classwork 11




For this exercise, we are using Raspberry Pi (RPi) clusters. 

1. Start the raspberry pi cluster.

    `
    ssh pi@10.42.0.25x
    `
    (where x=0, 1, 2, and 3 for rpi0, rpi1, rpi2, rpi3. The password is raspberry)

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

3. For this exercise, we are using the machine learning library ML of Apache Spark. Instructions on how to set up the environment are provided in the Jupyter notebook `SparkML.ipynb`: for Google Colab, on your own systems, and on Databricks. And download the csv files from this git repository and upload the files into HDFS.
```
hdfs dfs -put diabetes.csv /data/
hdfs dfs -put iris.csv /data/
```


4. Once all of the steps described above have been completed, you are ready to start the actual exercise.

    - The first exercise (in `SparkML.ipynb`) is about classifying two types of irises (the flowers) using some typical characteristics. This is mainly about following the instructions in the notebook. After completing the notebook, go back to the grid search section and try to find some parameters for which the model will perform better.

    - For the second exercise, we use the Kaggle dataset Pima Indians Diabetes Database, available here (and on this git repository)
[Pima Indians Diabetes Database](https://www.kaggle.com/uciml/pima-indians-diabetes-database)
about diagnostically predicting whether a patient has diabetes or not. Create your own Jupyter notebook and use the techniques employed in the iris-notebook (or any other technique you want to try out) to build a logistic regression classifier for the diabetes dataset.

