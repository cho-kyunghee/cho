import RPi.GPIO as GPIO
import time

LED = 26

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT) # GPIO.IN

GPIO.output(LED, GPIO.HIGH) # GPIO.HIGH == 1
time.sleep(5)

GPIO.output(LED, GPIO.LOW) # GPIO.LOW == 0