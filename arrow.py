#File for all things shooting related 
import PIL
import math
import os
import enemies
import n 
import towers
import random 
from other import *

### Collision check inspired from my Hack112 Projectile collision https://github.com/mattngaw/122.io/blob/main/Weapons.py

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
    
    def checkcollision(self, enemy):
        for balloon in enemy:
            if self.hit(balloon):
                if not isinstance(balloon, enemies.MetalBalloon):
                    newbloon = balloon.weakerballoon()
                    enemy.remove(balloon) 
                    if newbloon.health > 0:
                        enemy.append(newbloon)
                    return True 
                else:
                    if balloon.freeze == True: 
                        if self.hit(balloon):
                            newbloon = balloon.weakerballoon()
                            enemy.remove(balloon) 
                            if newbloon.health > 0:
                                enemy.append(newbloon)
                            return True
        return False 
                
            
 
    def hit(self, balloon):
        x,y = self.position[0], self.position[1]
        x0, y0 = x - (self.speed*self.dx), y-(self.speed*self.dy)
        br, bc = balloon.row, balloon.col
        bx, by, bx1, by1 = getCellBounds(br, bc)
        bcx, bcy = (bx+bx1)/2, (by+by1)/2
        
        #collision occurs
        if distance(x0, y0, bcx, bcy) <= self.radius + 15 or self.dx == 0 or self.dy == 0:
            return True 

        #else change x0, y0 until there is collision    
        else:
            dx, dy = x-x0, y-y0
            a = distance(bcx, bcy, x, y)
            if a <= self.radius + 15:
                return True
            x0 += dx / 10
            y0 += dy / 10
            return False



