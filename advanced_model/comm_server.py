# Server Communication (Tensorflow side & Pi side)
# 2018-07-31
# Copyright (c) Cen XIN & Logan Zhou

import threading
import struct
import os
import io
import sys
import time
import paho.mqtt.client as mqtt
from multiprocessing import Process, JoinableQueue, Event
import obj_detect

IM_WIDTH = 1280
IM_HEIGHT = 960

client = mqtt.Client()


def on_connect(client, userdata, flags, rc):
    print('Connected with result code %d' % rc)
    client.subscribe('SWST6/to_server')


def on_message(client, userdata, msg):
    print('Received message.')
    image = msg.payload
    images_queue.put(image)
    time.sleep(1)
    if results_queue.empty() is False:
        result_dict = results_queue.get()
        send_command(result_dict)
    else:
        pass


def send_command(result_dict):
    boxes = result_dict['boxes'][0]
    scores = result_dict['scores'][0]
    classes = result_dict['classes'][0]
    num = result_dict['num'][0]

    obj_num = int(num)

    person_num = 0
    vehicle_num = 0
    is_fire_hydrant = False
    is_stop = False
    left = 0
    right = IM_WIDTH
    top = 0
    bottom = IM_HEIGHT

    for i in range(obj_num):
        obj_id = classes[i]
        print(obj_id)
        if obj_id == 1:
            person_num = person_num + 1
        if obj_id == 2 or obj_id == 3 or obj_id == 4 or obj_id == 6 or obj_id == 8:
            vehicle_num = vehicle_num + 1
        if obj_id == 11:
            is_fire_hydrant = True
            (ymin, xmin, ymax, xmax) = boxes[i]
            (left, right, top, bottom) = (
                int(xmin * IM_WIDTH),
                int(ymax * IM_WIDTH),
                int(ymin * IM_HEIGHT),
                int(ymax * IM_HEIGHT))
        if obj_id == 13:
            is_stop = True

    print('width = %d  height = %d' % (IM_WIDTH, IM_HEIGHT))
    hydrant_position = (left + right) / 2
    mid_x = (left + right) / 2
    mid_y = (top + bottom) / 2
    # print('obj_num = %d' % obj_num)
    # print("centre = (%d, %d)" % (mid_x, mid_y))
    # print(person_num)
    # print(vehicle_num)
    print('Persons = %d, Vehicles = %d' % (person_num, vehicle_num))
    # print(is_fire_hydrant)
    # print(is_stop)
    if is_fire_hydrant is True:
        if hydrant_position < (IM_WIDTH / 3):
            client.publish('SWST6/to_pi', 'a 5'.encode('utf-8'))
        elif hydrant_position > (2 * IM_WIDTH / 3):
            client.publish('SWST6/to_pi', 'd 5'.encode('utf-8'))
        else:
            client.publish('SWST6/to_pi', 'w 1 50'.encode('utf-8'))
    elif is_stop is True:
        client.publish('SWST6/to_pi', 'x'.encode('utf-8'))
    else:
        client.publish('SWST6/to_pi', 'a 2'.encode('utf-8'))


def setup(host_name):
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(username='team6', password='20182018')
    client.connect(host_name)
    client.loop_start()


if __name__ == '__main__':
    setup('team6.sws3009.bid')
    images_queue = JoinableQueue()
    results_queue = JoinableQueue()
    tf_process = Process(target=obj_detect.tensorflow_worker, args=(images_queue, results_queue))

    tf_process.start()
