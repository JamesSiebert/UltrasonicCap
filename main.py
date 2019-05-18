# This is the main script
import I2C_LCD_driver
# import UltrasonicSensor
import RPi.GPIO as GPIO
import time
import pygame

# Pi setup
loop = True

# Pi Board Setup
GPIO.setmode(GPIO.BCM)

# LCD
mylcd = I2C_LCD_driver.lcd()
mylcd.lcd_display_string("BOOT UP...", 1)

# GPIO Pin Setup
fTrig = 1
fEcho = 1
rTrig = 5
rEcho = 12
bTrig = 1
bEcho = 1
lTrig = 24
lEcho = 27
switch1 = 16
switch2 = 20

# Front Ultrasonic
# GPIO.setup(fTrig, GPIO.OUT)  # Trig
# GPIO.setup(fTrig, GPIO.IN)   # Echo

# Right Ultrasonic
GPIO.setup(rTrig, GPIO.OUT)  # Trig
GPIO.setup(rTrig, GPIO.IN)   # Echo

# Back Ultrasonic
# GPIO.setup(bTrig, GPIO.OUT)  # Trig
# GPIO.setup(bTrig, GPIO.IN)   # Echo

# Left Ultrasonic
GPIO.setup(lTrig, GPIO.OUT)  # Trig
GPIO.setup(lTrig, GPIO.IN)   # Echo

# Switch
GPIO.setup(switch1, GPIO.IN)  #Option 1
GPIO.setup(switch2, GPIO.IN)  #Option 2
# GPIO.setup(switch1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #Option 1
# GPIO.setup(switch2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #Option 2

# PyGame Sounds Setup
pygame.init()
ping_sound = pygame.mixer.Sound("/home/pi/UltrasonicCap/ping.wav")
photo_sound = pygame.mixer.Sound("/home/pi/UltrasonicCap/ping.wav")
nav_sound = pygame.mixer.Sound("/home/pi/UltrasonicCap/ping.wav")

def get_distance(trig, echo):
    pulse_start = 0
    pulse_end = 0

    # Ensure that the sensor has settled down before read
    GPIO.output(trig, False)
    time.sleep(2)

    # START OF READ PROCESS

    # Turns ultrasonic on then off
    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)

    # While the Echo pin reads 0 set pulse_start to current time.
    while GPIO.input(echo) == 0:
        pulse_start = time.time()

    # Once the echo pin reads 1, set pulse end to time to current time.
    while GPIO.input(echo) == 1:
        pulse_end = time.time()

    # Calculates the duration of the ultrasonic pulse
    pulse_duration = pulse_end - pulse_start

    # Calculates the distance based on the ultrasonic duration time.
    distance = round((pulse_duration * 17150), 2)

    return distance


def play_sound(type):
    if type == 'ping':
        pygame.mixer.Sound.play(ping_sound)
    elif type == 'photo':
        pygame.mixer.Sound.play(photo_sound)
    elif type == 'ping':
        pygame.mixer.Sound.play(nav_sound)


while loop:
    play_sound('ping')
    time.sleep(1)
    print(get_distance(rTrig, rEcho))
    mylcd.lcd_display_string(str(get_distance(rTrig, rEcho)), 1)



GPIO.cleanup()
