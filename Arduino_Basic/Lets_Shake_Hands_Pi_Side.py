# Let's Shake Hands!
# 2018-07-24
# Copyright (c) Cen XIN

import serial

ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)

ser.write('a'.encode('utf-8'))

try:
    while 1:
        response = ser.readline()
        answer = response.decode('utf-8')
        if answer == 'b':
            print(answer)
            ser.write('b'.encode('utf-8'))
            print('Arduino Online')
            break
        else:
            print(answer)

except KeyboardInterrupt:
    ser.close()
