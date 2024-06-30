#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from kafka import KafkaConsumer
import json

# Consume the final output data
operator3_topic = "temperatures_ewma"
output_consumer2 = KafkaConsumer(
    operator3_topic,
    bootstrap_servers=['rpi0:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    consumer_timeout_ms=50000
)

print("Final output temperatures (EWMA):")
received_messages = 0
for message in output_consumer2:
    print(message.value)
    received_messages += 1
    if received_messages == 9:  # Note: Change this to match the number of messages you expect 
        break                   # after applying the filter operator and calculating ewma
