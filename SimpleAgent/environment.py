import numpy as np
import random
from Simplified_Agent_Visualization import Visualization

class Environment:


    #start_config: 0 = right; 1 = down; 2 = left; 3 = top
    def __init__(self, width, height, obstacles, goal_x, goal_y, start_pos_x, start_pos_y, start_config):
        self.width = width
        self.height = height
        self.obstacles = obstacles
        self.goal_x = goal_x
        self.goal_y = goal_y
        self.start_x = start_pos_x
        self.start_y = start_pos_y
        self.start_config = start_config
        self.agent_pos_x = start_pos_x
        self.agent_pos_y = start_pos_y
        self.agent_config = start_config
        self.number_states = width * height * 4
        self.actions = [-1, 0, 1]

    #-1 = turn left; 0 = move straight; 1 = turn right
    def step(self, action):
        reward = 0
        stop = False
        #move straight
        if action == 0:
            if self.agent_config == 0:
                self.agent_pos_x += 1
            elif self.agent_config == 1:
                self.agent_pos_y -= 1
            elif self.agent_config == 2:
                self.agent_pos_x -= 1
            elif self.agent_config == 3:
                self.agent_pos_y += 1
            #check if obstacle
            for (o_x, o_y) in self.obstacles:
                if o_x == self.agent_pos_x and o_y == self.agent_pos_y:
                    reward = -10
                    stop = True
                    return np.zeros(self.width * self.height * 4), reward, stop
            #check if grid is left:
            if self.agent_pos_x >= self.width or self.agent_pos_x < 0 or self.agent_pos_y >= self.height or self.agent_pos_y < 0:
                reward = -10
                stop = True
                return np.zeros(self.width * self.height * 4), reward, stop
            #check if goal is reached
            if self.goal_x == self.agent_pos_x and self.goal_y == self.agent_pos_y:
                reward = 10
                stop = True
        #else: turn, no reward, no stopping
        else:
            self.agent_config += action
            self.agent_config %= 4

        #TODO VISUALIZE ENVIRONMENT
        #PARAMETERS:
        #self.agent_config (0=right, 1=top, 2=left, 3=down) -> turning angle
        #self.width, self.height (grid size)
        #self.obstacles -> coordinates for obstacles
        #self.goal_x, self.goal_y -> goal coordinates
        #self.agent_pos_x, self.agent_pos_y -> agent coordinates

        visual_object = Visualization(self.width, self.height, self.goal_x, self.goal_y, self.agent_pos_x, self.agent_pos_y)
        visual_object.update(self.obstacles, self.agent_config)        
        
        #print(str(self.width)+"; "+str(self.height)+"; "+str(self.agent_pos_x)+"; "+str(self.agent_pos_y)+"; "+str(self.agent_config))
        state_one_hot = np.eye(self.width*self.height*4)[(self.agent_pos_y*self.width) + self.agent_pos_x+(self.agent_config*self.height*self.width)]
        return state_one_hot, reward, stop
        #return (self.agent_pos_x, self.agent_pos_y, self.agent_config), 0, 0

    def get_random_action(self):
        return random.choice(self.actions)

    def reset(self):
        self.agent_pos_x = self.start_x
        self.agent_pos_y = self.start_y
        self.agent_config = self.start_config
        #return (self.agent_pos_x, self.agent_pos_y, self.agent_config)
        state_one_hot = np.eye(self.width * self.height * 4)[
            (self.agent_pos_y * self.width) + self.agent_pos_x + (self.agent_config * self.height * self.width)]
        return state_one_hot
