# Hermes Control
# 2018-07-25
# Copyright (c) Cen XIN

import serial
import time

ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)

print('Init succeed!')

try:
    while True:
        cmd = input()
        if cmd == 'q':
            print('Quit from control...')
            break;
        elif cmd[0] == 'w' or cmd[0] == 's' or cmd[0] == 'a' or cmd[0] == 'd' or cmd[0] == 'x':
                ser.write(cmd.encode('utf-8'))
                print('Processing...')
        else:
            print('Wrong command! Try again...')

except KeyboardInterrupt:
    ser.close()
