#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from kafka import KafkaConsumer
import random

def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def add_random_noise(fahrenheit):
    return fahrenheit + random.uniform(-1, 1)

def round_noised(fahrenheit_noised):
    return round(fahrenheit_noised)

consumer = KafkaConsumer(
    'temperature',
    bootstrap_servers='rpi0:9092',
    value_deserializer=lambda x: int(x.decode('utf-8'))
)


for message in consumer:
    temp_celsius = message.value
    temp_fahrenheit = celsius_to_fahrenheit(temp_celsius)
    temp_fahrenheit_noised = add_random_noise(temp_fahrenheit)
    temp_rounded = round_noised(temp_fahrenheit_noised)
    print(f"Received: {temp_celsius}°C ({temp_fahrenheit:.1f}°F) - Noised: {temp_fahrenheit_noised:.1f}°F - Rounded: {temp_rounded:.1f}°F")
