import RPi.GPIO as GPIO
import time


def init():
    GPIO.setmode(GPIO.BCM)

    TRIG = 23
    ECHO = 24

    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    GPIO.output(TRIG, False)

def find_dist():
    # Wait for sensor to settle
    time.sleep(2)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
        
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    
    return distance


def main():
    init()
    cm = find_dist()
    print(f"distance(cm) : {cm}")
    
    
if __name__ == "__main__":
    main()

