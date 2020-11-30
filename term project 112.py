from cmu_112_graphics import *
import enemies
import PIL
import math 
import n
import tkinter
import towers

waves = [
    [5, 0, 0,0],
    [15, 0, 0,0],
    [5, 10, 0,0],
    [0, 20, 0,0],
    [0, 3, 10, 0 ],
    [0, 0, 20,5],
    [0, 0, 0,20],
    [20, 20, 20,20],
    [0, 30, 40,40],
    [0, 0, 50, 50]
]
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
        self.gold = 1000
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
        self.enemies = []
        self.cantafford = False 
        self.placetower = None
        self.placeMagetower = None 
        self.illegal = False 
        self.pathpos = 0
        self.endcol = 14
        self.endrow = self.path[-1][0]

    def addTower(self, x, y):
        tower = towers.Tower((x,y))
        self.towers.append(tower)
        
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
  
    def mousePressed(self, event):
        if self.placetower != None:
            if self.legalplace(event.x, event.y, 50):
                self.illegal = False
                towers.location = (event.x, event.y)
                self.towers.append(self.placetower)
                print("hi")
                self.gold -= self.placetower.price
                self.placetower = None    
            else:
                self.illegal = True 

    def timerFired(self):
        self.clock += 1
        if self.gameOver: return  
        if self.clock % 3 == 0:
            self.spawnBalloons()
            for balloon in self.enemies:
                if self.pathpos < len(self.path):
                    balloon.row = self.path[self.pathpos][0]
                    balloon.col = self.path[self.pathpos][1]
                    self.pathpos += 1
                elif self.pathpos >= len(self.path):
                    #self.pathpos = 0
                    #balloon.row = self.path[self.pathpos][0]
                    #balloon.col = self.path[self.pathpos][1]
                    self.removeenemies()


    def legalplace(self, x,y, towerrange):
        r,c = getCell(x,y)
        if self.boardd[r][c] == 1 or (r,c) in self.path:
            return False 
        for tower in self.towers:
            if distance(x,y,tower.position[0],tower.position[1]) > towerrange * 2:
                return False   
        for balloon in self.enemies:
            x1,y1 = getCell(balloon.row, balloon.col)
            if distance(x,y,x1,y1) > towerrange + 15:
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
            pass
        elif event.key == "t":
            pass
        elif event.key == "r":
            pass
    
    def removeenemies(self):
        result = []
        for balloon in self.enemies:
            if self.pathpos < len(self.path):
                continue
            else:
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
    def drawtowerrange(self, canvas):
        pass
    def drawtowers(self, canvas):
        for tower in self.towers:
            x,y = tower.location[0], tower.location[1]
            r = tower.radius
            if isinstance(tower, towers.Tower):
                canvas.create_image(x, y, image=ImageTk.PhotoImage(self.image3))
            elif isinstance(tower, towers.Fasttower):
                canvas.create_image(x, y, image=ImageTk.PhotoImage(self.image4))
            elif isinstance(tower, towers.tacshooter):
                canvas.create_image(x, y, image=ImageTk.PhotoImage(self.image3))
            elif isinstance(tower, towers.Wizardtower):
                canvas.create_image(x, y, image=ImageTk.PhotoImage(self.image5))
       
        canvas.create_image(100,100, image=ImageTk.PhotoImage(self.image4))
    def drawstats(self, canvas):
        canvas.create_text(1100, 15, text=f"Health: {self.lives}", fill="red", font="Arial 15 bold")
        canvas.create_text(990, 15, text=f"gold: {self.gold}", fill="yellow", font="Arial 15 bold")
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
        MyApp.drawstats(self, canvas)
        
def checkcollision(x,y,w,h,x2,y2,w2,h2):
    if x + w >= x2 and y + h >= y2 and x <= x2 + w2 and y <= y2 + h2:
        return True
    else:
        return False






MyApp(width=1200, height=700)

