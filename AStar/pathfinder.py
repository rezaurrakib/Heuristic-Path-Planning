import heapq 
import math

class Cell(object):
    def __init__(self, x, y, reachable):
        
        # Initialize new cell
        
        self.reachable = reachable # can a cell be reachable -might be an obstacle/wall-?
        self.x = x
        self.y = y
        self.parent = None
        
        # g(x) = cost of getting to that node from starting node.
        # h(x) = cost of getting to the goal node from current node.
        # f(x) = g(x)+h(x)

        self.g = 0
        self.h = 0
        self.f = 0


class AStar(object):
    def __init__(self):
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = set()
        self.cells = []
        self.grid_height = 10
        self.grid_width = 10


    def init_grid(self):
        walls = ((0, 5), (1, 0), (1, 1), (1, 5), (2, 3), 
                 (4, 5), (5, 5), (3, 7), (7, 7), (8, 7), (9, 7))
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if (x, y) in walls:
                    reachable = False
                else:
                    reachable = True
                self.cells.append(Cell(x, y, reachable))
        self.start = self.get_cell(0, 0)
        self.end = self.get_cell(8, 9)


    def get_heuristic(self, cell, option):
        
        # Heuristic val. H is calculated fo currenct cell to ending cell and multiplied by 10.
        
        result = 0
        if (option==0):     #euclidean distance
            dx, dy = abs(cell.x - self.end.x), abs(cell.y - self.end.y)
            result = 10 * (math.hypot(dx, dy)) 
        else:               #manhattan distance            
            result = 10 * (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))
        return result

    def get_cell(self, x, y):
        
        # Returns a cell from cells list
        
        return self.cells[x * self.grid_height + y]


    def get_adjacent_cells(self, cell):
        
        # Returns adjecent cells to a cell. Clockwise action starts with the one on the right.

        cells = []
        if cell.x < self.grid_width-1:
            cells.append(self.get_cell(cell.x+1, cell.y))
        if cell.y > 0:
            cells.append(self.get_cell(cell.x, cell.y-1))
        if cell.x > 0:
            cells.append(self.get_cell(cell.x-1, cell.y))
        if cell.y < self.grid_height-1:
            cells.append(self.get_cell(cell.x, cell.y+1))
        return cells


    def display_path(self):

        # Shows the path that is followed by the algorithm according to different heuristics mechanisms.

        cell = self.end
        while cell.parent is not self.start:
            cell = cell.parent
            print 'path: cell: %d,%d' % (cell.x, cell.y)


    def update_cell(self, adj, cell, option):
        
        # Update adjacent cell

        adj.g = cell.g + 10
        adj.h = self.get_heuristic(adj,option)
        adj.parent = cell
        adj.f = adj.h + adj.g

    def process(self, option):
    # add starting cell to open heap queue
        if (option==0):
            print "\nHeuristic Option is set to: Euclidean Distance!"
        else: 
            print "\nHeuristic Option is set to: Manhattan Distance!"
        heapq.heappush(self.opened, (self.start.f, self.start))
        while len(self.opened):
            # pop cell from heap queue 
            f, cell = heapq.heappop(self.opened)
            # add cell to closed list so we don't process it twice
            self.closed.add(cell)
            # if ending cell, display found path
            if cell is self.end:
                self.display_path()
                break
            # get adjacent cells for cell
            adj_cells = self.get_adjacent_cells(cell)
            for adj_cell in adj_cells:
                if adj_cell.reachable and adj_cell not in self.closed:
                    if (adj_cell.f, adj_cell) in self.opened:
                        # if adj cell in open list, check if current path is
                        # better than the one previously found for this adj
                        # cell.
                        if adj_cell.g > cell.g + 10:
                            self.update_cell(adj_cell, cell, option)
                    else:
                        self.update_cell(adj_cell, cell, option)
                        # add adj cell to open list
                        heapq.heappush(self.opened, (adj_cell.f, adj_cell))

A=AStar()
A.init_grid()
A.process(0)
B=AStar()
B.init_grid()
B.process(1)