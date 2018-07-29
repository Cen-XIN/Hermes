# Object Detection (Receive Image & Send Results)
# 2018-07-29
# Copyright (c) Cen XIN

from __future__ import print_function
import paho.mqtt.client as mqtt

import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tensorflow as tf
import time

from collections import defaultdict
from io import StringIO
from PIL import Image

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")
from object_detection.utils import ops as utils_ops
from utils import label_map_util
from utils import visualization_utils as vis_util

# The model used in object detection
MODEL_NAME = 'ssd_mobilenet_v1_coco_2018_01_28'

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')

# Total classes the model can detect
NUM_CLASSES = 90

# Target image path
IMAGE_PATH = 'tmp/image.jpg'

# Load label and index
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                            use_display_name = True)
category_index = label_map_util.create_category_index(categories)

detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')


def load_image_into_numpy_array(image, im_width, im_height):
    return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)


def run_inference_for_single_image(image, graph):
    with graph.as_default():
        with tf.Session() as sess:
            # Get handles to input and output tensors
            ops = tf.get_default_graph().get_operations()
            all_tensor_names = {output.name for op in ops for output in op.outputs}
            tensor_dict = {}
            for key in [
                'num_detections', 'detection_boxes', 'detection_scores',
                'detection_classes', 'detection_masks'
            ]:
                tensor_name = key + ':0'
                if tensor_name in all_tensor_names:
                    tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
                        tensor_name)
            if 'detection_masks' in tensor_dict:
                # The following processing is only for single image
                detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
                detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
                # Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
                real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
                detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
                detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
                detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
                    detection_masks, detection_boxes, image.shape[0], image.shape[1])
                detection_masks_reframed = tf.cast(
                    tf.greater(detection_masks_reframed, 0.5), tf.uint8)
                # Follow the convention by adding back the batch dimension
                tensor_dict['detection_masks'] = tf.expand_dims(
                    detection_masks_reframed, 0)
            image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

            # Run inference
            output_dict = sess.run(tensor_dict,
                                   feed_dict={image_tensor: np.expand_dims(image, 0)})

            # all outputs are float32 numpy arrays, so convert types as appropriate
            output_dict['num_detections'] = int(output_dict['num_detections'][0])
            output_dict['detection_classes'] = output_dict[
                'detection_classes'][0].astype(np.uint8)
            output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
            output_dict['detection_scores'] = output_dict['detection_scores'][0]
            if 'detection_masks' in output_dict:
                output_dict['detection_masks'] = output_dict['detection_masks'][0]
        sess.close()
    return output_dict


def on_connect(client, userdata, flags, rc):
    print('Connected with result code %d.' % rc)
    client.subscribe('SWS3009TEAM6/PIBACK')


def on_message(client, userdata, msg):
    # global model
    print('Received message. Writting to %s.' % IMAGE_PATH)
    img = msg.payload
    print('msg.payload executed...')
    with open(IMAGE_PATH, 'wb') as f:
        f.write(img)
    # time.sleep(2)
    print('write executed...')

    # image = Image.open(IMAGE_PATH)
    with Image.open(IMAGE_PATH) as image:
        print('open executed...')
        im_width, im_height = image.size
        image_np = load_image_into_numpy_array(image, im_width, im_height)
        image_np_expanded = np.expand_dims(image_np, axis=0)
        output_dict = run_inference_for_single_image(image_np, detection_graph)
        vis_util.visualize_boxes_and_labels_on_image_array(
            image_np,
            output_dict['detection_boxes'],
            output_dict['detection_classes'],
            output_dict['detection_scores'],
            category_index,
            instance_masks=output_dict.get('detection_masks'),
            use_normalized_coordinates=True,
            line_thickness=8)
        obj_num = output_dict['num_detections']

        person_num = 0
        vehicle_num = 0
        is_fire_hydrant = False
        is_stop = False
        # left = 0
        # right = im_width
        # top = 0
        # bottom = im_height
        hydrant_position = 0

        for i in range(obj_num):
            obj_id = category_index[output_dict['detection_classes'][i]]['id']
            if obj_id == 1:
                person_num = person_num + 1
            if obj_id == 2 or obj_id == 3 or obj_id == 4 or obj_id == 6 or obj_id == 8:
                vehicle_num = vehicle_num + 1
            if obj_id == 11:
                is_fire_hydrant = True
                (ymin, xmin, ymax, xmax) = output_dict['detection_boxes'][i]
                (left, right, top, bottom) = (
                    int(xmin * im_width),
                    int(ymax * im_width),
                    int(ymin * im_height),
                    int(ymax * im_height))
                hydrant_position = (left + right) / 2
            if obj_id == 13:
                is_stop = True

        print(hydrant_position)
        cmd = 'x'
        if is_fire_hydrant is True:
            cmd = 'w'
            '''
            if hydrant_position < (im_width / 3):
                cmd = 'a'
            elif hydrant_position > (2 * im_width / 3):
                cmd = 'd'
            else
                cmd = 'w'
            '''
        if is_stop is True:
            cmd = 'x'

        client.publish('SWS3009TEAM6/PI', cmd.encode('utf-8'))

        # print("width = %d  height = %d" % (im_width, im_height))
        # mid_x = (left + right) / 2
        # mid_y = (top + bottom) / 2
        # print("centre = (%d, %d)" % (mid_x, mid_y))

        '''
        # To calculate the density of crowd
        person_num = 0
        vehicle_num = 0
        min_left = 0
        max_right = im_width
        min_top = 0
        max_bottom = im_height
        sum_human_area = 0

        for i in range(obj_num):
            obj_id = category_index[output_dict['detection_classes'][i]]['id']
            if obj_id == 1:
                (ymin, xmin, ymax, xmax) = output_dict['detection_boxes'][i]
                (left, right, top, bottom) = (
                    int(xmin * im_width),
                    int(ymax * im_width),
                    int(ymin * im_height),
                    int(ymax * im_height))

                sum_human_area += (right - left) * (bottom - top)
                print(sum_human_area)

                if left > min_left:
                    min_left = left
                if right < max_right:
                    max_right = right
                if top > min_top:
                    min_top = top
                if bottom < max_bottom:
                    max_bottom = bottom

                person_num = person_num + 1
                continue

            if obj_id == 2 or obj_id == 3 or obj_id == 4 or obj_id == 6 or obj_id == 8:
                vehicle_num = vehicle_num + 1
                continue

        total_human_area = (max_bottom - min_top) * (max_right - min_left)
        dense_ratio = sum_human_area / total_human_area

        print(person_num)
        print('Crowd density = %d  Vehicle num = %f' % (dense_ratio, vehicle_num))
        client.publish('SWS3009TEAM6/PI', person_num)
        '''

def setup(client, host_name):
    # global detection_graph
    # global label_map
    # global categories
    # global category_index
    # Load graph
    # detection_graph = tf.Graph()
    # with detection_graph.as_default():
    #     od_graph_def = tf.GraphDef()
    #     with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    #         serialized_graph = fid.read()
    #         od_graph_def.ParseFromString(serialized_graph)
    #         tf.import_graph_def(od_graph_def, name='')
    # label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    # categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
    #                                                             use_display_name=True)
    # category_index = label_map_util.create_category_index(categories)
    # client = mqtt.Client()

    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(username='team6', password='20182018')
    client.connect(host_name)
    client.loop_start()


def main():
    client = mqtt.Client()
    setup(client, 'team6.sws3009.bid')

    try:
        while True:
            pass

    except KeyboardInterrupt:
        client.disconnect()


if __name__ == '__main__':
    main()
