import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

class IPAManager:
    def __init__(self, trig, echo):
        GPIO.setup(trig, GPIO.OUT)
        GPIO.setup(echo, GPIO.IN)

        self.ipa_dict = {}
        self.trig = trig
        self.echo = echo


    def get_distance(self):
        pulse_start = 0
        pulse_end = 0

        # Ensure that the sensor has settled down before read
        GPIO.output(self.trig, False)
        time.sleep(2)

        # START OF READ PROCESS

        # Turns ultrasonic on then off
        GPIO.output(self.trig, True)
        time.sleep(0.00001)
        GPIO.output(self.trig, False)

        # While the Echo pin reads 0 set pulse_start to current time.
        while GPIO.input(self.echo) == 0:
            pulse_start = time.time()

        # Once the echo pin reads 1, set pulse end to time to current time.
        while GPIO.input(self.echo) == 1:
            pulse_end = time.time()

        # Calculates the duration of the ultrasonic pulse
        pulse_duration = pulse_end - pulse_start

        # Calculates the distance based on the ultrasonic duration time.
        distance = round((pulse_duration * 17150), 2)

        return distance

