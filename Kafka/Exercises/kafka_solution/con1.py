#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from kafka import KafkaConsumer, KafkaProducer
import json

def filter_above_threshold(temp, threshold=50):
    return temp > threshold

producer = KafkaProducer(
    bootstrap_servers=['rpi0:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

operator1_topic = "temperatures_fahrenheit"
operator2_topic = "temperatures_above_threshold"
consumer1 = KafkaConsumer(
    operator1_topic,
    bootstrap_servers=['rpi0:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    consumer_timeout_ms=50000
)

received_messages = 0
for message in consumer1:
    if filter_above_threshold(message.value):
        producer.send(operator2_topic, message.value)
        print(f"Sent to {operator2_topic}: {message.value}")
        received_messages += 1
    if received_messages == 10:
        break
