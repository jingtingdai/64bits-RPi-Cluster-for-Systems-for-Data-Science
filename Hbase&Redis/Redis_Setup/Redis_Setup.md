## REDIS installation
1. install redis and change file permission in each node.
~~~bash
sudo apt-get install redis-server -y
sudo chmod 755 /etc/redis -R
~~~

2. configuration.
~~~bash
sudo nano /etc/redis/redis.conf
~~~

- in rpi0:
    - change line `bind 127.0.0.1 -::1` to `bind 127.0.0.1 -::1 10.42.0.250`
        
    - change `protected-mode yes` to `protected-mode no`

- in worker nodes:
    - change line `bind 127.0.0.1 -::1` to `bind 127.0.0.1 -::1 10.42.0.25x` x=1/2/3 for rpi1/2/3

    - Find the line `# replicaof <masterip> <masterport>` and replace as `replicaof 10.42.0.250 6379`

    - change `protected-mode yes` to `protected-mode no`

3. restart redis in every node.
~~~bash
sudo systemctl restart redis.service
~~~

4. test in master node.
~~~bash
redis-cli
INFO replication
~~~
should show the info of 3 connected slaves.
