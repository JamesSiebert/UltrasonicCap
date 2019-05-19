import smbus
import time

last_movement = 100
move_counter = 0

bus = smbus.SMBus(1)

# MAG3110 I2C address 0x0E
# Select Control register, 0x10(16)
bus.write_byte_data(0x0E, 0x10, 0x01)

time.sleep(0.5)

# MAG3110 I2C address 0x0E
# Read data back from 0x01(1), 6 bytes
data = bus.read_i2c_block_data(0x0E, 0x01, 6)

# Convert the data
xMag = data[0] * 256 + data[1]
if xMag > 32767:
    xMag -= 65536

yMag = data[2] * 256 + data[3]
if yMag > 32767:
    yMag -= 65536

zMag = data[4] * 256 + data[5]
if zMag > 32767:
    zMag -= 65536

# Output data
print("X-Axis : %d" % xMag)
print("Y-Axis : %d" % yMag)
print("Z-Axis : %d" % zMag)


def compass_init():
    global bus
    print('Compass Init')
    bus = smbus.SMBus(1)
    # MAG3110 I2C address 0x0E
    # Select Control register, 0x10(16)
    bus.write_byte_data(0x0E, 0x10, 0x01)
    time.sleep(0.5)


def get_compass():
    # MAG3110 I2C address 0x0E
    # Read data back from 0x01(1), 6 bytes
    data = bus.read_i2c_block_data(0x0E, 0x01, 6)

    # Convert the data
    xMag = data[0] * 256 + data[1]
    if xMag > 32767:
        xMag -= 65536

    yMag = data[2] * 256 + data[3]
    if yMag > 32767:
        yMag -= 65536

    zMag = data[4] * 256 + data[5]
    if zMag > 32767:
        zMag -= 65536

    # Output data
    print('----------------------------')
    movement = (xMag + yMag + zMag)
    if movement == 0:
        compass_init()
        get_compass()
    return movement


def is_moving(movement):
    global last_movement
    global move_counter

    variance = 100
    max_count = 100

    if (movement > (last_movement + variance)) or (movement < (last_movement - variance)):
        # print('Movement Detected')
        move_counter = 0
    else:
        move_counter = move_counter + 1
        # print('No Movement - Count = ' + str(move_counter))

    last_movement = movement

    if move_counter >= max_count:
        return 'POWER SAVE ON'
    else:
        return 'POWER SAVE OFF - Standby Count = ' + str(move_counter)


while True:

    time.sleep(1)
    try:
        print(get_compass())
        print(is_moving(get_compass()))
    except:
        print('Compass Error - If persists power compass off and on & reboot script')


