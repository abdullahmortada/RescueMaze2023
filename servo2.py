import RPi.GPIO as GPIO

from time import sleep


GPIO.setmode(GPIO.BCM)
SERVO = 4
GPIO.setup(SERVO, GPIO.OUT)

pwm=GPIO.PWM(SERVO, 50)
pwm.start(0)

pwm.ChangeDutyCycle(5) # left -90 deg position
sleep(1)
pwm.ChangeDutyCycle(7.5) # neutral position
sleep(1)
pwm.ChangeDutyCycle(10) # right +90 deg position
sleep(1)

pwm.stop()
GPIO.cleanup()
