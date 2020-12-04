from cmu_112_graphics import *
import enemies
import PIL
import math 
import n
import tkinter
import towers
import random
import arrow

####All images are from CraftPix.net


def getCell(x, y):
    cellWidth  = 1200/15
    cellHeight = 700/15
    row = int((y) / cellHeight)
    col = int((x) / cellWidth)
    return (row, col)

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
def board(rows, cols):
    return [[0] * cols for row in range(rows)]

class MyApp(App):

    def appStarted(self):
        self.rows = 15
        self.cols = 15
        self.towers = []
        self.bullets = []
        self.enemies = []
        self.gold = 1000
        self.lives = 100
        self.gameOver = False
        self.paused = False

        self.cantafford = False 
        self.placetower = None
        self.illegal = False 

        self.clock = 0
       
        self.pathpos = 0
        self.board = board(self.rows, self.cols)
        self.path = []
        self.board1 = n.createmap(self.board, self.path)
        self.boardd = self.board1[0]

        self.image = self.loadImage("Images/landv2.png")
        width, height = self.image.size
        scaleFactor = 80/width
        self.image = self.scaleImage(self.image, scaleFactor)
        
        self.image2 = self.loadImage("Images/landv1.png")
        width1, height1 = self.image2.size
        scaleFactor1 = 80/width1
        self.image2 = self.scaleImage(self.image2, scaleFactor1)

        self.image3 = self.loadImage("Images/13.png")
        width, height = self.image3.size
        self.image3 = self.scaleImage(self.image3, 80/width)
        
        self.image4 = self.loadImage("Images/decor_9.png")
        width, height = self.image4.size
        self.image4 = self.scaleImage(self.image4, 80/width)
        
        self.image5 = self.loadImage("Images/11.png")
        width, height = self.image5.size
        self.image5 = self.scaleImage(self.image5, 80/width)
       
        self.image6 = self.loadImage("Images/20.png")
        width, height = self.image6.size
        self.image6 = self.scaleImage(self.image6, 80/width)
        self.image7 = self.loadImage("Images/22.png")
        width, height = self.image7.size
        self.image7 = self.scaleImage(self.image7, 20/width)
        self.lix = None
        self.liy = None 
        self.lightning = []
        self.bolts = []


    def addTower(self, x, y):
        tower = towers.Tower((x,y))
        self.towers.append(tower)
    
    
    def spawnv2(self):
        while len(self.enemies) < 5:
            i = random.randint(0, 3)
            if i == 0:
                self.enemies.append(enemies.Enemy(self.path[0][0], self.path[0][1]))
                return 
            elif i == 1:
                self.enemies.append(enemies.BlueBalloon(self.path[0][0], self.path[0][1]))
                return 
            elif i == 2:
                self.enemies.append(enemies.GreenBalloon(self.path[0][0], self.path[0][1]))
                return 
            elif i == 3:
                self.enemies.append(enemies.YellowBalloon(self.path[0][0], self.path[0][0]))
                return 


    def mousePressed(self, event):
        if self.gameOver: return 
        if not self.paused:
            if self.placetower != None:
                if self.legalplace(event.x, event.y, 50):
                    self.illegal = False
                    towers.position = (event.x, event.y)
                    self.towers.append(self.placetower)
                    self.gold -= self.placetower.price
                    self.placetower = None    
                else:
                    self.illegal = True 
            if self.towers != []:
                for tower in self.towers:
                    if isinstance(tower, towers.Tower):
                        w,h = self.image3.size
                        if event.x <= tower.position[0] + w/2 and event.x >= tower.position[0] - w/2:
                            if event.y <= tower.position[1] + h/2 and event.y >=  tower.position[1] - h/2:
                                tower.selected = True 
                        else:
                            tower.selected = False 
                    elif isinstance(tower, towers.Fasttower):
                        w,h = self.image5.size
                        if event.x <= tower.position[0] + w/2 and event.x >= tower.position[0] - w/2:
                            if event.y <= tower.position[1] + h/2 and event.y >=  tower.position[1] - h/2:
                                tower.selected = True 
                        else:
                            tower.selected = False 
                    elif isinstance(tower, towers.tacshooter):
                        w,h = self.image4.size
                        if event.x <= tower.position[0] + w/2 and event.x >= tower.position[0] - w/2:
                            if event.y <= tower.position[1] + h/2 and event.y >=  tower.position[1] - h/2:
                                tower.selected = True 
                        else:
                            tower.selected = False 
                    elif isinstance(tower, towers.Wizardtower):
                        w,h = self.image6.size
                        if event.x <= tower.position[0] + w/2 and event.x >= tower.position[0] - w/2:
                            if event.y <= tower.position[1] + h/2 and event.y >=  tower.position[1] - h/2:
                                tower.selected = True 
                        else:
                            tower.selected = False 
            if len(self.bolts) > 0:
                i = 0
                while i < len(self.bolts):
                    bolt = self.bolts[i]
                    w,h = self.image7.size
                    if distance(event.x, event.y, bolt[0], bolt[1]) <= h:
                 #   if event.x <= bolt[0] + w/2 and event.x >= bolt[0] - w/2:
                     #   if event.y <= bolt[0] + h/2 and event.y>= bolt[1] - h/2:
                            self.gold += 50
                            self.bolts.pop(i)
                            self.lightning.pop(i)
                    else:
                        i += 1

    
    def mouseMoved(self, event):
        if self.placetower != None:
            self.placetower.position = (event.x, event.y)
    
    def timerFired(self):
        self.clock += 1
        if self.lives <= 0:
            self.gameOver = True 
        if self.gameOver: return
        if not self.paused:
            if self.clock % 3 == 0:
                self.spawnv2()
                for balloon in self.enemies:
                    if self.pathpos < len(self.path):
                        if isinstance(balloon, enemies.BlueBalloon):
                            balloon.row = self.path[balloon.pos][0]
                            balloon.col = self.path[balloon.pos][1]
                            if balloon.pos < len(self.path) - 1:
                                balloon.pos += 1
                            else:
                                self.removeenemies()
                                balloon.pos = 0
                    
                        elif isinstance(balloon, enemies.Enemy):
                            balloon.row = self.path[balloon.pos][0]
                            balloon.col = self.path[balloon.pos][1]
                            if balloon.pos < len(self.path) - 1:
                                balloon.pos += 1
                            else:
                                self.removeenemies()
                                balloon.pos = 0
                        
                        elif isinstance(balloon, enemies.GreenBalloon):
                            balloon.row = self.path[balloon.pos][0]
                            balloon.col = self.path[balloon.pos][1]
                            if balloon.pos < len(self.path) - 1:
                                balloon.pos += 1
                            else:
                                self.removeenemies()
                                balloon.pos = 0

                        elif isinstance(balloon, enemies.YellowBalloon):
                            balloon.row = self.path[balloon.pos][0]
                            balloon.col = self.path[balloon.pos][1]
                            if balloon.pos < len(self.path) - 1:
                                balloon.pos += 1
                            else:
                                self.removeenemies()
                                balloon.pos = 0
            if self.clock % 4 == 0:
                for tower in self.towers:
                    if not isinstance(tower, towers.Wizardtower):
                        bul = tower.attack(self.enemies)
                        self.bullets.append(bul)
                        i = 0
                        while i < len(self.bullets):
                            print(len(self.bullets))
                            bullet = self.bullets[i]
                            x0 = bullet.position[0]
                            y0 = bullet.position[1]
                            x1 = x0 - (bullet.dx + bullet.speed)
                            y1 = y0 - (bullet.dy + bullet.speed)
                            bullet.position = (x1, y1)
                            print(bullet.position)
                            if bullet.checkcollision(self.enemies):
                                self.bullets.pop(i)
                                self.gold += 3
                            elif distance(x1, y1, x0, y0) >= bullet.range:
                                self.bullets.pop(i)
                            else:   
                                i += 1
                    else:
                        if self.clock % 5 == 0:
                            if tower.shoot != 0:
                                self.lix, self.liy, gold = tower.attack(self.enemies)
                                tower.shoot -= 1
                                self.gold += gold
                                self.lightning.append((self.lix, self.liy))
                                self.bolts.append((self.lix, self.liy))
    
                            
                                        
                             
    def removeenemies(self):
        result = []
        for balloon in self.enemies:
            if balloon.pos < len(self.path) - 1:
                continue
            else:
                result.append(balloon)
        for balloon in result:
            self.lives -= balloon.health   
            self.enemies.remove(balloon)

    def legalplace(self, x,y, towerrange):
        r,c = getCell(x,y)
        if self.boardd[r][c] == 1 or (r,c) in self.path:
            return False 
        for tower in self.towers:
            if distance(x,y,tower.position[0],tower.position[1]) < tower.radius * 2:
                return False 
 
        for balloon in self.enemies:
            x1,y1 = getCell(balloon.row, balloon.col)
            if distance(x,y,x1,y1) < 65:
                return False 
        return True 

            

    def keyPressed(self, event):
        if event.key == "p":
            self.paused = not self.paused
        if event.key == "a":   
            if self.gold >= towers.Tower((1,1)).price:  
                self.placetower = towers.Tower((1,1))
                self.cantafford = False 
            else:
                self.cantafford = True 
        elif event.key == "m":
            if self.gold >= towers.Wizardtower((1,1)).price:  
                self.placetower = towers.Wizardtower((1,1))
                self.cantafford = False 
            else:
                self.cantafford = True 
        elif event.key == "t":
            if self.gold >= towers.tacshooter((1,1)).price:  
                self.placetower = towers.tacshooter((1,1))
                self.cantafford = False 
            else:
                self.cantafford = True 
        elif event.key == "f":
            if self.gold >= towers.Fasttower((1,1)).price:  
                self.placetower = towers.Fasttower((1,1))
                self.cantafford = False 
            else:
                self.cantafford = True 
        elif event.key == "l":
            self.lives = 0
        elif event.key == "z":
            self.gold = 10000



    def drawenemies(self, canvas): 
        r = 15
        for balloon in self.enemies:
            brow = balloon.row
            bcol = balloon.col
            x0,y0,x1,y1 = getCellBounds(brow,bcol)
            cx = (x0+x1)/2
            cy = (y0+y1)/2
            canvas.create_oval(cx-r, cy+r, cx+r, cy-r, fill=balloon.color)
    
    def drawtowerrange(self, canvas):
        for tower in self.towers:
            if tower.selected:
                x,y = x,y = tower.position[0], tower.position[1]
                r = tower.range
                canvas.create_oval(x-r, y-r, x+r, y+r)
   
    def drawtowers(self, canvas):
        for tower in self.towers:
            x,y = tower.position[0], tower.position[1]
            r = tower.radius
            if isinstance(tower, towers.Fasttower):
                canvas.create_image(x, y, image=ImageTk.PhotoImage(self.image5))
            elif isinstance(tower, towers.tacshooter):
                canvas.create_image(x, y, image=ImageTk.PhotoImage(self.image4))
            elif isinstance(tower, towers.Wizardtower):
                canvas.create_image(x, y, image=ImageTk.PhotoImage(self.image6))
            elif isinstance(tower, towers.Tower):
                canvas.create_image(x, y, image=ImageTk.PhotoImage(self.image3))

    def drawstats(self, canvas):
        canvas.create_text(1100, 15, text=f"Health: {self.lives}", fill="red", font="Arial 15 bold")
        canvas.create_text(990, 15, text=f"gold: {self.gold}", fill="yellow", font="Arial 15 bold")
    def drawinstructions(self, canvas):
        pass
    def drawstart(self, canvas):
        pass
    def drawbullets(self, canvas):
        for bullet in self.bullets:
            x,y = bullet.position[0], bullet.position[1]
            r = bullet.radius
            canvas.create_oval(x-r, y-r, x+r, y+r, fill="black")
            canvas.create_oval(50,50,100,100, fill="black")
    def drawlightning(self, canvas):
        for bolt in self.lightning:
            x,y = bolt[0], bolt[1]
            canvas.create_image(x,y, image=ImageTk.PhotoImage(self.image7))
  
    def redrawAll(self, canvas):
        for row in range(self.rows):
            for col in range(self.cols):
                x0,y0,x1,y1 = getCellBounds(row, col)
                cx,cy = (x0+x1)/2, (y0+y1)/2
                if self.boardd[row][col] == 0:
                    canvas.create_rectangle(x0,y0,x1,y1, fill="lightgreen")
                    canvas.create_image(cx,cy, image=ImageTk.PhotoImage(self.image))
                elif self.boardd[row][col] == 1:
                    canvas.create_rectangle(x0,y0,x1,y1, fill="brown")
                    canvas.create_image(cx,cy,image=ImageTk.PhotoImage(self.image2))
        MyApp.drawtowerrange(self, canvas)    
        MyApp.drawtowers(self, canvas)
        MyApp.drawstats(self, canvas)            
        MyApp.drawbullets(self, canvas)
        MyApp.drawenemies(self, canvas)  
        MyApp.drawlightning(self, canvas)
        if self.placetower != None:
            x = self.placetower.position[0]
            y = self.placetower.position[1]
            r = 50
            canvas.create_oval(x-r, y-r, x+r, y+r, fill="grey")
        if self.cantafford == True:
            canvas.create_text(self.width/2, self.height/2, text="You can't afford that right now, defeat more balloons in order to earn more gold")
        if self.illegal == True:
            canvas.create_text(self.width/2, self.height/2, text="You can't place that here")
        if self.lives <= 0:
            canvas.create_rectangle(20,20, 1000,1000, fill="yellow")
            canvas.create_text(500,300, text="GAMEOVER!", fill="black", font="Arial 50")
            canvas.create_text(500,500, text="You lost all your lives D:", fill="black", font="Arial 50")
MyApp(width=1200, height=700)

