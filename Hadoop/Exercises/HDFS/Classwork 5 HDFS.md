# Classwork 5

This classwork is adapted from the existing classwork that deploys HDFS on a cluster of Docker containers. Instead, we will run Hadoop and conduct experiments on HDFS using the Raspberry Pi cluster we've just set up, consisting of one NameNode and three DataNodes. The data file is the open dataset of all FIFA players (available on [Kaggle](https://www.kaggle.com/datasets/stefanoleone992/fifa-22-complete-player-dataset)).

## A) Exploring HDFS
From the master node(rpi0), start HDFS, and access the GUI on http://rpi0:9870/. It provides information on cluster health, logs as well as a visual interface to upload data. Explore it a bit and find the following in formation:

    i. Check the number of live nodes
    ii. Standard replication factor
    iii. Heartbeat interval

## B) Interacting with HDFS
Now, start modifying the HDFS, first by creating a directory named `data` and then uploading the list of female players to the HDFS within that directory. To do this get acquainted with the [Hadoop CLI](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HDFSCommands.html). To copy local files to the namenode, you can use the following command:
~~~bash
scp <Path to File To Copy> username@hostname:<Path to File will Go>
~~~

In general, HDFS commands follow the structure `hdfs fs <regular shell cmd>`

## C) Large File Storage
Next, upload the `male_players.csv` dataset to the HDFS. Find the uploaded data through the GUI.

    i. How many blocks are the two files in stored in?
    ii. What was the original file size and how much storage does the file occupy in total now?

## D) Changing the Replication Factor
Try changing the replication factor for the `male_players.csv` file to 4 and 2. How did the answers to the above questions change?

## E) Inducing Data Loss 
Forcefully make one of the data nodes exit by using the `hdfs --daemon stop datanode` and `yarn --daemon stop nodemanager` commands on the data node. You can monitor the condition on the GUI Datanodes tab.
What behaviour can you observe? Can you still fetch the entire `male_players.csv` file?

After finishing the exercises above, don't forget to stop the HDFS daemon using `./stop-dfs.sh && ./stop-yarn.sh`.
