import math
import n
import enemies
import arrow
from other import *

def normalize(x, y):
    return (x**2 + y**2)**.5
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
class Tower:
    def __init__(self, position):
        self.name = "tower"
        self.price = 100
        self.position = position
        self.range = 200
        self.selected = False
        self.x = 1
        self.y = 2
        self.radius = 50
        self.shoot = 30
        self.ammo = 15

    def attack(self, enemies):
        f = None
        for balloon in enemies:
            br, bc = balloon.row, balloon.col
            bx, by, bx1, by1 = getCellBounds(br, bc)
            bcx, bcy = (bx+bx1)/2, (by+by1)/2
            tx = self.position[0]
            ty = self.position[1]
            if distance(bcx, bcy, tx, ty) < self.range:
                if f == None:
                    f = balloon
                elif balloon.pos < f.pos:
                    f = balloon
        if f != None:
            row, col = f.row, f.col
            bx, by, bx1, by1 = getCellBounds(row, col)
            cx, cy = (bx+bx1)/2, (by+by1)/2
            dx, dy = cx - self.position[0], cy - self.position[1]
            #normalize dx, dy
            s =  normalize(dx, dy)
            ddx, ddy = dx/s, dy/s
            return[arrow.arrow(self.position, ddx, ddy)]
        return []


class Fasttower(Tower):
    def __init__(self, position):
        super().__init__(position)
        self.name = "Fasttower"
        self.price = 150
        self.range = 175
        self.shoot = 50

class bishoptower(Tower):
    def __init__(self, position):
        super().__init__(position)
        self.name = "tacshooter"
        self.price = 300
        self.range = 250
        self.shoot = 100
   
    def attack(self, enemies):
        bul = []
        bul.append(arrow.arrow(self.position, -1/(2**.5), -1/(2**.5)))
        bul.append(arrow.arrow(self.position, 1/(2**.5), -1/(2**.5)))
        bul.append(arrow.arrow(self.position, -1/(2**.5), 1/(2**.5)))
        bul.append(arrow.arrow(self.position, 1/(2**.5), 1/(2**.5)))
        return bul

class Wizardtower(Tower):
    def __init__(self, position):
        super().__init__(position)
        self.name = "Wizardtower"
        self.price = 500
        self.range = 300
        self.lx = None
        self.ly = None 
        self.shoot = 20
    def attack(self, enemies):
        i = 0
        while i < len(enemies):
            balloon = enemies[i]
            bx, by, bx1, by1 = getCellBounds(balloon.row, balloon.col)
            bcx, bcy = (bx+bx1)/2, (by+by1)/2
            tx = self.position[0]
            ty = self.position[1]
            if distance(bcx, bcy, tx, ty) < self.range:
                self.lx = bcx
                self.ly = bcy 
                gold = balloon.gold
                enemies.pop(i)
                return (self.lx, self.ly, gold)
            else:
                i += 1
                
        if self.lx == None and self.ly == None:
            return (0,0,0)
        
        