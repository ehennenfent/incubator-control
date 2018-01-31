from Adafruit_DHT import read_retry, AM2302
import RPi.GPIO as GPIO
import time

class Incubator(object):
    
    def __init__(self, ambient_temp):
        self.tick()
        self.ambient_temp = ambient_temp
        self.duty_cycle = 0
        self._tictime = time.time()
        self.uptime = 1

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(12, GPIO.OUT)
        GPIO.setup(13, GPIO.OUT)
        
        self.p_12 = GPIO.PWM(12, 50)
        self.p_13 = GPIO.PWM(13, 50)
        
        self.p_12.start(0)
        self.p_13.start(0)

        self.rolling_temp = []

    def tick(self, tictime=0):
        self.hum_1, self.temp_1 = read_retry(AM2302, 14)
        self.hum_2, self.temp_2 = read_retry(AM2302, 15)
        
        self.rolling_temp = self.rolling_temp[-4:]
        self.rolling_temp.append((self.temp_1 + self.temp_2) / 2.0)
        
        self.tictime = time.time()

    @property
    def temp(self):
        smoothed = list(filter(lambda k: (k >= 5) and (k =< 70), self.rolling_temp))
        return sum(smoothed) / float(len(smoothed))

    def cleanup(self):
        try:
            self.set_duty_cycle(0)
            self.p_12.stop()
            self.p_13.stop()
            self.uptime = 0
            print("Heater powered off safely")
        except:
            print("Uh oh! Couldn't power off the heater")
        try:
            GPIO.cleanup()
            print("Cleaned up GPIO Pins")
        except:
            print("Couldn't clean up GPIO pins!")

    def set_duty_cycle(self, new_duty_cycle):
        if new_duty_cycle > 1 or new_duty_cycle < 0:
            raise ValueError("Duty cycle must be between 0 and 1")
        self.duty_cycle = new_duty_cycle
        _scaled = self.duty_cycle * 100
        
        self.p_12.ChangeDutyCycle(_scaled)
        self.p_13.ChangeDutyCycle(_scaled)
        
    def stable_duty_cycle(self, target_temp):
        return abs(-.00257 * (target_temp - self.ambient_temp)) / (.00208 * (58.5 - target_temp))