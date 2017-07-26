import pygame
import sys
import time

RED = (255, 0 , 0)
GREEN = (0, 220, 0)
BLACK = (0, 0, 0)
BROWN = (153, 76, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

GRID_HEIGHT = 18
GRID_WIDTH = 25
BLOCK_SIZE = 60

SCREEN_WIDTH = 200
SCREEN_HEIGHT = 120

colors = [WHITE, BLACK]


class Visualization:
    def __init__(self, width, height, goal_x, goal_y, agent_pos_x, agent_pos_y):
        pygame.init()
        self.GRID_WIDTH = width
        self.GRID_HEIGHT = height
        self.goal_x = goal_x
        self.goal_y = goal_y
        self.agent_pos_x = agent_pos_x
        self.agent_pos_y = agent_pos_y
    
    def rotatingTheta(self, agentObject, theta, rotations={}):
        r = rotations.get(agentObject,0) + theta
        rotations[agentObject] = r
        return pygame.transform.rotate(agentObject, r)
    
    def agent_grid_movement_visualization(self, obstacles_coordinate, agent_config):
        
        screen = pygame.display.set_mode((self.GRID_WIDTH * BLOCK_SIZE, self.GRID_HEIGHT * BLOCK_SIZE))
        
        for y in range(self.GRID_HEIGHT):
            d = y%2  # applied for randomly distributed grid_color 
            for x in range(self.GRID_WIDTH):
                pygame.draw.rect(screen, colors[(x+d)%2 ], (x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        for i,j in obstacles_coordinate:
            #print i,j
            pygame.draw.rect(screen, RED, (i*BLOCK_SIZE, j*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        # Agent Loading
        Agent = pygame.image.load("tesla.png")
        Agent = pygame.transform.scale(Agent, (BLOCK_SIZE, BLOCK_SIZE))
        Agent.set_colorkey((255, 0, 0))

        # Goal Loading
        Goal = pygame.image.load("goal.png")
        Goal = pygame.transform.scale(Goal, (3*BLOCK_SIZE, 3*BLOCK_SIZE))
        Goal.set_colorkey((255, 0, 0))
        
        # Setting the car angle
        if agent_config == 0:
            updated_theta = 0   # turn right / front
        
        elif agent_config == 1:
            updated_theta = 90   # turn top 
            temp = self.agent_pos_x
            self.agent_pos_x = self.agent_pos_y
            self.agent_pos_y = -1 * temp
            
        elif agent_config == 2:
            updated_theta = -180   # turn left
            self.agent_pos_x = self.agent_pos_x * -1
        
        elif agent_config == 3:
            updated_theta = -90   # turn down
            temp = self.agent_pos_x
            self.agent_pos_x = self.agent_pos_y
            self.agent_pos_y = temp
        
        
        rotated_agent = self.rotatingTheta(Agent, updated_theta)
        position = rotated_agent.get_rect()
        displaced_agent_after_rotation = position.move(self.agent_pos_x, self.agent_pos_y)
        #screen.blit(rotated_agent, (400,300))
        screen.blit(rotated_agent, displaced_agent_after_rotation)
        
        goal_position = Goal.get_rect()
        goal_position_move = goal_position.move(self.goal_x, self.goal_y)
        screen.blit(Goal, goal_position_move)
        
        pygame.display.update()
        time.sleep(0.004) # Frame creates in 0.005 sec interval
        
    def update(self, obstacles_coordinate, agent_config):
        self.agent_grid_movement_visualization(obstacles_coordinate, agent_config)       
