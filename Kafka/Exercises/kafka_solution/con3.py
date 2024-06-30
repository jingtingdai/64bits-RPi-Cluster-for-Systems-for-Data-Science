#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from kafka import KafkaConsumer, KafkaProducer
import json

def moving_average(window_values):
    return sum(window_values) / len(window_values)

producer = KafkaProducer(
    bootstrap_servers=['rpi0:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

operator2_topic = "temperatures_above_threshold"
operator4_topic = "temperatures_moving_average"
consumer3 = KafkaConsumer(
    operator2_topic,
    bootstrap_servers=['rpi0:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    consumer_timeout_ms=50000
)

window_size = 3
window_values = []

received_messages = 0
for message in consumer3:
    window_values.append(message.value)
    if len(window_values) == window_size:
        average_temp = moving_average(window_values)
        producer.send(operator4_topic, average_temp)
        print(f"Sent to {operator4_topic}: {average_temp}")
        window_values.pop(0)
        received_messages += 1
    if received_messages == 8:  # Note: Change this to match the number of messages you expect after applying the filter operator and calculating moving average
        break
