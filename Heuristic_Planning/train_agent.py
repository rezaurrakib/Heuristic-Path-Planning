import gym
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from single_track_model import Single_track_model
from target import Target_Line
import random
from heuristic_visualization import Visualization

# LOAD ENVIRONMENT
env = gym.make('FrozenLake-v0')

#possible steering angles (degrees) = actions to take
STEERING_ACTIONS = [-5, -2.5, 0, 2.5, 5]

MAX_PHI = 45 #maximal steering angle
L = 3 #vehicle length between front and rear axis
VELOCITY = 5 #velocity in m/s -> 18 km/h -> quite slow
TIMESTEP_SIZE = 0.5 #timestep in s

print("Creating model")
#init model
model = Single_track_model(MAX_PHI, L, VELOCITY, TIMESTEP_SIZE)

#init target
target = Target_Line(x1=0, y1=0, x2=1, y2=0) #straight line on x-axis

#init visualization
visualization = Visualization()

#CREATE NETWORK
print("Creating network")
tf.reset_default_graph()

#Establish the feed-forward part of the network used to choose actions
# 16 states, 4 actions, but in the car case, there are infinite states! (infinite positions and infinite theta-configurations)
# Solution: don't use one-hot vector for state, but 3-element vector for (x,y,theta)
inputs1 = tf.placeholder(shape=[1,3],dtype=tf.float32)
W = tf.Variable(tf.random_uniform([3,len(STEERING_ACTIONS)],0,0.01))
Qout = tf.matmul(inputs1,W)
predict = tf.argmax(Qout,1)

# Below we obtain the loss by taking the sum of squares difference between the target and prediction Q values.
nextQ = tf.placeholder(shape=[1,len(STEERING_ACTIONS)],dtype=tf.float32)
loss = tf.reduce_sum(tf.square(nextQ - Qout))
trainer = tf.train.GradientDescentOptimizer(learning_rate=0.1)
updateModel = trainer.minimize(loss)


# TRAIN NETWORK
init = tf.initialize_all_variables()

# Set learning parameters
y = .99
e = 0.4
num_episodes = 100
# create lists to contain total rewards and steps per episode
jList = []
rList = []
with tf.Session() as sess:
    sess.run(init)
    for i in range(num_episodes):
        print("Starting new round; episode "+str(i))
        # Reset environment and get first new observation
        #reset model to some random state (for the beginning, always start with same point
        model.set_state(1,1,0)
        state = model.get_state()
        rAll = 0
        j = 0
        # The Q-Network
        while j < 99:
            j+=1
            # Choose an action by greedily (with e chance of random action) from the Q-network
            x, y, theta = state
            a,allQ = sess.run([predict,Qout],feed_dict={inputs1:[[x, y, theta]]})
            #TODO: take randomness back in
            if np.random.rand(1) < e:
                a[0] = random.choice(range(len(STEERING_ACTIONS)))
            #Get new state and reward from environment
            #s1,r,d,_ = env.step(a[0])

            state1, reward = model.step(STEERING_ACTIONS[a[0]], target)

            # VISUALIZE CAR AND LINE HERE
            #TODO add L, phi, target_line to visualization
            x1, y1, theta1 = state1
            visualization.update(x1,y1,theta, STEERING_ACTIONS[a[0]], reward)
			#...


            # Obtain the Q' values by feeding the new state through our network
            Q1 = sess.run(Qout,feed_dict={inputs1:[[x1, y1, theta1]]})
            # Obtain maxQ' and set our target value for chosen action.
            maxQ1 = np.max(Q1)
            targetQ = allQ
            targetQ[0,a[0]] = reward + y*maxQ1
            # Train our network using target and predicted Q values
            _,W1 = sess.run([updateModel,W],feed_dict={inputs1:[[x, y, theta]],nextQ:targetQ})
            rAll += reward
            state = state1
        # Reduce chance of random action as we train the model.
        e = 1./((i/50) + 10)
        jList.append(j)
        rList.append(rAll)
print("Percent of succesful episodes: " + str(sum(rList)/num_episodes) + "%")

print(rList)
print(jList)

# STATISTICS ON NETWORK PERFORMANCE
# reaching goal?
plt.plot(rList)
# progress through network?
plt.plot(jList)