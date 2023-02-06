import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)

TRIG1 = 5
ECHO1 = 6

GPIO.setup(TRIG1, GPIO.OUT)
GPIO.setup(ECHO1, GPIO.IN)

GPIO.output(TRIG1, False)

TRIG2 = 8
ECHO2 = 7

GPIO.setup(TRIG2, GPIO.OUT)
GPIO.setup(ECHO2, GPIO.IN)

GPIO.output(TRIG2, False)

TRIG3 = 16
ECHO3 = 26

GPIO.setup(TRIG3, GPIO.OUT)
GPIO.setup(ECHO3, GPIO.IN)

GPIO.output(TRIG3, False)

def find_dist(trig, echo):
    # Wait for sensor to settle
    time.sleep(2)

    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)
    
    while GPIO.input(echo) == 0:
        pulse_start = time.time()
    
    while GPIO.input(echo) == 1:
        pulse_end = time.time()
        
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    
    return distance


def main():
    cm1 = find_dist(TRIG1, ECHO1)
    cm2 = find_dist(TRIG2, ECHO2)
    cm3 = find_dist(TRIG3, ECHO3)
    print(f"distance1(cm) : {cm1}")
    print(f"distance2(cm) : {cm2}")
    print(f"distance3(cm) : {cm3}")
    GPIO.cleanup()
    
    
if __name__ == "__main__":
    main()


