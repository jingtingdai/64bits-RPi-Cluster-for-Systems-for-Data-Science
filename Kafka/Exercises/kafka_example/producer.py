#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from kafka import KafkaProducer
import time

producer = KafkaProducer(bootstrap_servers='rpi0:9092')

temperature_data = [20, 21, 19, 22, 25, 18, 23, 24, 26, 17]

for temp in temperature_data:
    producer.send('temperature', str(temp).encode('utf-8'))
    print(f"Sent: {temp}°C")
    time.sleep(1)

producer.flush()
producer.close()
