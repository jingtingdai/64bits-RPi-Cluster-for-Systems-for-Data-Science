create database if not exists testdb;
use testdb;
create external table if not exists order_item (
  orderid int,
  itemid int,
  prodid int,
  quantity int,
  totalretail string,
  priceperunit string
)
row format delimited
fields terminated by ';'
lines terminated by '\n'
stored as textfile location 'hdfs://rpi0:8020/user/hive/warehouse/testdb.db/employee/order_item';
create external table if not exists orders (
  orderid int,
  ordertype int,
  empid int,
  custid int,
  orderdate string,
  deliverydate string
)
row format delimited
fields terminated by ';'
lines terminated by '\n'
stored as textfile location 'hdfs://rpi0:8020/user/hive/warehouse/testdb.db/employee/orders';
create external table if not exists products (
  prodid int,
  name string,
  supplierid int,
  prodlevel int
)
row format delimited
fields terminated by ';'
lines terminated by '\n'
stored as textfile location 'hdfs://rpi0:8020/user/hive/warehouse/testdb.db/employee/products';



