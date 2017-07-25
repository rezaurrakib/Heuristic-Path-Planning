import math

class Single_track_model:

    #position variables refer to the 2D position of the rear axis!
    def __init__(self, max_phi, L, velocity, timestep_size, theta=0, x=0, y=0):
        self.max_phi = max_phi #maximal steering angle
        self.L = L #vehicle length
        self.theta = theta #car angle
        self.x = x
        self.y = y
        self.velocity = velocity #velocity is assumed to be constant
        self.timestep_size = timestep_size #discretization of time; one action = driving with a fixed steering angle for one timestep

    #set state of car
    def set_state(self, x, y, theta):
        self.x = x
        self.y = y
        self.theta = theta

    #get current state of the car
    def get_state(self):
        return self.x, self.y, self.theta

    # move the car and compute the position and angle of the car (x_new, y_new, theta_new),
    # depending on the previous state (x_old, y_old, theta_old)
    # and the action(steering angle phi with velocity v for duration of one timestep)
    def next_state(self, phi):

        #simplifying approach (without integrals etc): discretize timestep in to very small fraction
        #for each fraction, assume that the car moves straight (according to theta),
        #but phi changes according to velocity, car length and steering angle
        #that way, the exact new position can be approximated

        # fraction length of one elementary straight movement (0.001 seconds)
        fractions_per_timestep = 10
        fraction_size = self.timestep_size/fractions_per_timestep


        for _ in [float(j * fraction_size) for j in range(0, fractions_per_timestep, 1)]:

            self.x += self.velocity * fraction_size * math.cos(math.radians(self.theta))
            self.y -= self.velocity * fraction_size * math.sin(math.radians(self.theta))
            self.theta += math.degrees((math.tan(math.radians(phi)) / self.L) * fraction_size * self.velocity)
            self.theta %= 360
            #self.theta = -20

        return self.x, self.y, self.theta
        #self.theta += phi
        #self.x += math.cos(self.theta)*100
        #self.y += math.sin(self.theta)*100
        #return self.x, self.y, self.theta,

    #get reward for specific state (currently ignoring the angle theta)
    def get_reward(self, px, py, theta, target):
        #??? to make it realistic, the reward should be one when (almost) on the line and zero when away from the line
        #??? when the car is (+/-1 meter) on the line, it counts as a proper driving behaviour (which the car could observe by and the reward is 0

        distance, flag=target.get_distance(px, py)
        
        #initial approach
        #return 100/(distance+1)
        
        #an aggressive approach
        #return (100/math.pow(distance,2))-((100*theta*flag)/math.pow(distance,3))

        #less aggressive approach
        return (100/distance)-((100*theta*flag)/math.pow(distance,2))

		 
    #take action (steering angle phi) and return reward and new state
    def step(self, phi, target):
        new_state = self.next_state(phi)
        reward = self.get_reward(self.x, self.y, self.theta, target)
        return new_state, reward

"""
model = Single_track_model(45, 3, 5, 0.5)
print(model.get_state())
model.next_state(20)
print(model.get_state())
model.next_state(20)
print(model.get_state())
"""