# Packages import
import numpy as np
import cv2
import paho.mqtt.client as paho
import sys


broker_addr = "169.62.51.136"
output_dir = "./"
    
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connection to broker: Success!")
        client.subscribe("face_detect/my_topic")
    else:
        print("Connection to broker: Failed!")

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed")
    print("QOS = " + str(granted_qos))

# Start counter
count = 0

def on_message(client, userdata, msg):    
    
    global count # Counter for image naming
    print("Got image!")
    
    # Image decode
    f = np.frombuffer(msg.payload, dtype='uint8')
    face = cv2.imdecode(f, flags=1)
    
    # Create unique file name, increment counter
    file_name = output_dir + "/my_face_" + str(count) + ".png"
    count = count + 1
    
    print("Saving image: " + str(file_name))
    # Save image
    #cv.imwrite(file_name, face)
    
# Connect to MQTT client
client= paho.Client()
client.on_subscribe = on_subscribe
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_addr, 1883, 60)

# Loop until stream ends
client.loop_forever()