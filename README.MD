# Heuristic Path Planning with A* and Deep Q Networks

As a team of four, we worked on the comparison and visulization of path planning problem.
The responsibilities were the following (if there are any questions to one of the modules, feel free to contact to us)
- Reza - Visualization of agent + behaviour for simple model & complex model
- Till Soehlemann - Implementation of qlearning pipelines for simple model & complex model; Development of single-track model
- Abu - Make qlearning models deep + add multiple layers
- Emrecan Tarakci - A-Star Algorithm for grid model

## Getting Started

To train the simple q-learning module, run train_agent.py. The car learns to find a goal in a two-dimensional grid with random obstacles.

The size of the grid, the obstacles and the goal can be modified in train_agent.py.

The visualization shows, how the car converges from an exploration phase (many random movements) to an exploitation phase and finally ends up in figuring out efficient paths to the goal.

The downside of using qlearning is obviously the training time: in such a simple scenario, it would be more feasible using a simple heuristic in order to find the optimal path.

However, this simple model is a perfect example for getting to know how q-learning works and getting an idea of how it could be applied to more advanced problems.


We also implemented a more complex q-learning module, which does not use a discretized grid, but a more complex and high-dimensional environment.

Here, the movements are restricted by a single track model, defined by the length L of the car, the steering angle phi, the configuration angle theta and the position of the car and a goal line.

It can be seen that the movements of the car are more realistic, but also that the model is way more complex and unfortunately does not behave optimally.




### Prerequisites

What things you need to install the software and how to install them

Tensorflow: pip install tensorflow

Visualization: 

```
Give examples
```


## Authors

Reza, Abu, Emre Can, Till Soehlemann
