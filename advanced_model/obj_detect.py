# Tensorflow Working Factory
# 2018-07-30
# Copyright (c) Logan Zhou & Cen XIN

import numpy as np
import os
import sys
import tensorflow as tf
from PIL import Image
import io

tf.logging.set_verbosity(tf.logging.INFO)
sys.path.append("..")

from object_detection.utils import ops as utils_ops
from utils import label_map_util
from utils import visualization_utils as vis_util


def load_image_into_numpy_array(image, im_width, im_height):
    # (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)

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


def tensorflow_worker(images_queue, results_queue):
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                                use_display_name=True)
    category_index = label_map_util.create_category_index(categories)

    with detection_graph.as_default():
        with tf.Session(graph=detection_graph) as sess:
            # Definite input and output Tensors for detection_graph
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            # Each box represents a part of the image where a particular object was detected.
            detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            # Each score represent how level of confidence for each of the objects.
            # Score is shown on the result image, together with the class label.
            detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
            detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')

            while True:
                image_tmp = images_queue.get()
                image = Image.open(io.BytesIO(image_tmp))
                # the array based representation of the image will be used later in order to prepare the
                # result image with boxes and labels on it.
                (im_width, im_height) = image.size
                image_np = load_image_into_numpy_array(image, im_width, im_height)
                # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                image_np_expanded = np.expand_dims(image_np, axis=0)
                # Actual detection.
                (boxes, scores, classes, num) = sess.run(
                    [detection_boxes, detection_scores, detection_classes, num_detections],
                    feed_dict={image_tensor: image_np_expanded})

                result_dict = {
                    'boxes': boxes,
                    'scores': scores,
                    'classes': classes,
                    'num': num
                }

                results_queue.put(result_dict)
