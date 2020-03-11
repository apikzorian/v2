# W251 - Homework 07
# Apik Zorian


# Import libs
import cv2
import sys
import os
import urllib
import tensorflow.contrib.tensorrt as trt

import tensorflow as tf
import numpy as np
import time
import paho.mqtt.client as paho
import sys

# Time to wait next command, avoid blockage
time.sleep(1) 


# Setting variables
FROZEN_GRAPH_NAME = 'data/frozen_inference_graph_face.pb'
IMAGE_PATH = 'data/warriors.jpg'

INPUT_NAME='image_tensor'
BOXES_NAME='detection_boxes'
CLASSES_NAME='detection_classes'
SCORES_NAME='detection_scores'
MASKS_NAME='detection_masks'
NUM_DETECTIONS_NAME='num_detections'
DETECTION_THRESHOLD=0

input_names = [INPUT_NAME]
output_names = [BOXES_NAME, CLASSES_NAME, SCORES_NAME, NUM_DETECTIONS_NAME]

# Load the frozen graph
output_dir=''
frozen_graph = tf.GraphDef()
with open(os.path.join(output_dir, FROZEN_GRAPH_NAME), 'rb') as f:
    frozen_graph.ParseFromString(f.read())

# Optimize the frozen graph using TensorRT

trt_graph = trt.create_inference_graph(
    input_graph_def=frozen_graph,
    outputs=output_names,
    max_batch_size=1,
    max_workspace_size_bytes=1 << 25,
    precision_mode='FP16',
    minimum_segment_size=50
)

# Create session and load graph

tf_config = tf.ConfigProto()
tf_config.gpu_options.allow_growth = True

tf_sess = tf.Session(config=tf_config)

tf.import_graph_def(frozen_graph, name='')

tf_input = tf_sess.graph.get_tensor_by_name(input_names[0] + ':0')
tf_scores = tf_sess.graph.get_tensor_by_name('detection_scores:0')
tf_boxes = tf_sess.graph.get_tensor_by_name('detection_boxes:0')
tf_classes = tf_sess.graph.get_tensor_by_name('detection_classes:0')
tf_num_detections = tf_sess.graph.get_tensor_by_name('num_detections:0')


# Set broker address
broker_addr = "mqtt_broker"
    
# Function to check connection to broker in MQTT
def on_connect(client, userdata, flags, rc):
    print('AZ - Inside on_connect. RC = ' + str(rc))
    
    if rc == 0:
        print("Connection to broker: Success!")
    else:
        print("Connection to broker: Failed!")
        


# Connect to client
client = paho.Client()
client.on_connect = on_connect
client.connect(broker_addr, 1883, 60)


best_scores = []
cap = cv2.VideoCapture(1)
start = time.time()
count = 0
while 1:
    # Detecting and processing pics
    ret, img = cap.read()
    print("Ret = " + str(ret))

    # Resize image
    img = cv2.resize(img, (300, 300), interpolation = cv2.INTER_AREA)
    image_np = np.array(img)


    # Run network on image
    scores, boxes, classes, num_detections = tf_sess.run([tf_scores, tf_boxes, tf_classes, tf_num_detections], feed_dict={
        tf_input: image_np[None, ...]
    })


    boxes = boxes[0]
    scores = scores[0]
    classes = classes[0]
    num_detections = num_detections[0]

    # Get best score's index
    best_score_pos = np.argmax(scores)

    # If the best score is higher than the threshold, publish to broker
    if scores[best_score_pos] >= DETECTION_THRESHOLD:
        best_scores.append(scores[best_score_pos])
        box = boxes[best_score_pos] * np.array([image_np.shape[0], image_np.shape[1], image_np.shape[0], image_np.shape[1]])
        img = cv2.rectangle(img, (int(box[1]), int(box[0])), (int(box[3]),int(box[2])), (255,0,0), 2)
        img = cv2.putText(img, str(scores[best_score_pos]), (int(box[1]), int(box[0])), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        elapsed_time = time.time() - start

        # Display score and frame rate
#        cv2.imshow("frame", img)        
        print("Score: " + str(sum(best_scores)/len(best_scores)))
        print("Frame Rate: " + str(len(best_scores)/elapsed_time))
#        cv2.imwrite("./face_" + str(count) + ".jpg", img)
#        count += 1

        # Try publishing to face_detect/my_topic. If this fails, throw error                
        try:
            print("publishing it!")
            client.publish("face_detect/my_topic", bytearray(cv2.imencode('.png', img)[1]), qos=1)
        except:
            print("Unexpected error:", sys.exc_info()[0])

    # Loop breaking parameter
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

# Pause time
time.sleep(1)

# Stop
cap.release()
cv2.destroyAllWindows()



