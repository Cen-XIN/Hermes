# Hermes Control Terminal (Beta)
# 2018-07-27
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
            time.sleep(1)
        elif cmd[0] == 'r': # Reserved for future use
            ser.write(cmd.encode('utf-8'))
            print('Reading sensor info...')
            time.sleep(1)
            resp = ser.readline()

            sonar_1 = 0
            sonar_2 = 0
            sonar_3 = 0
            
            raw_data = resp.split()

            sonar_1 = int(raw_data[0])
            sonar_2 = int(raw_data[1])
            sonar_3 = int(raw_data[2])

            print(sonar_1)
            print(sonar_2)
            print(sonar_3)

        else:
            print('Wrong command! Try again...')

except KeyboardInterrupt:
    ser.close()
