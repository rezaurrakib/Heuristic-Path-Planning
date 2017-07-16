import math

class single_track_model:

    #x and y will always be different -> just passed to get_next_state function
    #position variables refer to the 2D position of the rear axis!

    def __init__(self, max_theta, L, theta, phi, velocity, timestep_size):
        self.max_theta = max_theta
        self.L = L #vehicle length
        self.theta = theta #car angle
        self.phi = phi #steering angle
        self.velocity = velocity #velocity is assumed to be constant
        self.timestep_size = timestep_size #discretization of time; one action = driving with a fixed steering angle for one timestep

    # compute the position and angle of the car (x_new, y_new, theta_new),
    # depending on the previous state (x_old, y_old, theta_old)
    # and the action(steering angle phi with velocity v for duration of one timestep)
    def get_next_state(self, x_old, y_old, theta_old, phi):

        #simplifying approach (without integrals etc): discretize timestep in to very small fraction
        #for each fraction, assume that the car moves straight (according to theta),
        #but phi changes according to velocity, car length and steering angle
        #that way, the exact new position can be approximated

        # fraction length of one elementary straight movement (0.001 seconds)
        fraction_size = 0.001

        x_new = x_old
        y_new = y_old
        theta_new = theta_old

        for fraction in [float(j) * fraction_size for j in range(0, self.timestep_size, 1)]:
            x_new += self.velocity * fraction_size * math.cos(theta_new)
            y_new += self.velocity * fraction_size * math.sin(theta_new)
            theta_new = (math.tan(phi)/self.L) * fraction_size * self.velocity

        return x_new, y_new, theta_new
