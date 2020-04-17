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


I then copied the private key from `gpfs1` to the other two, to ensure they had the same key and could communicate with each other

![](https://i.ibb.co/wrDvGms/Screen-Shot-2020-04-17-at-3-09-25-PM.jpg)

I exported the path to the `.bash_profile` file, modified the `/etc/hosts` to include all the nodes with their private keys, and created a node file `/root/noedfile`

After this, I installed the S3 clients

![](https://i.ibb.co/LxDtfLb/Screen-Shot-2020-04-17-at-3-22-41-PM.jpg)

![](https://i.ibb.co/Cw4yVF4/Screen-Shot-2020-04-17-at-3-24-33-PM.jpg)

However, when I tried to install GPFS, I got an error when I tried to call `/usr/lpp/mmfs/5.0.3.2/installer/spectrumscale node add gpfs1 `

![](https://i.ibb.co/RhgfM31/Screen-Shot-2020-04-17-at-4-24-29-PM.jpg)

I tried many ways around this, including editing the `/etc/ssh/sshd_config` (as shown in `HW2`) and tried chamging `PermitRootLogin` to `without-password` but even with this, I am still unable to ssh from one machine to the next. I've tried to get around this bug but have been unable to set up the 3 nodes to be able to communicate, and thus have not been able to move forward with the homework.
