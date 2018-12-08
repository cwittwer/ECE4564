import RPi.GPIO as GPIO
import time


class LED:

	def __init__(self):
		GPIO.setmode(GPIO.BOARD)
		GPIO.setwarnings(False)
		print('GPIO init')
		self.output_list = [36,38,40]
		GPIO.setup(self.output_list, GPIO.OUT)
		GPIO.output(self.output_list, GPIO.LOW)
	
	def led_cleanup(self):
		GPIO.cleanup()

	def blink_red(self, red):
		while red: #100s, pin 27
			GPIO.output(36, 1)
			time.sleep(.5)
			GPIO.output(36, 0)
			time.sleep(.5)
			red = red - 1
	def blink_green(self, green):
		while green: #10s, pin 28
			GPIO.output(38, 1)
			time.sleep(.5)
			GPIO.output(38, 0)
			time.sleep(.5)
			green = green - 1
	def blink_blue(self, blue):
		while blue: #1's pin 29
			GPIO.output(40, 1)
			time.sleep(.5)
			GPIO.output(40, 0)
			time.sleep(.5)
			blue = blue - 1