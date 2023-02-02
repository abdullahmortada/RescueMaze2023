#!/usr/bin/env python
# -*- coding: utf-8 -*-


import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

# define I/O pins
S0 = 27  # S0 TSC3200 GPIO27 Raspberry Pi
S1 = 22  # S1 TSC3200 GPIO22 Raspberry Pi
S2 = 23  # S2 TSC3200 GPIO23 Raspberry Pi
S3 = 24  # S3 TSC3200 GPIO24 Raspberry Pi
OUT = 25 # OUT TSC3200 GPIO25 Rasperry Pi


GPIO.setmode(GPIO.BCM)
GPIO.setup(OUT,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(S0,GPIO.OUT)
GPIO.setup(S1,GPIO.OUT)
GPIO.setup(S2,GPIO.OUT)
GPIO.setup(S3,GPIO.OUT)

# regulate frequency of capture (2% maximum)
GPIO.output(S0,GPIO.LOW)
GPIO.output(S1,GPIO.HIGH)

def measure():
    time.sleep(0.1)
    delay = time.time()
    for impulse_count in range(10):
        GPIO.wait_for_edge(OUT, GPIO.FALLING)
    return time.time() - delay      
   
while True:  

    GPIO.output(S2,GPIO.LOW)
    GPIO.output(S3,GPIO.LOW)
    blue = measure()
    print("Blue: ", blue)

    GPIO.output(S2,GPIO.LOW)
    GPIO.output(S3,GPIO.HIGH)
    red = measure()
    print("Red: ", red)

    GPIO.output(S2,GPIO.HIGH)
    GPIO.output(S3,GPIO.HIGH)
    green = measure()
    print("Green: ", green)
  
    GPIO.output(S2,GPIO.HIGH)
    GPIO.output(S3,GPIO.LOW)
    total = measure()
    print("No Filter: ",total)
  
    if blue >= 0.05 and red <= 0.03 and green <= 0.04:
        print("blue tile")
    elif blue >= 0.08 and red >= 0.08 and green >= 0.08:
        print("black tile")
    elif blue <= 0.017 and red <= 0.017 and green <= 0.017:
        print("white tile")
      
    print("\n")
    time.sleep(1)