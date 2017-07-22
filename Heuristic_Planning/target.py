import math

class Target_Line:

    #initialize target line with two points
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        if x1 == x2 and y1 == y2:
            raise ValueError('Invalid line initialization: points coincide')

    #compute distance between point and target line
    def get_distance(self, px, py):
        nominator = math.fabs(((self.x2-self.x1)*(self.y1-py)) - ((self.x1-px)*(self.y2-self.y1)))
        denominator = math.sqrt((self.x2-self.x1)**2 + (self.y2-self.y1)**2)
        return nominator / denominator