import math
import n
import enemies

class Tower:
    def __init__(self, position):
        self.name = "tower"
        self.price = 100
        self.position = position
        self.range = 500
        self.selected = False
        self.damage = 1
        self.x = 1
        self.y = 2
        self.radius = 50
        self.selected = False 

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

class Fasttower(Tower):
    def __init__(self, position):
        super().__init__(position)
        self.name = "Fasttower"
        self.price = 150
class tacshooter(Tower):
    def __init__(self, position):
        super().__init__(position)
        self.name = "tacshooter"
        self.price = 300
class Wizardtower(Tower):
    def __init__(self, position):
        super().__init__(position)
        self.name = "Wizardtower"
        self.price = 500