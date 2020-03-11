# Homework 7 - Neural face detection pipeline

### Overview
The objective of this homework is simple: modify the processing pipeline that you implemented in 
[homework 3](https://github.com/MIDS-scaling-up/v2/blob/master/week03/hw/README.md) and replace the OpenCV-based face detector with 
a Deep Learning-based one. You could, for instance, rely on what you learned in 
[TensorRT lab 5](https://github.com/MIDS-scaling-up/v2/blob/master/week05/labs/lab_tensorrt.md) or 
[Digits lab 5](https://github.com/MIDS-scaling-up/v2/blob/master/week05/labs/lab_digits.md)

### Hints
* You have the freedom to choose the neural network that does the detection, but don't overthink it; this is a credit / no credit assignment that is not supposed to take a lot of time.
* There is no need to train the network in this assignment, just find and use a pre-trained model that is trained on a face dataset.
* Your neural detector should run on the Jetson.
* Just like the OpenCV detector, your neural detector needs to take a frame as input and return an array of rectangles for each face detected.
* Most neural object detectors operate on a frame of a given size, so you may need to resize the frame you get from your webcam to that resolution.
* Note that face detection is not the same as face recognition; you don't need to discriminate between different faces
* Here's a [sample notebook](hw07-hint.ipynb) that loads and uses [one face detector](https://github.com/yeephycho/tensorflow-face-detection)
* A more graceful solution would involve using a face detector from [TensorFlow's Model Zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md) -- [this network](http://download.tensorflow.org/models/object_detection/facessd_mobilenet_v2_quantized_320x320_open_image_v4.tar.gz), to be exact, but at the moment, simply loading it as we did in [TensorRT lab 5](https://github.com/MIDS-scaling-up/v2/blob/master/week05/labs/lab_tensorrt.md)  does not work due to [this bug](https://stackoverflow.com/questions/53563976/tensorflow-object-detection-api-valueerror-anchor-strides-must-be-a-list-wit)

### Questions
* Describe your solution in detail.  What neural network did you use? What dataset was it trained on? What accuracy does it achieve?
  - My solution runs through the same pipeline as homework 7, but rather than using OpenCV's face cascade classifier to detect faces, I used a neural network. Specifically, I utilized the mobilenet SSD(single shot multibox detector) based face detector from [yeephycho](https://github.com/yeephycho/tensorflow-face-detection). This was trained on the trained [WIDERFACE dataset](http://mmlab.ie.cuhk.edu.hk/projects/WIDERFace/). I was able to get above 90% accuracy if my face was directly in front of the camera.
  
* Does it achieve reasonable accuracy in your empirical tests? Would you use this solution to develop a robust, production-grade system?
  - This does achieve reasonable accuracy in my epirical tests, but not high enough to use in a production-grade system

* What framerate does this method achieve on the Jetson? Where is the bottleneck?
  - My implementation's frames per second increased more and more as more frames were captured, with a high of 6.5 frames per second, which is about what I was getting with my OpenCV implementation (6.3 fps). The problem is that there is a "warm up" period where the model is loaded and the inference step also takes time. This results in a bottleneck that I did not experience when I used the OpenCV implementation from HW3.

* Which is a better quality detector: the OpenCV or yours?
  - I believe the OpenCV was the better quality detector

### To turn in:

Please provide answers to questions above, a copy of the code related to the neural face detector along with access to the location (object storage?) containing the detected face images. Note that this homework is NOT graded, credit / no credit only.
