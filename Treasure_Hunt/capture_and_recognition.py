# Capture & Recognition
# 2018-07-27
# Copyright (c) Fuzhao XUE & Cen XIN

from __future__ import print_function
from picamera import PiCamera
import paho.mqtt.client as mqtt
import time

resp_callback = None


def on_connect(client, userdata, flags, rc):
    print('Connected.  code is %d.' % (rc))
    client.subscribe('IMAGE/predict')


def on_message(client, userdata, msg):
    print('received message from server.')

    str = msg.payload.decode('UTF-8')
    str = str.split(':')
    if resp_callback is not None:
        resp_callback(str[0], float(str[1]), int(str[2]))


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
    client.publish('IMAGE/classify', img)


def resp_handler(label, prob, index):
    print('\n -- Response -- \n')
    print('Label: %s' % label)
    print('Probability: %3.4f' % prob)
    print('Index %d' % index)


def main():
    global resp_callback

    setup('team6.sws3009.bid')
    resp_callback = resp_handler

    camera = PiCamera()
    camera.resolution = (256, 256)
    camera.start_preview()
    
    try:
        while True:
            camera.capture('treasure.jpg')
            # print("waiting for 2s")
            time.sleep(2)
            # print("Sending picture")
            send_image('treasure.jpg')
            print(time.asctime(time.localtime(time.time())))

    except KeyboardInterrupt:
        camera.end_preview()


if __name__ == "__main__":
    main()

