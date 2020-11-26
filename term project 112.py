from cmu_112_graphics import *
import enemies
import PIL
import math 
import n
import tkinter


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
        self.enemies = [enemies.Enemy()]
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
        self.boardd = n.createmap(self.board)
        self.towers = []
        self.wave = 0
        self.currwave = waves[self.wave]
        self.clock = 0
     #   red = enemies.Enemy()
        #self.srow, self.scol = enemies.red.start(self)

    def mousePressed(self, event):
            x = event.x
            y = event.y
            print(x,y)
    
    def spawnBalloons(self):
        if sum(self.currwave) == 0: 
            if self.wave != 10:
                self.wave += 1
                self.currwave = waves[self.wave]
            else:
                self.currwave = waves[self.wave]
        else:
            balloons = [enemies.Enemy(), enemies.BlueBalloon(), enemies.GreenBalloon(), enemies.YellowBalloon()]
            for elem in range(len(self.currwave)):
                if self.currwave[elem] != 0:
                    self.enemies.append(balloons[elem])

    def timerFired(self):
        self.clock += 1
        if self.gameOver: return 
        if self.clock % 10 == 0:
            for balloon in self.enemies:
                enemies.Enemy.move(self) 


    def keyPressed(self, event):

        if event.key == "w": 
            pass
        elif event.key == "s":
            pass
        elif event.key == "a":
            pass
        elif event.key == "d":
            pass
        elif event.key == "p":
            self.paused = not self.paused
        elif event.key == "r":
            pass


    def drawenemies(self, canvas): 
        r = 15
        x0,y0,x1,y1 = getCellBounds(0, 0)
        cx = (x0+x1)/2
        cy = (y0+y1)/2
        for balloon in self.enemies:
            canvas.create_oval(cx-r, cy+r, cx+r, cy-r, fill="red")



    def redrawAll(self, canvas):
        for row in range(self.rows):
            for col in range(self.cols):
                x0,y0,x1,y1 = getCellBounds(row, col)
                cx,cy = (x0+x1)/2, (y0+y1)/2
                if self.boardd[row][col] == 0:
                    canvas.create_rectangle(x0,y0,x1,y1)
                    canvas.create_image(cx,cy, image=ImageTk.PhotoImage(self.image))
                elif self.boardd[row][col] == 1:
                    canvas.create_rectangle(x0,y0,x1,y1)
                    canvas.create_image(cx,cy,image=ImageTk.PhotoImage(self.image2))
        MyApp.drawenemies(self, canvas)       


        
def checkcollision(x,y,w,h,x2,y2,w2,h2):
    if x + w >= x2 and y + h >= y2 and x <= x2 + w2 and y <= y2 + h2:
        return True
    else:
        return False






MyApp(width=1200, height=700)