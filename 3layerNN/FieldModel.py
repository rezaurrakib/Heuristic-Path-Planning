import numpy as np
from random import randint
import math
class FieldModel:
    def __init__(self, w, h):
        self.width=w
        self.height=h
        self.obstacles=[]
        self.F= np.zeros(shape=(w,h), dtype=np.float32)
        #random start point
        self.x_init= randint(0,w)
        self.y_init= randint(0,h)
        self.theta= 0 # initially car is positioned straight, for 90 car is faced up, 180 faced back, 270 faced below
        #random goal line
        self.x0_goal= randint(10,w-10)
        self.y0_goal= randint(10, h-10)
        direction= randint(0,3)
        if direction == 0:
            self.xn_goal= self.x0_goal+10
            self.yn_goal= self.y0_goal+10
        elif direction == 1:
            self.xn_goal= self.x0_goal-10
            self.yn_goal= self.y0_goal+10
        elif direction == 2:
            self.xn_goal= self.x0_goal +10
            self.yn_goal= self.y0_goal -10
        else:
            self.xn_goal= self.x0_goal -10
            self.yn_goal= self.y0_goal -10
            
        #create obstacles
        #divide the field in 16 region, set one obstacle in each region
        for i in range(4):
            for m in range(4):
                a0= i*(w/4)+3 
                b0=m*(h/4)+3
                an= (i+1)*(w/4)-10
                bn= (m+1)*(w/4)-10
                #get obstacle coordinate
                obs_x= randint(a0, an)-3
                obs_y= randint(b0,bn)-3
                #update F
                for j in range(7):
                    for k in range(7):
                        self.F[obs_x+j][obs_y+k]=1
                #update obstacle list
                self.obstacles.append([obs_x, obs_y, 6])
    def getInputForSpecificLocation(self, x,y):
        #the input conists of 17 distance, 
        #16 distances from 16 obstacles
        #1 distance from the goal
        #the dqn will minimize the distance to goal and maximize the distance to obstacle using reward
        inp=[]
        for obstacle in self.obstacles:
            x0= obstacle[0]
            y0= obstacle[1]
            length= obstacle[2]
            x1= x0+length
            y1= y0
            x2= x1
            y2= y1+length
            x3= x0
            y3 = y2
            d1= self.euclideanDistance(x,y, x1,y1)
            d2= self.euclideanDistance(x,y, x2,y2)
            d3= self.euclideanDistance(x,y, x3,y3)
            d4= self.euclideanDistance(x,y, x0,y0)
            min_d= min(d1,d2,d3,d4)
            inp.append(min_d)
        d_g= self.euclideanDistance(x,y, self.x0_goal, self.y0_goal)
        inp.append(d_g)
        #print str(d_g) + "goal"
        return inp
    
    def getInputForQLearning(self):
        #the input conists of 17 distance, 
        #16 distances from 16 obstacles
        #1 distance from the goal
        #the dqn will minimize the distance to goal and maximize the distance to obstacle using reward
        inp=[]
        for obstacle in self.obstacles:
            x0= obstacle[0]
            y0= obstacle[1]
            length= obstacle[2]
            x1= x0+length
            y1= y0
            x2= x1
            y2= y1+length
            x3= x0
            y3 = y2
            d1= self.euclideanDistance(self.x_init, self.y_init, x1,y1)
            d2= self.euclideanDistance(self.x_init, self.y_init, x2,y2)
            d3= self.euclideanDistance(self.x_init, self.y_init, x3,y3)
            d4= self.euclideanDistance(self.x_init, self.y_init, x0,y0)
            min_d= min(d1,d2,d3,d4)
            inp.append(min_d)
        d_g= self.euclideanDistance(self.x_init, self.y_init, self.x0_goal, self.y0_goal)
        inp.append(d_g)
        #print str(d_g) + "goal"
        return inp
    def euclideanDistance(self, x0,y0,x1,y1):
        return math.sqrt((x0-x1)*(x0-x1)+(y0-y1)*(y0-y1))
    def getOutputData(self):
        out=[]
        outVal=[]
        if self.theta == 0:
           out.append((self.x_init+1, self.y_init))#straight
           out.append((self.x_init+1, self.y_init+1))#left
           out.append((self.x_init+1, self.y_init-1))#right
        elif self.theta == 90:
            out.append((self.x_init, self.y_init+1))#straight
            out.append((self.x_init-1, self.y_init+1))#left
            out.append((self.x_init+1, self.y_init+1))#right
        elif self.theta == 180:
            out.append((self.x_init-1, self.y_init))#straight
            out.append((self.x_init-1, self.y_init-1))#left
            out.append((self.x_init-1, self.y_init+1))#right
        else:
            out.append((self.x_init, self.y_init-1))#straight
            out.append((self.x_init+1, self.y_init-1))#left
            out.append((self.x_init-1, self.y_init-1))#right
        #reward policy
        #1. if distance from goal increases, reward will be positive
        #2. if distance from obstacle decreases reward will be positive
        inp = self.getInputForQLearning()
        for o in out:
            r=0 # reward
            a= self.getInputForSpecificLocation(o[0],o[1])
            for b in range(16):
                if a[b]< inp[b]:
                    r=r+1
            if a[15]>inp[15]:
                r=r+15
            outVal.append(r)
        return outVal
    def goalCheck(self):
        if self.x_init==self.x0_goal and self.y_init == self.y0_goal:
            print "Goal Reached\n"
            return True
        else:
            #print "Distance from Goal: "+ str(self.euclideanDistance(self.x_init, self.y_init, self.x0_goal, self.y0_goal))
            return False
        
    def collisionCheck(self):
        coll =False
        for ob in self.obstacles:
            x= ob[0]
            y= ob[1]
            h= ob[2]
            xh= x+h
            yh= y+h
            if (self.x_init >= x and self.x_init <=xh and self.y_init>=y and self.y_init <= yh) or self.x_init <1 or self.x_init >self.width-1 or self.y_init <1 or self.y_init > self.height-1:
                coll= True
                print "Collission detected\n"
                break
        return coll