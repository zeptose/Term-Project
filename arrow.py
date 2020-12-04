#import Weapons
import PIL
import math
import os
import enemies
import n 
import towers
import random 

def distance(x, y, x1, y1):
        return ((x-x1)**2 + (y-y1)**2)**0.5

def getCellBounds(row, col):
        cellWidth = 1200 / 15
        cellHeight = 700 / 15
        x0 = col * cellWidth
        x1 = (col+1) * cellWidth
        y0 =  row * cellHeight
        y1 = (row+1) * cellHeight
        return (x0, y0, x1, y1)

class arrow(object):
    def __init__(self, position, dx, dy):
        self.position = position
        self.dx = dx
        self.dy = dy 
        self.speed = 50
        self.radius = 10
        self.range = 200
    
    def checkcollision(self, enemies):
        for balloon in enemies:
            if self.hit(balloon):
                newbloon = enemies.weakerballoon()
                enemies.remove(balloon) 
                if newbloon.health > 0:
                    enemies.append(newbloon)
            print("hi")
            return True 
        return False 
 
    def hit(self, balloon):
        x,y = self.position[0], self.position[1]
        x0, y0 = x - (self.speed*self.dx), y-(self.speed*self.dy)
        br, bc = balloon.row, balloon.col
        bx, by, bx1, by1 = getCellBounds(br, bc)
        bcx, bcy = (bx+bx1)/2, (by+by1)/2
     #  self.dx, self.dy = x-x0, y-y0
        #collision occurs
        if distance(x0, y0, bcx, bcy) <= self.radius + 15:
            return True 
       # elif distance(x, y0, bcx, bcy) <= self.radius + 15:
        #    return True 
        if self.dy == 0:
            if abs(y-bcy) < self.radius + 15:
                if (y0<=bcy<=y) or (y<=bcy<=y0):
                    return True 
            return False 
        elif self.dx == 0:
            if abs(x-bcx) < self.radius + 15:
                if (x0<=bcx<=x) or (x<=bcx<=x0):
                    return True 
            return False 

        else:
            self.dx, self.dy = x-x0, y-y0
            for x in range(20):
                a = distance(bcx, bcy, x, y)
                if a <= self.radius + 15:
                    return True
                x0 += self.dx / 20
                y0 += self.dy / 20
            return False



