# Real Time View (via Raspberry Pi Camera)
# 2018-07-25
# Copyright (c) Cen XIN

from picamera import PiCamera, Color
from time import sleep

car_camera = PiCamera()

car_camera.start_preview()

while True:
    m = input()
    if m == 'q':
        break

car_camera.stop_preview()
