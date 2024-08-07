## Classwork 12

This exercise uses Hive, which is part of the Hadoop framework and is a distributed data warehouse built on top of HDFS. In order to get everything up and running, you need to start the raspberry pi cluster we offered first.

1. Start the raspberry pi cluster.

    `
    ssh pi@10.42.0.25x
    `
    (where x=0, 1, 2, and 3 for rpi0, rpi1, rpi2, rpi3. The password is raspberry)

2. Start Hadoop and Hive.
    - in rpi0:
    ```
    cd /opt/Hadoop/sbin
    ./start-dfs.sh
    ./start-yarn.sh

    nohup hive --service metastore &
    nohup hive --service hiveserver2 &
    beeline
    !connect jdbc:hive2://rpi0:10000/default
    ```
    enter skip input username and password.

3. Create 'testdb' database in hive.
```
CREATE DATABASE IF NOT EXISTS testdb;
```

4. Download the file `hive.tar.gz` from OLAT and unpack it. 

5. Go to the directory `employee` and create a table `employee` in beeline:
```
!run employee_table.hql
```


6.  Load the content of the table (`employee.csv`) into HDFS:
```
hdfs dfs -put employee.csv /user/hive/warehouse/testdb.db/employee
```

7. Now start to try out using Hive.
```
SHOW DATABASES;
USE testdb;
SHOW TABLES;
SELECT * FROM employee;
```
You can stop the interface by typing in
```
!exit
```


You are now ready to do the exercises. Do not forget to stop the shell you started in step 2. with `!exit` and to shut down the Hadoop containers, once you are done with the exercises, by calling
```
cd /opt/Hadoop/sbin
./stop-all.sh
```

Hint: if you want to see table headings in the result of a query, you have to enable this feature:
```
SET hive.cli.print.header=true;
```

Also, if you plan to write queries in which you formulate the join predicate in the where clause, you may have to tell Hive to run in a non-strict mode. Otherwise, it may complain that it will not execute queries with a Cartesian product in them:
```
SET hive.mapred.mode=nonstrict;
```


1. 
    - Create the tables `order_item`, `orders`, and `products` with the files found in the directory `employee`. The file `line_item.hql` contains the schema definition of the tables and the location of the content files. 

    - Next you need to copy the csv-files to HDFS. When you check the file `line_item.hql`, you will see that rather than specifying a file, the content is specified via a directory. That means, you may have to first create subdirectories `order_item`, `orders`, and `products` (if they have not been created by `line_item.hql`) and then copy the csv-files into the corresponding directory.

    - Can you think of a reason why Hive uses directories to specify the content of the tables? What happens if you copy one of the files into the corresponding subdirectory twice (for example, copy `orders.csv` as `orders2.csv` into the `orders` subdirectory on HDFS)?

2. Once you created the tables, just have a look at the content by running the query `select * from <table_name>` on all three tables to see if everything worked properly

To successfully run join in 3.&4., need to set:
```
SET hive.auto.convert.join=false;
```

3. Run a query that selects one column from one of the tables. Next, run a query that joins all three tables via their key/foreign-key relationships (`orderid` and `prodid`). Looking at the output, you can see that the join-query seems to do a lot more work. You can have a closer look at the query execution plans that were generated by putting the keyword `explain` in front of a query. This will give you a detailed description of the query execution plan. How many stages does the plan for the projection query have? How many does the plan for the join query have? Why do you think the join does not have a reduce phase?

4. Now write a query that groups the tuples in `order_item` by `orderid` and counts the number of items in each group. Look at the query execution plan with `explain`. Can you see a difference to the plans from the previous question? Modify the aggregation query by sorting the results by the counts. Again look at the query execution plan. Do you see any differences compared to the unsorted one?
