# Homework 7 - Neural face detection pipeline

### Overview
The objective of this homework is simple: modify the processing pipeline that you implemented in 
[homework 3](https://github.com/MIDS-scaling-up/v2/blob/master/week03/hw/README.md) and replace the OpenCV-based face detector with 
a Deep Learning-based one. You could, for instance, rely on what you learned in 
[TensorRT lab 5](https://github.com/MIDS-scaling-up/v2/blob/master/week05/labs/lab_tensorrt.md) or 
[Digits lab 5](https://github.com/MIDS-scaling-up/v2/blob/master/week05/labs/lab_digits.md)


### Files
`face_detect_nn.py` is my implementation of the face detection from hw03 but using a Neural Network, rather than OpenCV
`Dockerfile.hw07` is the Dockerfile I used to make my container. It is essentially the same as the Dockerfile from the week05 Tensorrt lab, but I added the mosquitto client and OpenCV library installs
`hw07_files` contain the files I copied into my docker container
`hw07-hint.ipynb` was provided to us as a hint on how to read in a pretrained model for face detection
The rest of the files are from hw03 for setting up my mosquitto client and broker. Below are a few examples of face detections from my implementation:

![Image 1](https://apikzorianbucket1.s3.us-south.cloud-object-storage.appdomain.cloud/apik_face_hw07_0.png)
![Image 2](https://apikzorianbucket1.s3.us-south.cloud-object-storage.appdomain.cloud/apik_face_hw07_16.png)
![Image 3](https://apikzorianbucket1.s3.us-south.cloud-object-storage.appdomain.cloud/apik_face_hw07_12.png)

Links:
https://apikzorianbucket1.s3.us-south.cloud-object-storage.appdomain.cloud/apik_face_hw07_0.png
https://apikzorianbucket1.s3.us-south.cloud-object-storage.appdomain.cloud/apik_face_hw07_16.png
https://apikzorianbucket1.s3.us-south.cloud-object-storage.appdomain.cloud/apik_face_hw07_12.png

All images can be found under: https://apikzorianbucket1.s3.us-south.cloud-object-storage.appdomain.cloud

### Questions
* Describe your solution in detail.  What neural network did you use? What dataset was it trained on? What accuracy does it achieve?
  - My solution runs through the same pipeline as homework 7, but rather than using OpenCV's face cascade classifier to detect faces, I used a neural network. Specifically, I utilized the mobilenet SSD(single shot multibox detector) based face detector from [yeephycho](https://github.com/yeephycho/tensorflow-face-detection). This was trained on the trained [WIDERFACE dataset](http://mmlab.ie.cuhk.edu.hk/projects/WIDERFace/). I was able to get above 90% accuracy if my face was directly in front of the camera.
  
* Does it achieve reasonable accuracy in your empirical tests? Would you use this solution to develop a robust, production-grade system?
  - This does achieve reasonable accuracy in my epirical tests, but not high enough to use in a production-grade system

* What framerate does this method achieve on the Jetson? Where is the bottleneck?
  - My implementation's frames per second increased more and more as more frames were captured, with a high of 6.5 frames per second, which is about what I was getting with my OpenCV implementation (6.3 fps). The problem is that there is a "warm up" period where the model is loaded and the inference step also takes time. This results in a bottleneck that I did not experience when I used the OpenCV implementation from HW3.

* Which is a better quality detector: the OpenCV or yours?
  - I believe the OpenCV was the better quality detector.

### To turn in:

Please provide answers to questions above, a copy of the code related to the neural face detector along with access to the location (object storage?) containing the detected face images. Note that this homework is NOT graded, credit / no credit only.
