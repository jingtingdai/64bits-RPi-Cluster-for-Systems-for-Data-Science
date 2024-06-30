## Model Answer 12

1. -  Just run the script `!run line_item.hql` in beeline .

    -  If the subdirectories have not been created by the hql-file, you can do so manually. First check whether the directories are there:
    ```
    hadoop fs -ls hdfs://rpi0:8020/user/hive/warehouse/testdb.db/employee
    ```

    If not, run the following commands:
    ```
    hadoop fs -mkdir hdfs://rpi0:8020/user/hive/warehouse/testdb.db/employee/orders
    hadoop fs -mkdir hdfs://rpi0:8020/user/hive/warehouse/testdb.db/employee/order_item
    hadoop fs -mkdir hdfs://rpi0:8020/user/hive/warehouse/testdb.db/employee/products
    ```

    Copying the files is done with these commands:
    ```
    hadoop fs -put orders/orders.csv hdfs://rpi0:8020/user/hive/warehouse/testdb.db/employee/orders
    hadoop fs -put order_item/order_item.csv hdfs://rpi0:8020/user/hive/warehouse/testdb.db/employee/order_item
    hadoop fs -put products/products.csv hdfs://rpi0:8020/user/hive/warehouse/testdb.db/employee/products
    ```

    - Hive takes all the files found in a directory as the content of a table. As tables can get very large, this allows us to break up the content into several files. Each individual file fits onto a single machine, while the total amount may not.

    If you copy a file into the directory twice, the tuples in this file will appear twice in the table.

2. Just run the queries and check the result.

3. Selecting one column is done with the following query:
```
select orderid from orders;
```

Joining the tables can be done via
```
select *
from orders o, order_item i, products p
where o.orderid = i.orderid
and i.prodid = p.prodid;
```

You can get detailed information about the query execution plan by putting the keyword 'explain' in front of a query:
```
explain select orderid from orders;
```

The projection query has a single phase. The join has three phases. Interestingly, the join does not use reduce phases: for small relations (that fit into main memory), Hive loads the whole table into every mapper and executes the join in the map phase

4. 
```
select orderid, count(*)
from order_item
group by orderid;
```
The aggregation query has a reduce phase. The query execution plans of the projection and join queries only had map phases.

```
select orderid, count(*) cnt
from order_item
group by orderid
order by cnt;
```
This query has an additional stage (the sorting requires another one).
