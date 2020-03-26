# Homework 11 -- More fun with OpenAI Gym!

## Intro

In this homework, I training a Lunar Lander to land properly **using my Jetson TX2**

There are two python scripts used for this process. The first file, `lunar_lander.py`, defines the Lunar Lander for OpenAI Gym. It also defines the keras model. The second file, `run_lunar_lander.py`, instantiates the Lunar Lander environment and runs it.


## Set Up
To run the environment, use these commands (ensure you have all the files from the hw11 github folder in your current directory):

```
sudo docker build -t lander -f Dockerfile.lander .
xhost +
sudo docker run -it --rm --net=host --runtime nvidia  -e DISPLAY=$DISPLAY -v /tmp/.X11-unix/:/tmp/.X11-unix:rw --privileged -v /tmp/videos:/tmp/videos lander
```

You will have a lot of mp4 files in `/tmp/videos` on your TX2. You can use VLC to watch the videos of your landing attempts to see the improvement of your model over the iterations.

## Results
You should upload two or three videos showing your best model to Cloud Object Storage and provide links using the instructions below.

Also, submit a write-up of the tweaks you made to the model and the effect they had on the results. What parameters did you change? Did they improve or degrade the model?

Grading is based on the changes made and the observed output, not on the accuracy of the model.

We will compare results in class.

## Results

### What parameters did you change? 

#### Round 1: Default 

```
At step  50000
reward:  -0.1858525493990155
total rewards  244.11681345794963
```

### Round 2: 

### What values did you try? 

### Did you try any other changes that made things better or worse? Did they improve or degrade the model?


### Based on what you observed, what conclusions can you draw about the different parameters and their values?


#### Enable http access to Cloud Object Storage

```
Here's how to enable http access to the S3 COS:
1) create a bucket & upload a file, remember the resiliency you pick and the location
2) Go to Buckets -> Access Policies -> Public Access
3) click the "Create access policy" button
4) Go to Endpoint (on the left menu) and select your resiliency to find your endpoint (mine was "Regional" because that's how I created my COS)
5) Your endpoint is the Public location plus your bucket name plus the file

Example: https://s3.eu-gb.cloud-object-storage.appdomain.cloud/brooklyn-artifacts/IBM_MULTICLOUD_MANAGER_3.1.2_KLUS.tar.gz

In this example, the bucket is "brooklyn-artifacts" and the single Region is eu-gb
```
