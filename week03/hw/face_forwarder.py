import paho.mqtt.client as mqtt

i = [0]
def on_message(client, userdata, message):
    print('Publishing message ' + str(i[0]))
    i[0] += 1
    #pub.publish('forwarder_out', message.payload)
    
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successful connection to Jetson broker!")
    else:
        print("Failed to connect to Jetson broker!")

sub = mqtt.Client()
sub.connect('192.168.0.18') # <- my Jetson's IP address
sub.subscribe('face_detect/#')

pub = mqtt.Client()

sub.on_connect = on_connect
sub.connect('169.62.51.136') # <- my IBM container's IP address

sub.on_message = on_message
sub.loop_forever()