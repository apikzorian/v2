# Homework 3 - Internet of Things 101


## Overall architecture / flow
Your overall application flow / architecture should be something like ![this](hw03.png).  

On the TX2, you should have a mosquitto broker container, based on Alpine linux.  Also, a container for the face detector that connects to the USB webcam, detects faces, and sends them to your internal Mosquitto broker. You should have another container that fetches face files from the internal broker and sends them to the cloud mosquitto broker.  This container should be based on Alpine linux.  In the cloud, you should have a container with a mosquitto broker running inside.  You should also have a container that connects to the cloud mosquitto broker, gets face messages, and puts them into the object storage.

## Submission
Please point us to the repository of your code and provide an http link to the location of your faces in the object storage.  Also, explan the naming of the MQTT topics and the QoS that you used.

### Some hints
1. See Week 1's lab (https://github.com/MIDS-scaling-up/v2/blob/master/week01/lab/Dockerfile.yolo) for how to install openCV.
2. To make storing in Object Store easier, look at https://github.com/s3fs-fuse/s3fs-fuse

## Note on cloud usage
![Soflayer](../../softlayer.png?raw=true "Title")


