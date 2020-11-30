from cmu_112_graphics import *
import enemies
import PIL
import math 
import n
import tkinter
import weapons

waves = [
    [20, 0, 0,0],
    [50, 0, 0,0],
    [80, 20, 0,0],
    [0, 70, 0,0],
    [0, 50, 0, 1],
    [0, 100, 0,5],
    [20, 100, 20,10],
    [50, 80, 60,30],
    [100, 100, 100],
    [0, 0, 50, 150]
]
def getCell(x, y):
    cellWidth  = 1200/15
    cellHeight = 700/15
    row = int((y - app.margin) / cellHeight)
    col = int((x - app.margin) / cellWidth)
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
        self.gold = 100
        self.lives = 100
        self.gameOver = False
        self.paused = False
        self.board = board(self.rows, self.cols)
        self.image = self.loadImage("Images/land.png")
        width, height = self.image.size
        scaleFactor = 80/width
        self.image = self.scaleImage(self.image, scaleFactor)
        self.image2 = self.loadImage("Images/land1.png")
        width1, height1 = self.image2.size
        scaleFactor1 = 80/width1
        self.image2 = self.scaleImage(self.image2, scaleFactor1)
        self.path = []
        self.board1 = n.createmap(self.board, self.path)
        print(self.path)
        self.boardd = self.board1[0]
        self.wave = 0
        self.currwave = waves[self.wave]
        self.clock = 0
        self.image3 = self.loadImage("Images/12.png")
        self.image3 = self.scaleImage(self.image3, scaleFactor)
        self.image4 = self.loadImage("Images/decor_9.png")
        self.image4 = self.scaleImage(self.image4, 0.5)
        self.image5 = self.loadImage("Images/3.png")
        self.image5 = self.scaleImage(self.image5, scaleFactor)
        self.r = self.path[0][0]
        self.c = self.path[0][1]
        print(self.r, self.c)
        self.enemies = [enemies.Enemy()]
    
    def mousePressed(self, event):
        if self.legalplace(event.x, event.y, 30):
            weapons.location = (event.x, event.y)
            self.towers.append(weapons.tower.location)
            self.gold -= weapons.tower.price

    
    def spawnBalloons(self):
        if sum(self.currwave) == 0: 
            if self.wave != 10:
                self.wave += 1
                self.currwave = waves[self.wave]
            else:
                self.gameOver = True 
        else:
            balloons = [enemies.Enemy(), enemies.BlueBalloon(), enemies.GreenBalloon(), enemies.YellowBalloon()]
            for elem in range(len(self.currwave)):
                if self.currwave[elem] != 0:
                    self.enemies.append(balloons[elem])
                    self.currwave[elem] =  self.currwave[elem] - 1
                    break
        
    def timerFired(self):
        self.clock += 1
        if self.gameOver: return  
        if self.clock % 2 == 0:
          #  self.spawnBalloons()
            for balloon in self.enemies:
                print(balloon.row, balloon.col)
                balloon.move() 
                
                self.removeenemies()
    
    def legalplace(self, x,y, towerrange):
        r,c = getCell(x,y)
        if self.boardd[r][c] == 1:
            return False 
        for tower in self.towers:
            if distance(x,y,tower.position[0],tower.position[1]) > towerrange * 2:
                return False 
        for balloon in self.enemies:
            if distance(x,y,tower.position[0],tower.position[1]) > towerrange + 15:
                return False 
        return True 

            

    def keyPressed(self, event):
        if event.key == "p":
            self.paused = not self.paused
        if event.key == "a":   
            pass
        elif event.key == "m":
            pass
        elif event.key == "t":
            pass
        elif event.key == "r":
            pass
    
    def removeenemies(self):
        result = []
        for balloon in self.enemies:
            if balloon.row >= balloon.endrow and balloon.col >= balloon.endcol:
                result.append(balloon)
        for balloon in result:
            self.lives -= balloon.health   
            self.enemies.remove(balloon)

    def drawenemies(self, canvas): 
        r = 15
        for balloon in self.enemies:
            brow = balloon.row
            bcol = balloon.col
            x0,y0,x1,y1 = getCellBounds(brow,bcol)
            cx = (x0+x1)/2
            cy = (y0+y1)/2
            canvas.create_oval(cx-r, cy+r, cx+r, cy-r, fill=balloon.color)

    def drawtowers(self, canvas):
        canvas.create_image(100,100, image=ImageTk.PhotoImage(self.image4))

    def redrawAll(self, canvas):
        for row in range(self.rows):
            for col in range(self.cols):
                x0,y0,x1,y1 = getCellBounds(row, col)
                cx,cy = (x0+x1)/2, (y0+y1)/2
                if self.boardd[row][col] == 0:
                    canvas.create_rectangle(x0,y0,x1,y1, fill="lightgreen")
                   # canvas.create_image(cx,cy, image=ImageTk.PhotoImage(self.image))
                elif self.boardd[row][col] == 1:
                    canvas.create_rectangle(x0,y0,x1,y1, fill="brown")
                  #  canvas.create_image(cx,cy,image=ImageTk.PhotoImage(self.image2))
        MyApp.drawenemies(self, canvas)       
        MyApp.drawtowers(self, canvas)

        
def checkcollision(x,y,w,h,x2,y2,w2,h2):
    if x + w >= x2 and y + h >= y2 and x <= x2 + w2 and y <= y2 + h2:
        return True
    else:
        return False






MyApp(width=1200, height=700)

