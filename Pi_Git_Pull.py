import os
import time

# Project UltrasonicCap

# Pi
# localDir = '/home/pi/UltrasonicCap/'

# PC
localDir = 'C:/_griffith/Robotics/UltrasonicCap'

git = 'https://github.com/JamesSiebert/UltrasonicCap.git'
push_and_pull = False

# If this script allows Git Push
print('Auto Pull Project')
if push_and_pull:
    command = input('enter "push" OR "pull"')
else:
    command = 'pull'

# Pull Command
if command == 'pull':
    print('Git Pull Started')
    os.system("cd " + localDir)
    os.system("git pull origin master")
    print('Git Pull Complete')

# Push Command
if command == 'push':
    print('Git Push Started')
    os.system("cd " + localDir)
    os.system("git push origin master")
    print('Git Push Complete')

time.sleep(5)
print('COMPLETE')