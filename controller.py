#!/usr/bin/python
# Copyright 2017 CypherCon Biohacking Village
# Author: Eric Hennenfent (@ehennenfent)

from ubidots import ApiClient
from secrets import master_incubator_token
from Adafruit_DHT import read_retry, AM2302
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)

HEATER_IS_ON = False

api = ApiClient(token=master_incubator_token)

incubator = api.get_datasource('5a224554c03f9721f59934ff')
variables = incubator.get_variables()

def get_variable(label):
    for variable in variables:
        if str(variable.label) == label:
            return variable
    raise Exception("Could not find variable %s!" % label)
    
def toggle_heater_state():
    if HEATER_IS_ON:
        GPIO.output(12, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)
        HEATER_IS_ON = False
    else:
        GPIO.output(12, GPIO.HIGH)
        GPIO.output(13, GPIO.HIGH)
        HEATER_IS_ON = True

temperature_1 = api.get_variable('temperature-1')
temperature_2 = api.get_variable('temperature-2')
humidity_1 = api.get_variable('humidity-1')
humidity_2 = api.get_variable('humidity-2')
heater_1 = api.get_variable('heater-1')
heater_2 = api.get_variable('heater-2')
uptime = api.get_variable('uptime')

last_avg_temp = 0.0

def write_sensor_data(temp1, temp2, hum1, hum2, heat1, heat2):
    timestamp = time.time()
    
    temperature_1.save_value({'value': temp1, timestamp:timestamp})
    temperature_2.save_value({'value': temp2, timestamp:timestamp})
    humidity_1.save_value({'value': hum1, timestamp:timestamp})
    humidity_2.save_value({'value': hum2, timestamp:timestamp})
    heater_1.save_value({'value': heat1, timestamp:timestamp})
    heater_2.save_value({'value': heat2, timestamp:timestamp})
    uptime.save_value({'value': 1, timestamp:timestamp})
    

while(True):
    try:
        hum_1, temp_1 = Adafruit_DHT.read_retry(AM2302, 14)
        hum_2, temp_2 = Adafruit_DHT.read_retry(AM2302, 15)
        last_avg_temp = (temp_1 + temp_2) / 2
        
        if HEATER_IS_ON and (last_avg_temp > 30.2):
            toggle_heater_state()
        
        if not HEATER_IS_ON and (last_avg_temp < 29.8):
            toggle_heater_state()
        
        hs = 1 if HEATER_IS_ON else 0
        write_sensor_data(temp_1, temp_2, hum_1, hum_2, hs, hs)
        
        time.sleep(5)
    except:
        print("Something terrible happened!")
        raise