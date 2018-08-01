# Capture & Recognition
# 2018-07-29
# Copyright (c) Cen XIN

from __future__ import print_function
from picamera import PiCamera
import paho.mqtt.client as mqtt
import time
import serial


def on_connect(client, userdata, flags, rc):
    print('Connected.  code is %d.' % (rc))
    client.subscribe('SWST6/to_pi')


def on_message(client, userdata, msg):
    print('received message from server.')
    raw_data = msg.payload
    print(raw_data.decode('utf-8'))
    cmd = raw_data.decode('utf-8')
    ser.write(cmd.encode('utf-8'))


def setup(host_name):
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(username='team6', password='20182018')
    client.connect(host_name)
    client.loop_start()


def load_image(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    return data


def send_image(filename):
    img = load_image(filename)
    client.publish('SWST6/to_server', img)


def main():
    setup('team6.sws3009.bid')

    camera = PiCamera()
    camera.resolution = (1280, 960)
    camera.start_preview()

    try:
        while True:
            camera.capture('image.jpg')
            print(time.asctime(time.localtime(time.time())))
            time.sleep(1)
            send_image('image.jpg')

    except KeyboardInterrupt:
        camera.end_preview()


if __name__ == "__main__":
    client = mqtt.Client()
    ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)
    print('Init succeed!')
    main()
