# Packages import
import numpy as np
import cv2
import paho.mqtt.client as paho
import sys


broker_addr = "169.62.51.136"
output_dir = "./"
    
# Create methods for connections and subscription of messages
def on_connect(client, userdata, flags, rc):
    print("Connected to broker!")
    print("RC = "+str(rc))
    client.subscribe("face_app/test")

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
    
    # Save image
    cv.imwrite(file_name, face)
    
# Connect to MQTT client
client= paho.Client()
client.connect(broker_addr, 1883, 60)
client.on_connect = on_connect
client.on_message = on_message

# Loop until stream ends
client.loop_forever()