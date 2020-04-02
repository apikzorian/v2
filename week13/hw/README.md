# Homework 13: Deep Learning SDK (the unofficial one, by Dustin Franklin)

In this homework, used transfer learning to create a model that classifies plants, directly on my TX2

## Setting up

* Review the [github repo](https://github.com/dusty-nv/jetson-inference)
* Review the Docker file (Dockerfile.inf) required the build the container
* Try building on the TX2, e.g. ``` docker build -t inf -f Dockerfile.inf .``` This will take a few minutes.
* Start the container in interactive mode, e.g.
```
# this needs to be done on the jetson
xhost +
docker run --rm --privileged -v /tmp:/tmp -v /data:/data -v /var:/var -v /home/nvidia/models:/models --net=host --ipc=host --env DISPLAY=$DISPLAY -ti w251/inf:dev-tx2-4.2.1_b97 bash
```
* Pytorch and torchvision should already be installed for you, just make sure you use python3 for all commands instead of regular python (which points to python2)
* Swap should also be already set up for you ( we did this in homework 1)

## Training the model
I trained using [these instructions](https://github.com/dusty-nv/jetson-inference/blob/master/docs/pytorch-plants.md) to train ResNet-18 on the PlantCLEF dataset.  I trained on 100 epochs

## Results

Training log can be seen in `train.log`

It took 32057.062 seconds to train the model. My final accuracies were Acc@1 56.83	Acc@5  86.08.

I was unable to increase the batch size, as I got memory errors (out of memory)

Model has been saved.





