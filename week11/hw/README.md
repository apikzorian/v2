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

### What parameters did you change? What values did you try? 

#### Round 1: Default 

I began with the standard setting for the run

Results:
```
Total successes are:  22
```
#### Round 2: 

Next, I tried lowering the training threshold from 3000 to 300 and also changed the optimizer from adam to adamax. The idea of lowering the training threshold would be to start training earlier, thereby getting more training cycles out of our model with the hopes that it will be able to learn more and get more landings. The Adamax optimizer works well with sparse parameter updates, and the gradient term is ignored when it is small, allowing less gradient noise effect to the parameters.

in run_lunar_lander.py
```
training_thr = 300
```

in lunar_lander.py
```
def nnmodel(input_dim):
    model = Sequential()
    model.add(Dense(32, input_dim=input_dim, activation='relu'))
    model.add(Dense(16, activation='sigmoid'))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    return model
```

Results:
```
Total successes are:  31
```


### Round 3:

Finally, I decided to increase the complexity of the model. By doing this, I hoped to have a better accuracy and get the most succesful landings possible. I added another layer and increased the nodes.

```
def nnmodel(input_dim):
    model = Sequential()
    model.add(Dense(64, input_dim=input_dim, activation='relu'))
    model.add(Dense(64, input_dim=input_dim, activation='relu'))
    model.add(Dense(32, activation='sigmoid'))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adamax', metrics=['accuracy'])
    return model

```

Result:

```
Total successes are:  36
```

### Other changes

I found the following code on the #w251 slack channel by Austin Doolittle, which showed a way to speed up the runs:

```
a_candidates = np.random.uniform(low=-1, high=1, size=(batch_size, 2))
s_expanded = np.broadcast_to(new_s, (batch_size, 8))
all_candidates = np.concatenate([s_expanded, a_candidates], axis=1)
r_pred = model.predict(all_candidates)

max_idx = np.argmax(r_pred)
a = a_candidates[max_idx]
```

Replacing this code for the action candidate generation code helped me really cut down on my runtime, as I was able to get results for the 50,000 iterations in 5 hours (previously, it took almost 11 hours).

I also tried decreasing the number of iterations to see if this would help with my results, as I assumed it would result in less overfitting. However, this gave me worse results, as I was unable to get more than 25 landings (I was able to get 31 with 50000 iterations and lowering the training threshold to 300).

### Conclusion
I was able to get improved results by lowering the training threshold and letting my model start training earlier in the workflow. This way, it was able to get more training cycles in the run and did result in more succesful landings. The key change that I made was adding a layer and adding more nodes to the layers of my model. This allowed for a more complex neural network that was able to make improved classificactions and finally gave me the best result of all of my configurations. While we were told to play with the number of total iterations, my experience was that decreasing these iterations resulted in worse results, and I believe maintaining 50,000 iterations was fine as long as we were able to lower the training threshold and work with a more complex model.



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
