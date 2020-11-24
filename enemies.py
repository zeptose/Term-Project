import math
import map
from cmu_112_graphics import *

def distance(x, y, x1, y1):
        return ((x-x1)**2 + (y-y1)**2)**0.5

class Enemy(object):    
    def __init__(self, x, y):
        self.width = 30
        self.height = 65
        self.health = 1
        self.vel = 3
        self.rows = 15
        self.cols = 15
        self.board = map.board(self.rows, self.cols)
        self.path = map.startend(self.board)
        self.x = 1
        self.y = 1
        self.pathpos = 0
        self.movecount = 0
        self.totaldist = 0
    
    def checkcollision(self, x, y):
        if x <= self.x + self.width and x >= self.x:
            if y <= self.y + self.height and y >= self.y:
                return True
        return False
    
    def move(self):
        for row in range(len(self.path)):
            for col in range(len(self.path)):
                if self.path[row][col] == 1:
                    pass

                    


    