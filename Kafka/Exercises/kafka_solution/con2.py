#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from kafka import KafkaConsumer, KafkaProducer
import json

def ewma(new_temp, old_temp, alpha=0.5):
    return alpha * new_temp + (1 - alpha) * old_temp

producer = KafkaProducer(
    bootstrap_servers=['rpi0:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

operator2_topic = "temperatures_above_threshold"
operator3_topic = "temperatures_ewma"
consumer2 = KafkaConsumer(
    operator2_topic,
    bootstrap_servers=['rpi0:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    consumer_timeout_ms=50000
)

received_messages = 0
previous_temp = None
for message in consumer2:
    if previous_temp is None:
        previous_temp = message.value
    else:
        ewma_temp = ewma(message.value, previous_temp)
        producer.send(operator3_topic, ewma_temp)
        print(f"Sent to {operator3_topic}: {ewma_temp}")
        previous_temp = ewma_temp
        received_messages += 1
    if received_messages == 9:  # Note: Change this to match the number of messages you expect after applying the filter operator
        break
