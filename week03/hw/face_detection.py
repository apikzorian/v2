# import libs
import numpy as np
import cv2 as cv
import time
import paho.mqtt.client as paho
import sys

# Set broker address
broker_addr = "mqtt_broker"
    
# Function to check connection to broker in MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connection to broker: Success!")
    else:
        print("Connection to broker: Failed!")
        
# Connect to client
client = paho.Client()
client.on_connect = on_connect
client.connect(broker_addr, 1883, 60)

# Time to wait next command, avoid blockage
time.sleep(1) 

# Capture from video (set to 0 to capture from USB camera)
cap = cv.VideoCapture(0)

# XML classifier (local, mounted)
face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

# Start stream
client.loop_start()

# While camera is on, run below
while(True):
    # Capture frame-by-frame from feed
    ret, frame = cap.read()

    # gray here is the gray frame you will be getting from a camera
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    for (x,y,w,h) in faces:        
        gray_crop = gray[y:y+h,x:x+w]
        # Show boxed photo
        cv.imshow("Gray Cropped", gray_crop)

        # Try publishing to face_detect/my_topic. If this fails, throw error                
        try:
            # Publish 
            client.publish("face_detect/my_topic", bytearray(cv.imencode('.png', gray_crop)[1]), qos=1)
        except:
            print("Unexpected error:", sys.exc_info()[0])


    # Close the connection
    if cv.waitKey(1) & 0xFF == ord('q'):
        break


time.sleep(1) 

# Disconnect from client
client.loop_stop()
client.disconnect()

# Close all windows
cap.release()
cv.destroyAllWindows()
