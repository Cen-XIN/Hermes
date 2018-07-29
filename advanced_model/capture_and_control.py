# Capture & Recognition
# 2018-07-29
# Copyright (c) Cen XIN

from __future__ import print_function
from picamera import PiCamera
import paho.mqtt.client as mqtt
import time
import os
import serial


def get_img_size(file_path):
    fsize = os.path.getsize(file_path)
    fsize = fsize / float(1024)
    return round(fsize, 2)


def on_connect(client, userdata, flags, rc):
    print('Connected.  code is %d.' % (rc))
    client.subscribe('SWS3009TEAM6/PI')


def on_message(client, userdata, msg):
    print('received message from server.')
    global cmd
    instruct_info = msg.payload.decode('utf-8')
    print(instruct_info)
    if instruct_info is 'w':
        cmd = 'w'
    if instruct_info is 'x':
        cmd = 'x'

    ser.write(cmd.encode('utf-8'))


def setup(host_name):
    global client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(username='team6', password='20182018')
    client.connect(host_name)
    client.loop_start()


def load_image(filename):
    with open(filename, 'rb') as f:
        data=f.read()
    return data


def send_image(filename):
    img = load_image(filename)
    client.publish('SWS3009TEAM6/PIBACK', img)


def main():
    # global resp_callback

    setup('team6.sws3009.bid')
    # resp_callback = resp_handler

    camera = PiCamera()
    camera.resolution = (1280, 960)
    camera.start_preview()
    
    try:
        while True:
            camera.capture('image.jpg')
            if get_img_size('./image.jpg') < 700:
                continue
            else:
                # print("waiting for 2s")
                # print("Sending picture")
                send_image('image.jpg')
                print(time.asctime(time.localtime(time.time())))

    except KeyboardInterrupt:
        camera.end_preview()


if __name__ == "__main__":
    ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)
    print('Init succeed!')
    main()

