import math
import n
from cmu_112_graphics import *

def getCellBounds(row, col):
            cellWidth = 1200 / 15
            cellHeight = 700 / 15
            x0 = col * cellWidth
            x1 = (col+1) * cellWidth
            y0 =  row * cellHeight
            y1 = (row+1) * cellHeight
            return (x0, y0, x1, y1)
def distance(x, y, x1, y1):
        return ((x-x1)**2 + (y-y1)**2)**0.5
def board(rows, cols):
    return [[0] * cols for row in range(rows)]
class Enemy(object):    
    def __init__(self, row, col):
        self.color = "red"
        self.health = 1 
        self.rows = 15
        self.cols = 15
        self.board = board(self.rows, self.cols)
        self.peth = []
        self.path1 = n.createmap(self.board, self.peth)[0]    
        self.gold = 15
        self.pos = 0
        self.row, self.col = row, col
        self.freeze = False 


   
    def weakerballoon(self):
        self.health = 0
        return self
    
    




                        
class BlueBalloon(Enemy):
    def __init__(self, row, col):
        super().__init__(row,col)
        self.color = "blue"
        self.gold = 30
        self.health = 2
        self.row = row 
        self.col = col
        self.pos = 0
        self.freeze = False 
     
    
    def weakerballoon(self):
        balloon = Enemy(self.row, self.col)
        balloon.pos = self.pos
        return balloon

class GreenBalloon(Enemy):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.color = "green"
        self.gold = 60
        self.health = 3
        self.row = row 
        self.col = col
        self.pos = 0
        self.freeze = False 
   
    def weakerballoon(self):
        balloon = BlueBalloon(self.row, self.col)
        balloon.pos = self.pos
        return balloon

class YellowBalloon(Enemy):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.color = "yellow"
        self.gold = 100
        self.health = 4
        self.row = row 
        self.col = col
        self.pos = 0
        self.freeze = False 
    
    def weakerballoon(self):
        balloon = GreenBalloon(self.row, self.col)
        balloon.pos = self.pos
        return balloon

class MetalBalloon(Enemy):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.color = "black"
        self.gold = 100
        self.health = 20
        self.row = row 
        self.col = col
        self.pos = 0
        self.freeze = False 
    
    def weakerballoon(self):
        self.health -=1
        return self




