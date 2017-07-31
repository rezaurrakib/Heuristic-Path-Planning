# Heuristic Path Planning with A* and Deep Q Networks

As a team of four, we worked on the comparison and visulization of path planning problem.
The responsibilities were the following (if there are any questions to one of the modules, feel free to contact to us)
- Reza - Visualization of agent + behaviour for simple model & complex model (all Visualization modules)
- Till Soehlemann - Implementation of qlearning pipelines for simple model & complex model; Development of single-track model (SimpleQAgent, ComplexQAgent)
- Abu - Make qlearning models deep + add multiple layers (3LayerNN)
- Emrecan Tarakci - A-Star Algorithm for grid model, reward mechanism for DQN (AStar)

## Overview
#A-Star (Emrecan)

To see the visualized A Star approach with two different heuristics, namely Euclidean Distance and Manhattan Distance, you need to run pathfinder.py which requires AStar_Visualization.py. 
Also please note that, this part is realized under Ubuntu 16.04 with python2.7. 

Thus, in order to run this program you need to use `python pathfinder.py`.

The size of the grid, the obstacles, coordinates of starting point and the goal point can be modified in pathfinder.py. 
The car finds the shortest path -smallest cost- in a timely manner. Of course, this depends on the heuristics that we are using, but for our 2D grid problem with some obstacles, it outperformed DQN approach.

In addition, in visualization you may see the different heuristics and their path to goal.


#Q-learning (Till)

Secondly, To train the simple q-learning module, run train_agent.py in SimpleQAgent. The car learns to find a goal in a two-dimensional grid with random obstacles.

For each action in each state, the rewards are observed (1 if the goal is reached, -1 if a wall or an obstacle is hit, 0 otherwise). By trying out a large amount of action sequences, the car learns a set of q-values for each state, which represents the expected future reward for each action. As the agent explores the environment more and more (Exploration-Phase), the randomness factor decreases and the agent makes use of the observations and starts to only take the actions that turned out to lead to high rewards (Exploitation-Phase)

The training process takes some time, as the agent starts with exploring the environment using a specific randomness factor e (set to 0.4, can be changed in train_agent.py), which decreases with training time.

The size of the grid, the obstacles and the goal can also be modified in train_agent.py.

The visualization shows how the car converges from an exploration phase (many random movements) to an exploitation phase and finally ends up in figuring out efficient paths to the goal.

The downside of using qlearning is obviously the training time: in such a simple scenario, it would be more feasible using a simple heuristic in order to find the optimal path.

However, this simple model is a perfect example for getting to know how q-learning works and getting an idea of how it could be applied to more advanced problems. Especially in complex environments, in which it is not possible for humans any more to define clear and simple heuristics or rules, q-learning can be a great opportunity to let an agent explore the environment and the rewards for each action in each state by exploration.


Finally, there is also a more complex q-learning module, which does not use a discretized grid, but a more complex and high-dimensional environment.

To run the complex model, execute the script train_agent.py in ComplexQAgent.

Here, the movements are restricted by a single track model, defined by the length L of the car, the steering angle phi, the configuration angle theta and the position of the car and a goal line. More specifically, the only action the car can take is a change of the steering angle phi, which leads (due to constant speed) to a change of x, y and theta.

It can be seen that the movements of the car are more realistic, but also that the model is way more complex and unfortunately does not behave optimally.




## Prerequisites

What things you need to install the software and how to install them

Tensorflow: pip install tensorflow
Python 3
Python 2.7

## Visualization Process (Reza)
The visualization process incorporates a two dimensional grid having the co-ordinates of the obstacles in it. For the design of the simple Q Learning based agent and A-Star implemmentation the Grid has been used as the traning space. 

In case of simple Q Learning based agent, the Agent (i.e., the car) starts it's journey from the starting coordiante which has been provided by the system. The goal is also fixed. We have four agent configuration for the facing of the car/agent.

- For agent_config 0, it faces towards right/forward, rotation of 0 degree 
- For agent_config 1, it faces towards top of the current cell, rotation of 90 degree 
- For agent_config 2, it faces towards left/backward, rotation of -180 degree 
- For agent_config 3, it faces towards down of the current cell, rotation of 270 degree 

for the A - Star implementation, the scenerio is slightly different. Although the agent facing and the 2D Grid world is same , but the visualization process is not same. In A - Star implementation, we've shouwn the path construction of the car from the starting point towards the Goal position. The heuristic technique has been applied using the Manhattan distance and Euclidean Distance. Obviously , the co-ordinate list of the obstacles are also present in this visualization model too.

## Visualization Methods (Reza)
For the simple Q Learning based agent movemment, the *Visualization Class* in the *Simplified_Agent_Visualization.py* file defines the update() method which takes the co-ordinate list of the ostacles, agent/car's updated position (x, y) and the agent configuration as the parameter. 


#*agent_grid_movement_visualization()*

This method is responsible for creating the 2D World cordinate system where the car will navigate and learn. The obstacles are distributed in the screen according to the dynamic coordinate provided from the update() method. We've used the *pygame* framework for visualizing the rectangles, grids and animations. The agent and the goal position is also configured here. 

After the displacement of the agent according to the updated (x,y) coordinate, the car is redrawn in the 2D Grid. We have created the frames in 0.05 secs interval, to show the  movement and learning procedure of the car.


#*rotatingTheta()*

This method is responsible for updating the car position according to the updated agent configuration angle. It returns the transformed image of rotated car.

In the A - Star implementation, the visualizaton methods are almost same. A few changes have been made for showing the path constrauction of the car. The system provided the car's updated  (x,y) position and the list of the so far visited co-ordinates. Then the *agent_grid_movement_visualization()* method in the *AStar_Visualization.py* file draws the visited paths in the GRID with obstacles and agent's new position.   

In below, there are some snippets of the visualizaton process is given : 

## Visualization Snippets: 

A\* with Euclidean Distance as Heuristic Technique:

![ED](images/EuclideanDistance.png)

A\* with Manhattan Distance as Heuristic Technique:

![MD](images/ManhattanDistance.png))

## Deep Q Network (Abu)
### Random Field with Random Obstacles and Random Goal
The executables can be found in 3LayerNN.
A Random field with 16 Random obstacles and 1 goal line has been generated for the training purpose. Initially each obstacle is a square having a length (l=6 unit). The field size is set to 300x300 unit.

### More simplified car
The concept of Dubins car is used. The car can moved only forward, left or right with a v=1 unit/sec. theta represents the facing of the car.
### DQN Architecture
Our DQN consists of 3 fully connected hidden layer. Each layer is using RELU as activation function. Each layer has 200 neurons. The input layer consists of 17 inputs each is a measure of distance. 16 are the distance of car from 16 obstacles and last distance is from the goal to the car. The output layer consists of 3 unit( for straight, left and right movement), each one is a reward value (Q value in this model). Adam optimizer has been used for minimizing the Q value (we are treating less reward as good position) since the traditional SGD has shown Vanishing Gradient problem with our model. 

### Reward Policy
When the car moves as near as 2 unit to obstacles, the reward value is increased by 1. When the car moves away from the goal, the reward is increased by 1. 


## Authors

Reza, Abu, Emrecan Tarakci, Till Soehlemann
