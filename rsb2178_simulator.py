import random
import math
from matplotlib import pyplot as plt
import numpy as np

def normpdf(x, mean, sd):
    """
    Return the value of the normal distribution 
    with the specified mean and standard deviation (sd) at
    position x.
    You do not have to understand how this function works exactly. 
    """
    var = float(sd)**2
    denom = (2*math.pi*var)**.5
    num = math.exp(-(float(x)-float(mean))**2/(2*var))
    return num/denom

def pdeath(x, mean, sd):
    start = x-0.5
    end = x+0.5
    step =0.01    
    integral = 0.0
    while start<=end:
        integral += step * (normpdf(start,mean,sd) + normpdf(start+step,mean,sd)) / 2
        start += step            
    return integral    
    
recovery_time = 4 # recovery time in time-steps
virality = 0.2    # probability that a neighbor cell is infected in 
                  # each time step    
mean = 5
sd = 2                                   

class Cell(object):

    def __init__(self,x, y):
        self.x = x
        self.y = y 
        self.state = "S" # can be "S" (susceptible), "R" (resistant = dead), or 
                         # "I" (infected)
        self.time = 0
    
    def __str__(self):
        return str(self.x) + ',' + str(self.y)
    
    def infect(self):
        self.state = "I"
        self.time = 0
    
    def process(self, adjacent_cells):
        
        if (self.state == "I" and self.time >= 1):
            
            random_float = random.random()
            
            #Decide if cell recovers
            if (self.time >= recovery_time):
                print(self, "RECOVERS")
                self.state = "S"
    
            #Decide if cell dies
            elif (random_float <= pdeath(self.time, mean, sd)):
                print(self, "DIES")
                self.state = "R"
                    
            #If cell is still infected
            else: 
                
                for cell in adjacent_cells:
                    
                    #Adjacent cell is in S state
                    if (cell.state == "S"):
                        random_float = random.random()
                        #print(cell, ":", random_float)
                        
                        if (random_float <= virality):
                            print("INFECTING", cell)
                            cell.infect()
                                                    
        #Otherwise increment data field 
        else:
            self.time += 1
            
        
class Map(object):
    
    cells = dict()
    
    def __init__(self):
        self.height = 150
        self.width = 150           
        self.cells = {}

    def add_cell(self, cell):
        self.cell = cell
        key = (cell.x, cell.y)
        self.cells[key] = self.cell
        
    def display(self):
        image = []

        for i in range(150):
            image.append([(0,0,0)] * 150)
            
        for x,y in self.cells:
            cell = self.cells[x,y]
            
            #Green
            if (cell.state == "S"):
                image[x][y] = (0,1.0,0)
                
            #Red
            elif (cell.state == "I"):
                image[x][y] = (1.0,0,0)
                
            #Gray
            elif (cell.state == "R"):
                image[x][y] = (0.5,0.5,0.5)
            
        plt.imshow(image)
    
    def adjacent_cells(self, x,y):
        
        results = []
        left = x-1
        right = x+1
        above = y-1
        below = y+1
        
        if left >= 0:
            if (left, y) in self.cells:
                left_cell = self.cells[(left, y)]
                results.append(left_cell)
            
        if right <= 150:
            if (right, y) in self.cells:
                right_cell = self.cells[(right, y)]
                results.append(right_cell)
            
        if above >= 0:
            if (x, above) in self.cells:
                above_cell = self.cells[(x, above)]
                results.append(above_cell)            
    
        if below <= 150:         
            if (x, below) in self.cells:
                below_cell = self.cells[(x, below)]
                results.append(below_cell)
            
        return results
    
    def time_step(self):
        # Update each cell on the map 
        # display the map.
        
        # ... cell.process(adjacent_cells... )
        
        for x,y in self.cells:
            
            cell = self.cells[x,y]
            #cell.time += 1
            cell.process(self.adjacent_cells(x,y))
            
        self.display()
        
def read_map(filename):
    
    m = Map()
    
    f = open(filename,'r')
    
    for line in f:
        coordinates = line.strip().split(',')
        c = Cell(int(coordinates[0]),int(coordinates[1]))
        Map.add_cell(m, c)

    return m
