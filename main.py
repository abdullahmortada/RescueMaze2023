import RPi.GPIO as gpio
import time as t

m1a = 6
m1b = 27
m1 = 13
m2a = 22
m2b = 26
m2 = 12
p1 = gpio.PWM(m1, 1000)
p2 = gpio.PWM(m2, 1000)
p1.start(50)
p2.start(50)


def init():
    gpio.setmode(gpio.BCM)
    gpio.setup(m1a, gpio.OUT)
    gpio.setup(m1b, gpio.OUT)
    gpio.setup(m2a, gpio.OUT)
    gpio.setup(m2b, gpio.OUT)
    gpio.setup(m1, gpio.OUT)
    gpio.setup(m2, gpio.OUT)
    gpio.output(m1, gpio.HIGH)
    gpio.output(m2, gpio.HIGH)


def forward():
    p1.ChangeDutyCycle(50)
    p2.ChangeDutyCycle(50)
    gpio.output(m1a, gpio.HIGH)
    gpio.output(m1b, gpio.LOW)
    gpio.output(m2a, gpio.HIGH)
    gpio.output(m2b, gpio.LOW)


def stop():
    gpio.output(m1a, gpio.LOW)
    gpio.output(m1b, gpio.LOW)
    gpio.output(m2a, gpio.LOW)
    gpio.output(m2b, gpio.LOW)


def left(secs = 60):
    #2 Options
    #Option 1 - Time Feed back
    start = t.time()
    while t.time()-start < secs:
        gpio.output(m1a, gpio.LOW)
        gpio.output(m1b, gpio.HIGH)
        gpio.output(m2a, gpio.HIGH)
        gpio.output(m2b, gpio.LOW)
    #Option 2 - Heading Feedback
    initHeading = mpu.readAngle() #find library for the mpu
    currentHeading = initHeading
    while abs(initHeading - currentHeading) not in range(85, 96):
        currentHeading = mpu.readAngle()
        gpio.output(m1a, gpio.LOW)
        gpio.output(m1b, gpio.HIGH)
        gpio.output(m2a, gpio.HIGH)
        gpio.output(m2b, gpio.LOW)
    stop()


def right(secs = 60):
    # 2 Options
    # Option 1 - Time Feed back
    start = t.time()
    while t.time()-start < secs:
        gpio.output(m1a, gpio.HIGH)
        gpio.output(m1b, gpio.LOW)
        gpio.output(m2a, gpio.LOW)
        gpio.output(m2b, gpio.HIGH)
    # Option 2 - Heading Feedback
    initHeading = mpu.readAngle()  # find library for the mpu
    currentHeading = initHeading
    while abs(initHeading - currentHeading) not in range(85, 96):
        currentHeading = mpu.readAngle()
        gpio.output(m1a, gpio.HIGH)
        gpio.output(m1b, gpio.LOW)
        gpio.output(m2a, gpio.LOW)
        gpio.output(m2b, gpio.HIGH)
    stop()


def leftturn(x):
    timeToTurn = 3    #time required for the turn
    startTime= t.time()
    while t.time - startTime < timeToTurn:
        forward()
    stop()
    left(x)

def rightturn(x):
    timeToTurn = 3  # time required for the turn
    startTime = t.time()
    while t.time - startTime < timeToTurn:
        forward()
    stop()
    right(x)


while True:
    init()
    forward()
    if left_dist > 10:
        stop()
        leftturn(2)
    elif left_dist < 10 and front_dist < 10:
        stop()
        right(2)
    elif left_dist < 10 and front_dist < 10 and right_dist < 10:
        stop()
        left(2)
        left(2)