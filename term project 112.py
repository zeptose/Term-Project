from cmu_112_graphics import *
import enemies
import PIL
import math 
import map





class MyApp(App):

    @staticmethod
    def getCellBounds(row, col):
        cellWidth = 1200 / 15
        cellHeight = 700 / 15
        x0 = col * cellWidth
        x1 = (col+1) * cellWidth
        y0 =  row * cellHeight
        y1 = (row+1) * cellHeight
        return (x0, y0, x1, y1)

    path = [(-8, 224),(19, 224), (177, 235), (282, 283), (526, 277), (607, 217), (641, 105), (717, 57), (796, 83), (855, 222), (973, 284), (1046, 366), (1022, 458), (894, 492), (740, 504), (580, 542), (148, 541), (10, 442), (-20, 335), (-75, 305), (-100, 345)]

    def appStarted(self):
        self.rows = 15
        self.cols = 15
        self.enemies = []
        self.towers = []
        self.gold = 100
        self.lives = 100
        self.gameOver = False
        self.paused = False     
        map = "images/map.png"
        self.image1 = self.loadImage(map)
        self.image2 = self.scaleImage(self.image1, 0.65)

    
    def mousePressed(mode, event):
            x = event.x
            y = event.y
            print(x,y)
    def timerFired(self):
        #if self.gameOver: return 
        pass

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
        cx,cy = 1,1
        #for balloon in enemies:
            #canvas.create_oval(cx-r, cy+r, cx+r, cy-r, fill=color)



    def redrawAll(self, canvas):
        #canvas.create_image(self.width/2, self.height/2, image=ImageTk.PhotoImage(self.image2))
       # drawenemies(self, canvas)
        
        for row in range(self.rows):
            for col in range(self.cols):
                board = map.board(self.rows, self.cols)
                x0,y0,x1,y1 = getCellBounds(row, col)
                if board[row][col] == 0:
                    canvas.create_rectangle(x0,y0,x1,y1, fill = "blue")
                else:
                    canvas.create_rectangle(x0,y0,x1,y1, fill="yellow")


        
def checkcollision(x,y,w,h,x2,y2,w2,h2):
    if x + w >= x2 and y + h >= y2 and x <= x2 + w2 and y <= y2 + h2:
        return True
    else:
        return False






MyApp(width=1200, height=700)