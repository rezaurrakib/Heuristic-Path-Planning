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
    def next_state(self, theta_old, phi):

        #simplifying approach (without integrals etc): discretize timestep in to very small fraction
        #for each fraction, assume that the car moves straight (according to theta),
        #but phi changes according to velocity, car length and steering angle
        #that way, the exact new position can be approximated

        # fraction length of one elementary straight movement (0.001 seconds)
        fraction_size = 0.001

        x_new = self.x
        y_new = self.y
        theta_new = theta_old

        for _ in [float(j) * fraction_size for j in range(0, self.timestep_size, 1)]:
            x_new += self.velocity * fraction_size * math.cos(theta_new)
            y_new += self.velocity * fraction_size * math.sin(theta_new)
            theta_new = (math.tan(phi)/self.L) * fraction_size * self.velocity

        self.x = x_new
        self.y = y_new
        self.theta = theta_new

        return x_new, y_new, theta_new

    #get reward for specific state (currently ignoring the angle theta, just using distance to target)
    def get_reward(self, px, py, theta, target):
        return 100/(target.get_distance(px, py)+1)

    #take action (steering angle phi) and return reward and new state
    def step(self, phi, target):
        new_state = self.next_state()
        reward = self.get_reward(self.x, self.y, self.theta, target)
        return new_state, reward
