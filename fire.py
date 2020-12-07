## file for tower 
# Fire on path, burns bloons, if metal and frozen it becomes yellow 


class Fire:
    def __init__(self, position):
        self.position = position
        self.price = 700
        self.radius = 50 
        self.damage = 1
        self.selected = False 