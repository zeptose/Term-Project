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
        self.path = n.createmap(self.board)
        self.row = None
        self.col = -1
        self.endrow = None
        self.endcol = 14
        self.gold = 15
    def weakerballoon(self):
        self.health = 0
        return self
    
    def start(self):
        for row in range(len(self.path)):
            if self.path[row][0] == 1:
                self.col += 1
                self.row = row
                return (self.col, self.row)
    def end(self):
        for row in range(len(self.path)):
            if self.path[row][14] == 1:
                self.endrow = row
                return (self.endcol, self.endrow)

   # def move(self):
       # x,y = Enemy.start(self)
       # x1,y1 = Enemy.end(self)

      #  result = Enemy.moveindir(self, x, y, x1, y1)
       # if result != None:
         #   return result
       # else:
          #  return None
    #def moveindir(self, row, col, erow, ecol):
       # rows, cols = len(self.path), len(self.path)
       # dirs = [(0,1), (1,0), (-1,0)] 
       # if row >= erow and col >= ecol:
       #     return True 
      #  for move in dirs:
        #    newrow = row + move[0]
        #    newcol = col + move[1]
        #    if newrow >= 0 and newrow < rows and newcol >= 0 and newcol < cols:
         #       if self.path[newrow][newcol] == 1:
          #          return Enemy.moveindir(self, newrow, newcol, erow, ecol)
        #return None

    def move(self):
        self.col,self.row = Enemy.start(self)
        self.endcol,self.endrow = Enemy.end(self)
        rows, cols = len(self.path), len(self.path)
        dirs = [(0,1), (1,0), (-1,0)] 
        if self.row != 14 and self.col != self.endcol:
            newcol = self.col + dirs[0][1]
            newrow = self.row + dirs[0][0]
            if newrow >= 0 and newrow < rows and newcol >= 0 and newcol < cols:
                if self.path[newrow][newcol] == 1:
                    self.col = newcol
                    self.row = newrow
                else:
                    newcol = self.col + dirs[1][0]
                    newrow = self.row + dirs[1][1]
                    if newrow >= 0 and newrow < rows and newcol >= 0 and newcol < cols:
                        if self.path[newrow][newcol] == 1:
                            self.col = newcol
                            self.row = newrow
        elif self.row == 14 and self.col != self.endcol:
            newcol = self.col + dirs[2][1]
            newrow = self.row + dirs[2][0]
            if newrow >= 0 and newrow < rows and newcol >= 0 and newcol < cols:
                if self.path[newrow][newcol] == 1:
                    self.col = newcol
                    self.row = newrow
                else:
                    newcol = self.col + dirs[1][0]
                    newrow = self.row + dirs[1][1]
                    if newrow >= 0 and newrow < rows and newcol >= 0 and newcol < cols:
                        if self.path[newrow][newcol] == 1:
                            self.col = newcol
                            self.row = newrow

                        
class BlueBalloon(Enemy):
    def __init__(self):
        super().__init__(self)
        self.color = "blue"
        self.gold = 30
    def weakerballoon(self):
        balloon = Enemy()
        return balloon

class GreenBalloon(Enemy):
    def __init__(self):
        super().__init__(self)
        self.color = "green"
        self.gold = 60
    def weakerballoon(self):
        balloon = BlueBalloon()
        return balloon

class YellowBalloon(Enemy):
    def __init__(self):
        super().__init__(self)
        self.color = "yellow"
        self.gold = 100
    def weakerballoon(self):
        balloon = GreenBalloon()
        return balloon



  

                    


    