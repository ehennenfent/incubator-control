#!/usr/bin/python
# Copyright 2017 CypherCon Biohacking Village
# Author: Eric Hennenfent (@ehennenfent)

from ubidots import ApiClient
from secrets import master_incubator_token
from Adafruit_DHT import read_retry, AM2302
import RPi.GPIO as GPIO
import time
import traceback

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
            print("Found variable %s: %s" % (variable.label, variable.id))
            return variable
    raise Exception("Could not find variable %s!" % label)

def get_time():
    return int(time.time() * 1000)

temperature_1 = get_variable('temperature-1')
temperature_2 = get_variable('temperature-2')
humidity_1 = get_variable('humidity-1')
humidity_2 = get_variable('humidity-2')
heater_1 = get_variable('heater-1')
heater_2 = get_variable('heater-2')
uptime = get_variable('uptime')

last_avg_temp = 0.0

def toggle_heater_state():
    global HEATER_IS_ON
    if HEATER_IS_ON:
        print("Turning heater off at {0:0.1f} degrees C".format(last_avg_temp))
        GPIO.output(12, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)
        HEATER_IS_ON = False
    else:
        print("Turning heater on at {0:0.1f} degrees C".format(last_avg_temp))
        GPIO.output(12, GPIO.HIGH)
        GPIO.output(13, GPIO.HIGH)
        HEATER_IS_ON = True

def write_sensor_data(temp1, temp2, hum1, hum2, heat1, heat2):
    timestamp = get_time()

    try:
        api.save_collection([
            {'variable': temperature_1.id, 'value': temp1, timestamp:timestamp},
            {'variable': temperature_2.id, 'value': temp2, timestamp:timestamp},
            {'variable': humidity_1.id, 'value': hum1, timestamp:timestamp},
            {'variable': humidity_2.id, 'value': hum2, timestamp:timestamp},
            {'variable': heater_1.id, 'value': heat1, timestamp:timestamp},
            {'variable': heater_2.id, 'value': heat2, timestamp:timestamp},
            {'variable': uptime.id, 'value': 1, timestamp:timestamp}])
    except:
        print("Error saving data to ubidots")
        traceback.print_exc()


print("Beginning main event loop")
while(True):
    try:
        hum_1, temp_1 = read_retry(AM2302, 14)
        hum_2, temp_2 = read_retry(AM2302, 15)
        last_avg_temp = (temp_1 + temp_2) / 2

        if HEATER_IS_ON and (last_avg_temp > 30.2):
            toggle_heater_state()

        if not HEATER_IS_ON and (last_avg_temp < 29.8):
            toggle_heater_state()

        hs = 1 if HEATER_IS_ON else 0
        write_sensor_data(temp_1, temp_2, hum_1, hum_2, hs, hs)

        time.sleep(5)
    except:
        print("Program exiting! Turning heater off...")
        try:
            GPIO.output(12, GPIO.LOW)
            GPIO.output(13, GPIO.LOW)
            HEATER_IS_ON = False
            print("Turned heater off safely")
        except:
            print("Uh oh! Couldn't power off the heater")
        try:
            GPIO.cleanup()
            print("Cleaned up GPIO Pins")
        except:
            print("Couldn't clean up GPIO pins!")
        raise
