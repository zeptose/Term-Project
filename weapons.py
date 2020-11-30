import math
import n
import enemies

class Tower:
    def __init__(self, position):
        self.name = "tower"
        self.price = 100
        self.position = position
        self.range = 50 
        self.level = 1
        self.selected = False
        self.tower_imgs = []
        self.damage = 1
        self.x = 1
        self.y = 2
        

    def attacK(self):
        pass
   
    def collide(self, otherTower):
            x2 = otherTower.x
            y2 = otherTower.y
            dis = math.sqrt((x2 - self.x)**2 + (y2 - self.y)**2)
            if dis >= 100:
                return False
            else:
                return True