# Initial commit of visualization codes, containing the movement of the agent according to X, Y and Theta
# I will refactor the code and give call from train_agent Class

import pygame
import sys
import time

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


# The rotate transformation of pygame alters the dimensions of the object. 
# So, I Save the original object and continue to apply the altered transformation to the original agent object.

def rotatingTheta(agentObject, theta, rotations={}):
    r = rotations.get(agentObject,0) + theta
    rotations[agentObject] = r
    return pygame.transform.rotate(agentObject, r)

def agent_movement_visualization(train_finish, updated_x, updated_y):
    pygame.init()
    
    screen = pygame.display.set_mode((1200,600))

    # Agent Initializtion .......
    Agent = pygame.image.load("tesla.png")
    Agent = pygame.transform.scale(Agent, (100, 50))
    Agent.set_colorkey((255, 0, 0))
    
    while not train_finish:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                train_finish = True
                #sys.exit()
                
        #screen.fill( (255,0,0) )
        # Background Initialization ...
        BackGround = Background('crossboard.png', [0,0])
        screen.fill([255, 255, 255])
        screen.blit(BackGround.image, BackGround.rect)
        
        rotated_agent = rotatingTheta(Agent, 10)
        position = rotated_agent.get_rect()
        displaced_agent_after_rotation = position.move(updated_x, updated_y)
        #screen.blit(rotated_agent, (400,300))
        #screen.blit(rotated_agent, displaced_agent_after_rotation)
        screen.blit(Agent, displaced_agent_after_rotation)
        pygame.display.update()
        time.sleep(0.005)
        updated_x += 7
        updated_y += 0
        
        
    pygame.quit()
    quit()

train_finish = False
agent_movement_visualization(train_finish, 10, 7)