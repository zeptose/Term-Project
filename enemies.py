import math
import map

def distance(x, y, x1, y1):
        return ((x-x1)**2 + (y-y1)**2)**0.5

class Enemy(object):    
    def __init__(self, x, y):
        self.width = 30
        self.height = 65
        self.health = 1
        self.vel = 3
        self.path = map.startend
        self.x = self.path[0][0]
        self.y = self.path[0][1]
        self.pathpos = 0
        self.movecount = 0
        self.totaldist = 0
    
    def checkcollision(self, x, y):
        if x <= self.x + self.width and x >= self.x:
            if y <= self.y + self.height and y >= self.y:
                return True
        return False
    
    def move(self):
        for i in range(len(self.path)):
            x1,y1 = self.path[i][0],self.path[i][1]
            x2,y2 = self.path[i+1][0], self.path[i+1][1]
            self.totaldist += distance(x1,y1,x2,y2)

            if self.totaldist >= 1065:
                self.dir = -1


    