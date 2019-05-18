# This is the main script
import I2C_LCD_driver
import UltrasonicSensor
import RPi.GPIO as GPIO
import time

# Pi Board Setup
GPIO.setmode(GPIO.BCM)

# LCD
mylcd = I2C_LCD_driver.lcd()

# Ultrasonic Init
usF = UltrasonicSensor(1, 2)
usR = UltrasonicSensor(1, 2)
usB = UltrasonicSensor(1, 2)
usL = UltrasonicSensor(1, 2)







mylcd.lcd_display_string("Hello World!", 1)

GPIO.cleanup()
