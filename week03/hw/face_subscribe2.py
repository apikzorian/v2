# Packages import
import numpy as np
import cv2
import paho.mqtt.client as paho
import sys
import ibm_cloud_utils
import os

import ibm_boto3
from ibm_botocore.client import Config

# List object credentials
cos_credentials={
  "apikey": "M2vVCP3n-GibcrdUvC_9p56VnwwhRK0diIK1U-zrBohj",
  "endpoints": "https://iam.cloud.ibm.com/identity/token",
  "iam_apikey_description": "Auto-generated for key a6c2c756-a419-4e36-95b9-606cfb22b6b0",
  "iam_apikey_name": "apikzorianbucket1",
  "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Writer",
  "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/0440d900927541e98236cd4faaa71c3a::serviceid:ServiceId-e9ec582f-3ed2-4a15-97a9-aa0ee1a5c714",
  "resource_instance_id": "crn:v1:bluemix:public:cloud-object-storage:global:a/0440d900927541e98236cd4faaa71c3a:3667a31b-8e2f-4d5b-b9fa-9bfe337ba1c0::"
}


cos = ibm_boto3.resource('s3',
                         ibm_api_key_id=cos_credentials['apikey'],
                         ibm_service_instance_id=cos_credentials['resource_instance_id'],
                         ibm_auth_endpoint="https://iam.cloud.ibm.com/identity/token",
                         config=Config(signature_version='oauth'),
                         endpoint_url="https://s3.us-south.cloud-object-storage.appdomain.cloud")

broker_addr = "169.62.51.136"
output_dir = "./my_faces/"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connection to broker: Success!")
        client.subscribe("face_detect/my_topic")
    else:
        print("Connection to broker: Failed!")

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed")
# Start counter
count = 0

def on_message(client, userdata, msg):

    global count # Counter for image naming
    print("Got image!")

    # Image decode
    f = np.frombuffer(msg.payload, dtype='uint8')
    face = cv2.imdecode(f, flags=1)
    cur_dir = os.getcwd()
    

    # Create unique file name, increment counter
    file_name = "my_face_" + str(count) + ".png"
    count = count + 1

    print("Saving image: " + str(file_name))
    # Save image
    bucket_name = 'apikzorianbucket1'
    cos.Bucket(name='apikzorianbucket1').put_object(Key=file_name, Body=msg.payload)

# Connect to MQTT client
client= paho.Client()
client.on_subscribe = on_subscribe
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_addr, 1883, 60)

# Loop until stream ends
client.loop_forever()
