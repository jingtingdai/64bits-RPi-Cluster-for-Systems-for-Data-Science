
## Classwork 6

For this exercise, we use two NoSQL systems: Redis and HBase. We would provide raspberry pi cluster with Redis and Hbase installed to finish this exercise. However, if you want to install them directly on your system, this is also possible. In this case, you have to go to [Redis Download](https://redis.io/download) or [HBase Download](https://www.apache.org/dyn/closer.lua/hbase/), respectively, and follow the instructions given there. (Some Linux distributions offer a Redis package that you can install.)

- Start the raspberry pi cluster.
    - In order to get started, you need to connect the cluster via the Ethernet cable to your machine. The setup we use is to create a private network (usually used for sharing WiFi with other machines over Ethernet). The RPis in the cluster have fixed IP-addresses in the network 10.42.0.0/24: 10.42.0.250 (master), 10.42.0.251, 10.42.0.252, and 10.42.0.253. If the wired network created by you uses another address space, you have to change it to the address space 10.42.0.0./24. Network settings can be found here:
        - MacOS: under System Preferences → Internet and Network

        - Windows: under Settings → Network \& Internet

    - The RPis in the clusters are powered over Ethernet (PoE), which means that you only have to plug in the switch. You need to wait a bit until all RPis have booted. Before continuing, you may also have to connect to each RPi via SSH in turn:
    `
    ssh pi@10.42.0.25x
    `
    (where x=0, 1, 2, and 3. The password is raspberry)


You are now ready to start the actual exercises.

1. The first exercise refers to Redis. Download the tutorial/guide `The Little Redis Book`, available as PDF on OLAT, and work through the examples in the first three chapters. Start Redis in all nodes with this command: `sudo systemctl start redis`

    The tutorial contains a few lines of Ruby code, which cannot be executed in the command-line interface of Redis. For example, the following lines are found on page 12:  
    ```ruby
        ids = redis.lrange('newusers', 0, 9)
        redis.mget(*ids.map {|u| "users:#{u}"})
    ```
    There is similar code on pages 15, 16, and 17. Just skip these parts.

2. In the second exercise, we work with HBase. Start Hbase with following code:
    - in every nodes:
    ```
    cd /opt/Hadoop/sbin
    ./start-dfs.sh
    ./start-yarn.sh
    cd /opt/hbase/bin
    ./start-hbase.sh
    ```

    - access Hbase shell in rpi0:
    ```
    ./hbase shell
    ```

    a) As a warmup, go through steps 3 to 10 of the “Procedure: Use HBase For the First Time” part of Section 2.2 in the HBase Reference Guide, which can be found here: [HBase Quickstart](https://hbase.apache.org/book.html#quickstart).  
       You can skip steps 1 to 4, as they only describe how to download and install HBase from scratch. You can go directly to the section “Procedure: Use HBase For the First Time”.
    
    b) A table in HBase has a specific substructure. Each cell in a table is defined by its row, column family, column qualifier, and version. For instance, when you scan the table `test` from the warmup part, the row of the first record is `row1`, the column family is `cf`, the column qualifier is `a`, and the version is the timestamp. If you have dropped the table during the warmup exercise, create it again and insert the rows `row1`, `row2`, and `row3`.

    i. When querying the database, you can use different granularities. 
    
    First, add another column to the third record (`row3`):  
    ```
    put 'test', 'row3', 'cf:a', 'value4'
    ```

    When you retrieve `row3`, you get all the information:  
    ```
    get 'test', 'row3'
    ```

    You can restrict yourself to just one column family (here `cf`):  
    ```
    get 'test', 'row3', {COLUMN => 'cf'}
    ```

    or to one column within this family:  
    ```
    get 'test', 'row3', {COLUMN => 'cf:a'}
    ```

    ii. Look up the content of `cf:c` for `row3`, remember the timestamp, and insert another value into the cell:  
    ```
    put 'test', 'row3', 'cf:c', 'value5'
    ```

    When you now look up the content of `cf:c` for `row3`, you get the new value and timestamp. However, it seems the old value is still retained. Run the following query (replace `xxx` with the old timestamp):  
    ```
    get 'test', 'row3', {COLUMN => 'cf:c', TIMESTAMP => xxx}
    ```

    This will return the previous content. When you overwrite or delete a row, it is scheduled for deletion and it is still around until then. You can force HBase to do the deletion immediately by issuing the following commands:
    ```
    flush 'test'
    major_compact 'test'
    ```

    If you try to access the old row again (with the option `TIMESTAMP`), it is gone.

    iii. If you want to keep around different versions, you have to configure HBase to do so. When you run
    ```
    describe 'test'
    ```

    you see a parameter `VERSIONS`, which is set to 1. Change this parameter to 3 (this keeps the three most recent versions): 
    ```
    alter 'test', NAME => 'cf', VERSIONS => 3
    ```

    Reinsert a new row3 and see what happens: 
    ```
    put 'test', 'row3', 'cf:c', 'value6'
    ```

    Scanning the table with `scan 'test'` returns the new value. However, you can also ask for all the stored versions with 
    ```
    scan 'test', {VERSIONS => 3}
    ```

    This will show you the different versions that are available. These versions are still around after flushing and compacting the database.

    iv. Now delete one of the old versions (`xxx` is a timestamp again): 
    ```
    delete 'test', 'row3', 'cf:c', xxx
    ```

    Scanning the table will reveal that this cell is gone when you explicitly delete it: 
    ```
    scan 'test', {VERSIONS => 3}
    ```

3. In the third exercise we will see how HBase handles a large dataset, as well as learn about filters in HBase. We are using exercise 5 of the [Big Data For Engineers at ETH](https://github.com/RumbleDB/bigdata-exercises.git).

    a) The provided dataset comprises metadata information of articles from the English version of Wikipedia. The .csv file uses the following variables: 

    We use the `wiki_small` dataset (about 85MB) in this assignment, as we want to load it into HBase in a reasonable timeframe (will take about 5-10 minutes). Based on the variable description in the table above, we can categorize the variables into two categories:

        i. some variables are about a page;
        ii. others are about an author/contributor.

    b) Setting up the dataset:

    - Download the csv file using `wget` command and check if it exists using `ls`.

    - Run the following command to start hbase:
    ```
    ./hbase shell
    ```

    - Now create the schema in HBase with two column families, page and author:
    ```
    create 'wiki_small', 'page', 'author'
    ```

    - After the table is created, exit the HBase shell:
    ```
    exit
    ```

    - Now populate the table wiki_small with data using the ImportTsv utility of HBase by running the following command.
    ```
    hbase org.apache.hadoop.hbase.mapreduce.ImportTsv \
    -Dimporttsv.separator=, -Dimporttsv.columns="HBASE_ROW_KEY, \
    page:page_title,page:page_ns,page:revision_id, \
    author:timestamp,author:contributor_id, \
    author:contributor_name,page:bytes" \
    wiki_small enwiki-20200920-pages-articles-multistream_small.csv
    ```

    We need to specify which column in the csv maps to which column in the HBase table. Note that we make page id into the `HBASE_ROW_KEY`. The command will trigger a lot of (harmless) messages, mostly status updates and non-critical warnings, e.g. reporting ”Bad Lines”, which drops some lines due to illegal characters, but there is plenty of data left.

    - You can count how many rows there are using this command from your head node’s shell: 
    ```
    hbase org.apache.hadoop.hbase.mapreduce.RowCounter 'wiki_small'
    ```

    - Now let us return to the HBase shell and run some queries against the `wiki_small` table. We will use some of the filter provided by HBase, you can obtain a list of the available filters by running `show_filters` in the HBase shell. You will see filters such as `PrefixFilter()`, `ValueFilter()`, or `SingleColumnValueFilter()`.

    c) Tasks to do with `wiki small`:

    i. How does HBase index the row keys? We choose page_id in the original table to be the row keys in the HBase table. What do you observe running the following two queries? What can you say about row key indexing based on the results?
    ```
    scan 'wiki_small', {STARTROW=>'100009', ENDROW=>'100011'}
    scan 'wiki_small', {STARTROW=>'100015', ENDROW=>'100016'}
    ```

    ii. Write the following queries:

        A. Select all article titles and author names where the row name starts with ’1977’.

        B. Select all article titles and author names where the author contains the substring ’tom’.

    iii. Write the following queries:

        A. Return the number of articles from 2017.

        B. Return the number of articles that contain the word ’Sydney’ in them. Try out different variations for formulating the query.



