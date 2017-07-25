# Initial commit of visualization codes, containing the movement of the agent according to X, Y and Theta
# I will refactor the code and give call from train_agent Class

import pygame
import sys
import time

RED = (255, 0 , 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

TEXT_SIZE = 20
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
LINE_THICKNESS = 8

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Visualization:

    # The rotate transformation of pygame alters the dimensions of the object.
    # So, I Save the original object and continue to apply the altered transformation to the original agent object.

    def __init__(self):
        pygame.init()


    def rotatingTheta(self, agentObject, theta, rotations={}):
        r = rotations.get(agentObject,0) + theta
        rotations[agentObject] = r
        return pygame.transform.rotate(agentObject, r)


    def text_information_display(self, screen, x, y, theta, phi, reward):
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', TEXT_SIZE)
        text = "X : " + str(x) + "\nY : " + str(y) + "\nTheta : " + str(theta) + "\nPhi: "+str(phi) +"\nReward: "+str(reward)
        lines = text.splitlines()
        
        for i, length in enumerate(lines):
            screen.blit(myfont.render(lines[i], 0, BLACK), (SCREEN_WIDTH - 300, 0 + TEXT_SIZE * i))


    def agent_movement_visualization(self, updated_x, updated_y, updated_theta, current_phi, reward):

        screen = pygame.display.set_mode((1200,700))

        # Agent Initializtion .......
        Agent = pygame.image.load("tesla.png")
        Agent = pygame.transform.scale(Agent, (100, 50))
        Agent.set_colorkey((255, 0, 0))

        # Background Initialization ...
        BackGround = Background('crossboard.png', [0,0])
        screen.fill([255, 255, 255])
        screen.blit(BackGround.image, BackGround.rect)

        #draw_line_obstacle(BackGround.image, (20, 20) , (100, 100))
        pygame.draw.line(screen, RED, (SCREEN_WIDTH - 1000, (SCREEN_HEIGHT/2)) , (SCREEN_WIDTH - 200, (SCREEN_HEIGHT/2)), LINE_THICKNESS)

        # Displaying Animation
        rotated_agent = self.rotatingTheta(Agent, updated_theta)
        position = rotated_agent.get_rect()
        displaced_agent_after_rotation = position.move(updated_x, updated_y)
        #screen.blit(rotated_agent, (400,300))
        screen.blit(rotated_agent, displaced_agent_after_rotation)
        #screen.blit(Agent, displaced_agent_after_rotation)
        self.text_information_display(screen, updated_x, updated_y, updated_theta, current_phi, reward)
        pygame.display.update()
        time.sleep(0.005) # Frame creates in 0.005 sec interval



    def update(self, x, y, theta, phi, reward):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #TODO
                train_finish = True
        self.agent_movement_visualization(x, y, theta, phi, reward)

    def test_agent_visualization(self):
        pygame.init()
        train_finish = False
        init_X = 5
        init_Y = 10
        theta = 5

        while not train_finish:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    train_finish = True

            self.agent_movement_visualization(init_X, init_Y, theta)

            init_X += 1
            init_Y += 1
            theta += 1

        pygame.quit()