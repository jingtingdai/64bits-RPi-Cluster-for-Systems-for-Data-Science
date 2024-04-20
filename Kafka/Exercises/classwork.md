
## Classwork 9


For this classwork exercise, we use Kafka, which is a platform for streaming events. Streams of
events are organized around topics, which can be seen as message queues or containers for a certain
category of events. Producers publish events to one or more topics and consumers subscribe to one or
more topics, i.e., producers write events and consumers read them. A brief introduction to Kafka can
be found here: [Kafka Introduction](https://kafka.apache.org/intro). We would finish this classwork with our raspberry pi
cluster:


- Start the raspberry pi cluster.

    - In order to get started, you need to connect the cluster via the Ethernet cable to your machine. The setup we use is to create a private network (usually used for sharing WiFi with other machines over Ethernet). The RPis in the cluster have fixed IP-addresses in the network 10.42.0.0/24: 10.42.0.250 (master), 10.42.0.251, 10.42.0.252, and 10.42.0.253. If the wired network created by you uses another address space, you have to change it to the address space 10.42.0.0./24. Network settings can be found here:

        - MacOS: under System Preferences → Internet and Network

        - Windows: under Settings → Network & Internet

    - The RPis in the clusters are powered over Ethernet (PoE), which means that you only have to plug in the switch. You need to wait a bit until all RPis have booted. Before continuing, you may also have to connect to each RPi via SSH in turn (to accept the SSH-keys of all RPis, needed to run ansible scripts):
    ```
    ssh pi@10.42.0.25x
    ```
    where x=0, 1, 2, and 3. The password is `raspberry`

- Start Kafka in each node.
```
cd /opt/kafka/bin
./zookeeper-server-start.sh -daemon /opt/kafka/config/zookeeper.properties
./kafka-server-start.sh -daemon /opt/kafka/config/server.properties
```

You are now ready to start the actual exercises.

1. Get familiar with Kafka command line.

    - Create topics: topics are where messages are published, use this command to create a new topic named `test`.
    ```
    ./kafka-topics.sh --create --bootstrap-server rpi0:9092 --replication-factor 1 --partitions 1 --topic test
    ```

    - List topics: you can list all existing topics by running:
    ```
    ./kafka-topics.sh --bootstrap-server rpi0:9092 --list
    ```

    - Send message using producer by running:
    ```
    ./kafka-console-producer.sh --broker-list rpi0:9092 --topic test
    ```
    It will show you a > prompt where you can input the message to be produced. For example:
    ```
    > Hello
    > World
    ```

    - Consume message using consumer by running: (in another shell)
    ```
    bin/kafka-console-consumer.sh --topic test --from-beginning --bootstrap-server rpi0:9092
    ```
    It will show you all the messages from the beginning until now. By omitting `--from-beginning` the consumer will only show messages from the point it was started. Anything you enter on the producer side will shortly show up on the consumer side.

    - Once you are finished, you can delete the topic again:
    ```
    ./kafka-topics.sh --bootstrap-server rpi0:9092 --delete --topic test
    ```

2. Use Kafka with Python:

    - In order to use Kafka with Python, we need to install kafka-python using pip by running in rpi0:
    ```
    sudo apt install python3-kafka
    ```
    After installation, we can now start creating producers/consumers and processing streams of data with Python. In this exercise, we will build some of the functionality shown on the lecture slides.

    **Note**: substitute all the `localhost` to `rpi0`

    - On OLAT, there are two folders (compressed in a zip-file) with Python files for accessing Kafka. The one named `kafka_example` contains a small example for a temperature data processing pipeline where there is only one producer/consumer pair. The producer writes the input data line by line as events into the topic `temperature`, the consumer subscribes the topic and and, in turn, passes the messages through three operators (converting the temperature value from Celsius to Fahrenheit, adding some noise, and finally rounding the value).

        In order to run the Python code, first make sure your Zookeeper and Kafka are up and running, then open two consoles and run both scripts (start the consumer first). You can then observe the producer and consumer process the individual messages.

    - The `kafka_chaining` folder has more than one pair of producers and consumers. It is still a temperature processing pipeline with similar operators as in the kafka example folder. However, this time you are building a more complex structure: the temperatures are converted from Celsius to Fahrenheit, then filtered by a threshold, after which the events are split into two streams, one stream is passed through EWMA and another through Avg. We provide example code for one stateless operator(`celsius_to_fahrenheit`), one stateful operator (EWMA), and one output consumer of EWMA. Your task is to fill in/replace code to make this work. Currently, there is some placeholder code that just passes through the events without processing them. In particular, you should finish another stateless operator, stateful operator, and output consumer of moving average.

        - To run this in a raspberry pi cluster with 4 nodes, run `pro.py` in rpi0, run `con1.py` in rpi1, run `con2.py` and `out_ewma.py` in rpi2, run `con3.py` and `out_avg.py` in rpi3.



