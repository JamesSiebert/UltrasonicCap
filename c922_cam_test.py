import os
# FSWEBCAM -r (resolution) -s (Skip - for errors) - https://www.mankier.com/1/fswebcam
os.system('fswebcam -r 1920x1080 -S 3 --jpeg 92 --save /home/pi/UltrasonicCap/capture.jpg')