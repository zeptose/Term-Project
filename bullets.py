#import Weapons
import PIL
import math
import os
import enemies
import n 

class arrow()
def checkcollision(x,y,w,h,x2,y2,w2,h2):
    if x + w >= x2 and y + h >= y2 and x <= x2 + w2 and y <= y2 + h2:
        return True
    else:
        return False

#regular arrows and lightning for mage 
