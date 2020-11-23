import math
import map
import enemies

class Tower:

    def __init__(self,x,y):
            self.x = x
            self.y = y
            self.width = 0
            self.height = 0
            self.sell_price = [0,0,0]
            self.price = [0,0,0]
            self.level = 1
            self.selected = False
            # define menu and buttons
            self.menu = Menu(self, self.x, self.y, menu_bg, [2000, "MAX"])
            self.menu.add_btn(upgrade_btn, "Upgrade")

            self.tower_imgs = []
            self.damage = 1

            self.place_color = (0,0,255, 100)


    def collide(self, otherTower):
            x2 = otherTower.x
            y2 = otherTower.y

            dis = math.sqrt((x2 - self.x)**2 + (y2 - self.y)**2)
            if dis >= 100:
                return False
            else:
                return True