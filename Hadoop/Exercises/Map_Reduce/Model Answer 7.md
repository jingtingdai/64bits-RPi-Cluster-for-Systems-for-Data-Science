# Model Answer 7

## A) Exploring WordCount
Copy the file from local directory to the filesystem of the namenode, create the HDFS directory and upload csv file.

~~~bash
#From local machine
scp <Path to File To Copy> username@hostname:<Path to File will Go>
#From NameNode
hadoop fs -mkdir /data
hadoop fs -copyFromLocal <Path to File>/power_consumption.csv /data
~~~

After the word count praogram is finished, cat the out put file to look at the result.

~~~bash
hadoop fs -cat /data/output/part-r-00000
~~~

## B) Power consumption of households
The Map-Reduce Framework under mapreduce.Job: Counters will return

~~~bash
Map input records=9
Map output records=8
Map output bytes=184
Map output materialized bytes=206
Input split bytes=107
Combine input records=0
Combine output records=0
Reduce input groups=4
Reduce shuffle bytes=206
Reduce input records=8
Reduce output records=4
~~~

The Map input taks all 8 records and 1 heading row and output 8 data records, then the Reduce takes the 8 output from Map and reduces to 4 records. The Reduce input groups represents the number of unique keys fed into the reducers, which in our case is the 4 unique HID.
