import math
import n
from cmu_112_graphics import *

def distance(x, y, x1, y1):
        return ((x-x1)**2 + (y-y1)**2)**0.5
def board(rows, cols):
    return [[0] * cols for row in range(rows)]
class Enemy(object):    
    def __init__(self, health=1, color="red"):
        self.color = color
        self.health = 1 
        self.rows = 15
        self.cols = 15
        self.board = board(self.rows, self.cols)
        self.peth = []
        self.path1 = n.createmap(self.board, self.peth)[0]    
        self.gold = 15
        self.pathpos = 0
        self.row, self.col = self.peth[0]

   
    def weakerballoon(self):
        self.health = 0
        return self
    def getpos(self):
        return self.row, self.col
    #def move(self):
        #self.row = self.peth[self.pathpos][0]
        #self.col = self.peth[self.pathpos][1]
        #self.pathpos += 1

                        
class BlueBalloon(Enemy):
    def __init__(self):
        super().__init__(self)
        self.color = "blue"
        self.gold = 30
        self.health = 2
    
    def weakerballoon(self):
        balloon = Enemy()
        balloon.row = self.row
        balloon.col = self.col
        return balloon

class GreenBalloon(Enemy):
    def __init__(self):
        super().__init__(self)
        self.color = "green"
        self.gold = 60
        self.health = 3
    
    def weakerballoon(self):
        balloon = BlueBalloon()
        balloon.row = self.row
        balloon.col = self.col
        return balloon

class YellowBalloon(Enemy):
    def __init__(self):
        super().__init__(self)
        self.color = "yellow"
        self.gold = 100
        self.health = 4
    
    def weakerballoon(self):
        balloon = GreenBalloon()
        balloon.row = self.row
        balloon.col = self.col
        return balloon






