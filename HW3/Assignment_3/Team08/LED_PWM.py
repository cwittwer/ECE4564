import RPi.GPIO as GPIO
import time

redPin   = 36
greenPin = 38
bluePin  = 40
red=None
blue=None
green=None

class LED_PWM:
	def __init__(self):
		GPIO.setmode(GPIO.BOARD)
		GPIO.setwarnings(False)

		GPIO.setup(redPin, GPIO.OUT)
		GPIO.setup(greenPin, GPIO.OUT)
		GPIO.setup(bluePin, GPIO.OUT)

		# GPIO.PWM(pin, frequency)
		global red
		global green
		global blue
		red = GPIO.PWM(redPin, 100)
		green = GPIO.PWM(greenPin, 100)
		blue = GPIO.PWM(bluePin, 100)
		red.start(0)
		green.start(0)
		blue.start(0)

	# Credits to these sources for the code to control an LED on the Pi:
	# http://www.instructables.com/id/Using-a-RPi-to-Control-an-RGB-LED/
	# https://www.youtube.com/watch?v=uUn0KWwwkq8
	def blink(self, pin, intensity):
		if pin == redPin:
			red.ChangeDutyCycle(intensity)
		elif pin == greenPin:
			green.ChangeDutyCycle(intensity)
		elif pin == bluePin:
			blue.ChangeDutyCycle(intensity)
		#GPIO.output(pin, GPIO.HIGH)

	def turnOff(self, pin):
		if pin == redPin:
			red.ChangeDutyCycle(0)
		elif pin == greenPin:
			green.ChangeDutyCycle(0)
		elif pin == bluePin:
			blue.ChangeDutyCycle(0)
		#GPIO.output(pin, GPIO.LOW)
	
	def led_cleanup(self):
		GPIO.cleanup()
