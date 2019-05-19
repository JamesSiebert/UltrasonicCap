import I2C_LCD_driver       # Blue LCD Controller
import RPi.GPIO as GPIO     # GPIO import
import time                 # Import time module
import pygame               # import pygame for audio
import os                   # Import OS for terminal commands (webcam)


# Pi setup
max_ping_dist = 200  # measured in cm
switch_active = True
loop_frequency = 1

# Pi Board Setup
GPIO.setmode(GPIO.BCM)

# LCD Setup
mylcd = I2C_LCD_driver.lcd()
mylcd.lcd_display_string("BOOTING UP...", 1)

# GPIO Pin Setup Declaration (white TRIG | red ECHO(resistor))
fTrig = 24
fEcho = 27
rTrig = 5
rEcho = 12
bTrig = 17
bEcho = 18
lTrig = 6
lEcho = 13
switch1 = 20
switch2 = 16

# Front Ultrasonic
GPIO.setup(fTrig, GPIO.OUT)  # Trig
GPIO.setup(fEcho, GPIO.IN)   # Echo

# Right Ultrasonic
GPIO.setup(rTrig, GPIO.OUT)  # Trig
GPIO.setup(rEcho, GPIO.IN)  # Echo

# Back Ultrasonic
GPIO.setup(bTrig, GPIO.OUT)  # Trig
GPIO.setup(bEcho, GPIO.IN)   # Echo

# Left Ultrasonic
GPIO.setup(lTrig, GPIO.OUT)  # Trig
GPIO.setup(lEcho, GPIO.IN)  # Echo

# Switch
GPIO.setup(switch1, GPIO.IN)  # Option 1
GPIO.setup(switch2, GPIO.IN)  # Option 2
# GPIO.setup(switch1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #Option 1
# GPIO.setup(switch2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #Option 2

# PyGame Sounds Setup
pygame.init()
ping_sound = pygame.mixer.Sound("/home/pi/UltrasonicCap/ping.wav")
front_sound = pygame.mixer.Sound("/home/pi/UltrasonicCap/front.wav")
left_sound = pygame.mixer.Sound("/home/pi/UltrasonicCap/left.wav")
back_sound = pygame.mixer.Sound("/home/pi/UltrasonicCap/back.wav")
right_sound = pygame.mixer.Sound("/home/pi/UltrasonicCap/right.wav")
photo_sound = pygame.mixer.Sound("/home/pi/UltrasonicCap/photo.wav")
nav_sound = pygame.mixer.Sound("/home/pi/UltrasonicCap/ping.wav")


def get_distance(trig, echo):
    """ This function is responsible for returning the distance for each ultrasonic."""
    pulse_start = 0
    pulse_end = 0

    # Ensure that the sensor has settled down before read
    GPIO.output(trig, False)
    time.sleep(0.1)

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


def play_sound(type, volL, volR):
    """ This handles the sound playing though the use of PyGame. """
    if type == 'pingLR':
        pygame.mixer.Sound.play(ping_sound).set_volume(volL, volR)
    elif type == 'pingL':
        pygame.mixer.Sound.play(left_sound).set_volume(volL, volR)
    elif type == 'pingR':
        pygame.mixer.Sound.play(right_sound).set_volume(volL, volR)
    elif type == 'pingF':
        pygame.mixer.Sound.play(front_sound).set_volume(volL, volR)
    elif type == 'pingB':
        pygame.mixer.Sound.play(back_sound).set_volume(volL, volR)
    elif type == 'photo':
        pygame.mixer.Sound.play(photo_sound)
    elif type == 'ping':
        pygame.mixer.Sound.play(nav_sound)


def dist_to_vol(dist):
    """ This function handles the distance to volume percentage conversion.
    max_ping_dist refers to the furthest distance the unit should report items."""
    if dist > max_ping_dist:
        return 0.01
    else:
        return 1 - (dist * 0.005)


def ping_all():
    """ This function is used to handle pinging all directions at once. """

    # Gets the rounded distance for each Ultrasonic direction
    dist_f = round(get_distance(fTrig, fEcho))
    dist_r = round(get_distance(rTrig, rEcho))
    dist_b = round(get_distance(bTrig, bEcho))
    dist_l = round(get_distance(lTrig, lEcho))

    # Console output
    print('F ' + str(dist_f) + 'cm | R ' + str(dist_r) + 'cm | B ' + str(dist_b) + 'cm | L ' + str(dist_l) + 'cm')

    # LCD Output distances to line 3 (format as XXXX XXXX XXXX XXXX )
    mylcd.lcd_display_string(str(dist_f).zfill(4) + ' ' + str(dist_r).zfill(4) + ' ' + str(dist_b).zfill(4) + ' ' + str(dist_r).zfill(4) + ' ', 3)

    # Play Sounds
    play_sound('pingLR', dist_to_vol(dist_l), dist_to_vol(dist_r))
    play_sound('pingF', dist_to_vol(dist_f), dist_to_vol(dist_f))
    play_sound('pingB', dist_to_vol(dist_b), dist_to_vol(dist_b))

def check_inputs():
    """ This function is used to check for user inputs, in our case it is switch input 1 & 2. """
    global switch_active

    if switch_active:
        if GPIO.input(switch1) == GPIO.HIGH:
            switch_active = False
            print("Switch 1 pressed - Capture Photo")
            mylcd.lcd_display_string('Capture Photo', 4)

            os.system('fswebcam -r 1920x1080 -S 3 --jpeg 92 --save /home/pi/UltrasonicCap/capture.jpg')

            mylcd.lcd_display_string('      STANDBY       ', 4)
            switch_active = True

        if GPIO.input(switch2) == GPIO.HIGH:
            switch_active = False
            print("Switch 2 pressed - Access Compass")
            mylcd.lcd_display_string('Compass - N 11 deg', 4)

            time.sleep(2)

            mylcd.lcd_display_string('      STANDBY       ', 4)
            switch_active = True


mylcd.lcd_display_string("----- VIS 3000 ------", 1)
""" The main program loop. """
while True:

    check_inputs()
    ping_all()
    time.sleep(loop_frequency)

GPIO.cleanup()
