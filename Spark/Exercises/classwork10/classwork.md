## Classwork 10

This exercise uses Apache Spark. The instruction to use raspberry pi cluster we provided for this exercise:

- Start the raspberry pi cluster.

    `
    ssh pi@192.168.1.11x
    `
    (where x=4, 5, 6, and 7 for rpi0, rpi1, rpi2, rpi3. The password is raspberry)

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

1. Download the notebook `SparkDemo.ipynb` (or, if using Spark locally, `SparkDemo.html`) and the files `2015-summary.csv` & `data.tar.gz` from this git repository and follow the instructions above to get it up and running. Then follow the instructions in the notebook. During this introduction to Spark, you will learn about Spark in a more general (offline) context as well as in the context of a streaming application.



