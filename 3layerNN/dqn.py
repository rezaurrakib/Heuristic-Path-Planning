import tensorflow as tf
import numpy as np
from FieldModel import FieldModel
n_epochs=2000

n_obstacle=16
n_input= n_obstacle+1 # one for goal
n_hidden_feature=200
n_output=3
W1=tf.Variable(tf.random_uniform((n_input, n_hidden_feature), -.5,.5,dtype=tf.float32) )# weight between input and first hidden layer
W2=tf.Variable(tf.random_uniform((n_hidden_feature, n_hidden_feature), -.5,.5, dtype=tf.float32)) # weight between first and second hidden layer
W3=tf.Variable(tf.random_uniform((n_hidden_feature, n_hidden_feature), -.5,.5, dtype=tf.float32)) # weight between second and third hidden layer
W4=tf.Variable(tf.random_uniform((n_hidden_feature, n_output), -.5,.5, dtype=tf.float32))# weight between third and output oayer

B1= tf.Variable(tf.zeros(n_hidden_feature, dtype=tf.float32))
B2= tf.Variable(tf.zeros(n_hidden_feature, dtype=tf.float32))
B3= tf.Variable(tf.zeros(n_hidden_feature, dtype=tf.float32))
B4= tf.Variable(tf.zeros(n_output, dtype=tf.float32))

#inputs
X= tf.placeholder("float", [None, n_input])
#output
Y= tf.placeholder("float", [None, n_output])
#first hidden layer with relu activation
layer1=tf.add(tf.matmul(X,W1), B1)
layer1=tf.nn.relu(layer1)
#second hidden layer with relu activation
layer2=tf.add(tf.matmul(layer1, W2),B2)
layer2=tf.nn.relu(layer2)
#third hidden layer with relu activation
layer3= tf.add(tf.matmul(layer2, W3),B3)
layer3=tf.nn.relu(layer3)
#output layer with linear activatino
reward_layer= tf.add(tf.matmul(layer3, W4),B4)


reward= tf.sqrt(tf.reduce_sum(tf.square(reward_layer-Y)))
optimizer= tf.train.AdamOptimizer(0.01).minimize(reward)
decision= tf.argmin(reward_layer,1)

init = tf.global_variables_initializer()
with tf.Session() as sess:
    sess.run(init)
    for epoch in range(n_epochs):
        print "entering epoch "+ str(epoch+1)
        #generate field with obstacle and start and goal 
        Field= FieldModel(300,300)# field is a grid of 300x300 unit
        condition= True
        while(condition):
            #get input from field
            inputData= Field.getInputForQLearning()
            outputData= Field.getOutputData()
            for _ in range(1000):
                R,_, dec= sess.run([reward_layer, optimizer, decision], feed_dict={X: np.array(inputData).reshape((1, 17)), Y:np.array(outputData).reshape((1, 3)) })
            print R
            #print outputData
            #print outputData3
            
            
            # update car position
            #print type(dec)
            #print dec
            #print Field.theta
            new_dec= dec[0]
            if new_dec==0: #move left
                if Field.theta ==0: # car is facing forward
                    Field.x_init +=1
                    Field.y_init +=1
                    Field.theta= 90
                elif Field.theta ==90: #car is facing upward
                    Field.x_init -=1
                    Field.y_init+=1
                    Field.theta = 180
                elif Field.theta == 180: #car is facing backward
                    Field.x_init-=1
                    Field.y_init-=1
                    Field.theta=270
                else: # car is facing downward
                    Field.x_init+=1
                    Field.y_init-=1
                    Field.theta= 0
            elif new_dec==1: #move straight
                if Field.theta ==0: # the car is facing forward
                    Field.x_init+=1
                elif Field.theta ==90: # the car is facing upward
                    Field.y_init+=1
                elif Field.theta == 180: # the car is facing backward
                    Field.x_init-=1
                else: # the car is facing downward
                    Field.y_init-=1
            else: 
                if Field.theta==0: 
                    Field.x_init+=1
                    Field.y_init-=1
                    Field.theta= 270
                elif Field.theta==90:
                    Field.x_init+=1
                    Field.y_init+=1
                    Field.theta=0
                elif Field.theta==180:
                    Field.x_init-=1
                    Field.y_init+=1
                    Field.theta=90
                else:
                    Field.x_init-=1
                    Field.y_init-=1
                    Field.theta=180
            #input()
            print str(Field.x_init)+" "+str(Field.y_init)+"---->"+str(Field.x0_goal)+" "+str(Field.y0_goal)
            #condition = not Field.goalCheck()
            condition = (not Field.goalCheck()) and (not Field.collisionCheck())
            #print str(Field.goalCheck())+" "+ str(Field.collisionCheck())
            if condition==False:
                print "breaking while loop"
                break