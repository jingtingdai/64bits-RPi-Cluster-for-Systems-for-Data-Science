#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from kafka import KafkaProducer
import json
import time

# Helper function to convert Celsius to Fahrenheit
def celsius_to_fahrenheit(celsius_temp):
    return (celsius_temp * 9/5) + 32

# Kafka producer configuration
producer = KafkaProducer(
    bootstrap_servers=['rpi0:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Input temperature data in Celsius
input_data = [7, 6, 9, 14, 12, 17, 9, 13, 11, 12, 13, 16, 16, 19]

# Apply the first operator: Convert Celsius to Fahrenheit
operator1_topic = "temperatures_fahrenheit"
for temp in input_data:
    fahrenheit_temp = celsius_to_fahrenheit(temp)
    producer.send(operator1_topic, fahrenheit_temp)
    print(f"Sent to {operator1_topic}: {fahrenheit_temp}")
    time.sleep(3)