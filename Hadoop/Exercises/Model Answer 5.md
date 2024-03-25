# Model Answer 5

## A) Exploring HDFS
### i. Check the number of live nodes
In the `Overview` tab, the number of Live Datanodes should be 3. And under `Datanodes` tab, we can see more details including last contact time, block used, capacity, ect.

### ii. Standard replication factor
In the `hdfs-site.xml` configuration, we explicitly set the `dfs.replication` to 3. It can also be found under the heading `Utilities` - `Configuration`. 

### iii. Heartbeat interval
Still, we can find the heartbeat interval under `Utilities` - `Configuration`. Look for `dfs.heartbeat.interval`, it determines datanode heartbeat interval in seconds, the default value is 3. 

## B) Interacting with HDFS
We first have to copy the file from the local filesystem to the filesystem of the namenode. From there, we can first create a subdirectory, e.g. data and transfer the file to HDFS. This is done via `put` or `copyFromLocal`:
~~~bash
#From local machine
scp <Path to File To Copy> username@hostname:<Path to File will Go>
#From NameNode
sudo unzip FIFA_Dataset.zip
hadoop fs -mkdir /data
hadoop fs -copyFromLocal ~/FIFA_Dataset/female_players.csv /data
hadoop fs -copyFromLocal ~/FIFA_Dataset/male_players.csv /data
~~~
Other useful options are `-ls` for listing the contents of a directory, `-rm` for removing a file, and `-rmdir` for removing a directory.

We can also copy a file from HDFS to the local directory. The following command copies the file female_players.csv from the root directory of HDFS into a file called tmp.csv into the current local directory:
~~~bash
hadoop fs -get /female_players.csv ./tmp.csv
~~~

## C) Large File Storage
### i. How many blocks are the two files stored in?
female_players.csv needs one block and male_players.csv needs four blocks. Under `Utilities` we can select `Browse the file system` and then click on the files. In the drop-down menu, we can
get information about the individual blocks.
As we have a replication factor of 3 (i.e., each datanode stores a copy of the file), female_players.csv needs a total of three blocks and male_players.csv a total of twelve blocks.

### ii. What was the original file size and how much storage does the file occupy in total now?
The original file size of female_players.csv is 90 MByte and that of male_players.csv is 494 MByte. As the block size is 128 MByte, female_players.csv requires 128 MByte in HDFS and male_players.csv requires 512 MByte. For the total required storage space, these numbers have to be multiplied by 3 again.

## D) Changing the Replication Factor
Changing the replication factor can be done in the GUI or through command `hadoop fs -setrep`. For the total required storage space, we have to multiply the numbers from the last answer with the replication factor. Running a replication factor of 4 on three datanodes is not very useful. This means that one
of the datanodes will store a copy of the file.

## E) Inducing Data Loss 
When checking the status of the nodes under the heading `Datanodes`, we see that the time indicated under `Last contact` goes up for the killed datanode. After about 10 minutes, the namenode will realize that the node has crashed and this is also shown on the webpage. The formula to calculate the timeout is 
~~~bash
2 * dfs.namenode.heartbeat.recheck-interval + 10 * (1000 * dfs.heartbeat.interval)
~~~
Try to explicitly define a smaller number for the two parameters in `hdfs-site.xml` configuration to reduce the timeout.

As long as we have a replication factor higher than 1, we can still access the file, as the copies are distributed over the datanodes and are still available.


