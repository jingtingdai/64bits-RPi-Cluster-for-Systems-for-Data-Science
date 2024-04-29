# Classwork 7

## A) Exploring WordCount
Fro the master node, start HDFS and YARN. Create a data directory in HDFS and then upload a text file (for example README.txt under $HADOOP_HOME). Follow the [File System Shell Guide](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/FileSystemShell.html) or upload directly under `Utilities - Browse the file system` through the GUI on http://rpi0:9870/.

Test a simple WordCount Application on the text file, the output data will be stored in a directory named `output`.

~~~bash
bin/hadoop jar share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar wordcount /data/README.txt /data/output
~~~

During the program execution, a url to track the job and the MapReduce progress will be provided. Check the result by cat file `part-r-00000` in the output directory. 

## B) Power consumption of households
Download the csv file and the Java source code. Upload csv file to the HDFS data directory and save the source code to a new directory. Compile the code into Java classes with the javac command.

~~~bash
javac -classpath `hadoop classpath` -d output_classes src/com/example/hadoop/*.java
~~~

Create the Jar file with the jar command.
~~~bash
jar -cvf PowerConsumptionAnalysis.jar -C output_classes/ .
~~~

Run the jar command.
~~~bash
hadoop jar $HADOOP_HOME/project-root/PowerConsumptionAnalysis.jar com.example.hadoop.Main /data/power_consumption.csv /data/power_output
~~~
In mapreduce.Job: Counters, how many records are in Map input, Map output, Reduce input and Reduce output? What does Reduce input groups represent?