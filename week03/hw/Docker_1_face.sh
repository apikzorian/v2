#!/bin/bash
!xhost + local:root
#sudo docker run --user=root --env="DISPLAY" --name face_detect2 --privileged --network face_net -v "$PWD":/hw3_vol -ti az_ub bash

sudo docker run --user=root --env="DISPLAY" --name face_detect3 --privileged --network face_net -v "$PWD":/hw3_vol -v="/tmp/.X11-unix:/tmp/.X11-unix:rw" -ti az_ub bash
