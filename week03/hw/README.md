# Homework 3 - Internet of Things 101


### Overall architecture / flow
![this](hw03.png).  



### On the Jetson

I first ran `Cloud_Docker_Install.sh` to make sure Docker was installed available. Next, i build my 2 images for my 2 types of containers on my Jetson: One face detection image (built on Ubuntu) and one Mosquitto image (built on Alpine), the latter of which would be used for the broker and forwarder containers.

```
docker build --network=host -t az_ub -f Dockerfile.ub .
docker build --network=host -t az_mosq -f Dockerfile.mosq
```

Once this was ready, I was ready to run my Docker container for face detection

```
!xhost + local:root
sudo docker run --user=root --env="DISPLAY" --name face_detect --privileged --network face_net -v "$PWD":/hw3_vol -v="/tmp/.X11-unix:/tmp/.X11-unix:rw" -ti az_ub bash
```

Once the bash was open, I ran `face_detection.py` which accessed my camera on my Jetson, took images, cropped out the face, and sent them to my mosquitto broker.

Next, I built my two containers for Mosquitto. I created a bridge so that they could communicate

```
docker network create --driver bridge face_net
docker run --name mqtt_broker --network face_net -p :1883 -v "$PWD":/HW03 -d az_mosq sh -c "mosquitto -c /HW03/mqtt_broker.conf"
docker run --name mqtt_forwarder --network face_net -v "$PWD":/HW03 -d az_mosq sh -c "mosquitto -c /HW03/mqtt_forwarder.conf"
```

From `face_detection`, I published the images to `face_detect/my_topic`, but in the `.conf` files for my broker and forwarder, I made sure to use a wildcard for `face_detect/#` as my topic, to allow all messages under `face_detect` to be forwarded. I published messages using QOS=1, which guarantees that the message will be delievered at least once. This is a safe QOS to use and while it does mean that a subscriber can receive a message multiple times, the end goal is to upload these images to IBM cloud which is able to handle duplicates.

### On the Cloud

I initiaited my IBM cloud instance and installed Docker (via `Cloud_Docker_Install.sh`). I built a Docker image for my cloud instances, one which would be a forwarder and the other which would take the received messages from my Jetson and upload them to the cloud.


```
docker build -t az_cloud -f Dockerfile.cloud .
```

I then spun up both of my containers. The forwarder container would simply have its port open and pass the processing to `mqtt_saver`. 

```
docker run --name mosquitto -p 1883:1883 -d az_cloud mosquitto
docker run --name mqtt_saver --rm -v $HOME/v2/week03/hw:/hw03 -it az_cloud sh
```

From here, I had a bash open to run the following python script:
```
python3 face_subscribe.py
```
This script takes all of the messages sent to topic `face_detect/#` and uploads them to my ibm cloud. I used `face_detect/#` as it is a wildcard which allows us to access any level of topics under `face_detect`. I used the ibm SDK to upload my images. Below is a sample of some of the images uploaded.
