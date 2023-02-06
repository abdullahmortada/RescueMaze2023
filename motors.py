import RPi.GPIO as GPIO
import time as t

m1a = 23
m1b = 24
m1 = 25
#m2a = 22
#m2b = 26
#m2 = 12

RO = 17 # encoder pin

GPIO.setmode(GPIO.BCM)

#set up encoder pin
GPIO.setup(RO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# set up motor
GPIO.setup(m1, GPIO.OUT)
#GPIO.setup(m2, GPIO.OUT)
GPIO.output(m1, GPIO.HIGH)
#GPIO.output(m2, GPIO.HIGH)
GPIO.setup(m1a, GPIO.OUT)
GPIO.setup(m1b, GPIO.OUT)
#GPIO.setup(m2a, GPIO.OUT)
#GPIO.setup(m2b, GPIO.OUT)
p1 = GPIO.PWM(m1, 1000)
#p2 = GPIO.PWM(m2, 1000)
p1.start(50)
#p2.start(50)



def forward():
    p1.ChangeDutyCycle(50)
    #p2.ChangeDutyCycle(50)
    GPIO.output(m1a, GPIO.HIGH)
    GPIO.output(m1b, GPIO.LOW)
    #GPIO.output(m2a, GPIO.HIGH)
    #GPIO.output(m2b, GPIO.LOW)


def stop():
    GPIO.output(m1a, GPIO.LOW)
    GPIO.output(m1b, GPIO.LOW)
    #GPIO.output(m2a, GPIO.LOW)
    #GPIO.output(m2b, GPIO.LOW)


def left(secs = 60):
    #2 Options
    #Option 1 - Time Feed back
    start = t.time()
    while t.time()-start < secs:
        GPIO.output(m1a, GPIO.LOW)
        GPIO.output(m1b, GPIO.HIGH)
        GPIO.output(m2a, GPIO.HIGH)
        GPIO.output(m2b, GPIO.LOW)
    #Option 2 - Heading Feedback
    initHeading = mpu.readAngle() #find library for the mpu
    currentHeading = initHeading
    while abs(initHeading - currentHeading) not in range(85, 96):
        currentHeading = mpu.readAngle()
        GPIO.output(m1a, GPIO.LOW)
        GPIO.output(m1b, GPIO.HIGH)
        GPIO.output(m2a, GPIO.HIGH)
        GPIO.output(m2b, GPIO.LOW)
    stop()


def right(secs = 60):
    # 2 Options
    # Option 1 - Time Feed back
    start = t.time()
    while t.time()-start < secs:
        GPIO.output(m1a, GPIO.HIGH)
        GPIO.output(m1b, GPIO.LOW)
        GPIO.output(m2a, GPIO.LOW)
        GPIO.output(m2b, GPIO.HIGH)
    # Option 2 - Heading Feedback
    initHeading = mpu.readAngle()  # find library for the mpu
    currentHeading = initHeading
    while abs(initHeading - currentHeading) not in range(85, 96):
        currentHeading = mpu.readAngle()
        GPIO.output(m1a, GPIO.HIGH)
        GPIO.output(m1b, GPIO.LOW)
        GPIO.output(m2a, GPIO.LOW)
        GPIO.output(m2b, GPIO.HIGH)
    stop()
    
def main():
    stateLast = GPIO.input(RO)
    rotationCount = 0
    stateCount = 0
    stateCountTotal = 0
    
    circ = 20.4203 #cm
    statesPerRot = 40
    distPerStep = circ/statesPerRot
    
    
    forward()
    
    try:
        while True:
            stateCurrent = GPIO.input(RO)
            if stateCurrent != stateLast:
                stateLast = stateCurrent
                stateCount += 1
                stateCountTotal += 1
                
            if stateCount == statesPerRot:
                rotationCount += 1
                stateCount = 0
                
            distance = distPerStep * stateCountTotal
            print(f"distance(cm) : {distance}")
    
    except KeyboardInterrupt: #ctrl c
        stop()
        GPIO.cleanup()    

if __name__ == "__main__":
    main()
    