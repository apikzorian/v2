# Homework 12

## Overview

I tried to follow the instructions for setting up the 3 nodes but was unable to get them to communicate with each other

I started by setting up 3 servers using the same key. They have 2 CPUs and a 25 and 100 GB disk:

```
ibmcloud sl vs create --hostname=gpfs1 --domain=server.cloud --cpu=2 --memory=4096 --datacenter=wdc04 --san --os=UBUNTU_16_64 --disk=25 --disk=100 key=<key>
ibmcloud sl vs create --hostname=gpfs2 --domain=server.cloud --cpu=2 --memory=4096 --datacenter=wdc04 --san --os=UBUNTU_16_64 --disk=25 --disk=100 key=<key>
ibmcloud sl vs create --hostname=gpfs3 --domain=server.cloud --cpu=2 --memory=4096 --datacenter=wdc04 --san --os=UBUNTU_16_64 --disk=25 --disk=100 key=<key>
```

![](https://i.ibb.co/7vwbj2z/Screen-Shot-2020-04-17-at-2-27-20-PM.jpg)
