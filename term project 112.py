from cmu_112_graphics import *
import enemies
import PIL
import math 
import n
import tkinter
import towers
import random
import arrow
from other import *

####All tower images are from CraftPix.net
##Background from wallpapertip.com 



def runGame():
    def board(rows, cols):
        return [[0] * cols for row in range(rows)]
    class SplashScreenMode(Mode):
        def appStarted(mode):
            mode.startimg = mode.loadImage("Images/start.jpg")
            width, height = mode.startimg.size
            mode.startimg = mode.scaleImage(mode.startimg, mode.width/width)
            mode.help = False 
            mode.helpimg = mode.loadImage("Images/cool.png")
            width, height = mode.helpimg.size
            mode.helpimg = mode.scaleImage(mode.helpimg, (mode.height - 50)/width)
        def mousePressed(mode, event):
            x = event.x
            y = event.y
            if (120 <= x <= 360) and (520 <= y <= 630):
                mode.app.setActiveMode(mode.app.normal)
            if (840 <= x <= 1080) and (520 <= y <= 630):
                mode.app.setActiveMode(mode.app.nightmare)
            if (480 <= x <= 720) and (520 <= y <= 630):
                mode.help = True 
            if mode.help == True:
                if (450<=x<=500) and (660<=y<=690):
                    mode.help = False 
                    mode.app.setActiveMode(mode.app.splashscreen)
        def redrawAll(mode, canvas):
            canvas.create_image(600,350, image=ImageTk.PhotoImage(mode.startimg))
            canvas.create_text(mode.width/2, mode.height/2, text="Balloons Tower Defense 1", font="Arial 50")
            canvas.create_rectangle(120, 520, 360, 630, fill="brown")
            canvas.create_text(240, 575, text="Normal", font="Arial 35")

            canvas.create_rectangle(840, 520, 1080, 630, fill="red")
            canvas.create_text(960, 575, text="Nightmare", font="Arial 35")

            canvas.create_rectangle(480, 520, 720, 630, fill="white")
            canvas.create_text(600, 575, text="How To Play", font="Arial 30")
            if mode.help:
                canvas.create_image(mode.width/2, mode.height/2, image=ImageTk.PhotoImage(mode.helpimg))
                canvas.create_rectangle(450, 660, 500, 690, fill="black")
                canvas.create_text(475,675, text="back", fill="white", font="Arial 15")

    class Normal(Mode):

        def appStarted(mode):
            mode.rows = 15
            mode.cols = 15
            mode.towers = []
            mode.bullets = []
            mode.bullet = []
            mode.enemies = []
            mode.gold = 1000
            mode.lives = 100
            mode.gameOver = False
            mode.paused = False

            mode.cantafford = False 
            mode.placetower = None
            mode.illegal = False 

            mode.clock = 0
        
            mode.pathpos = 0
            mode.board = board(mode.rows, mode.cols)
            mode.path = []
            mode.board1 = n.createmap(mode.board, mode.path)
            mode.boardd = mode.board1[0]

            mode.image = mode.loadImage("Images/landv2.png")
            width, height = mode.image.size
            scaleFactor = 80/width
            mode.image = mode.scaleImage(mode.image, scaleFactor)
            
            mode.image2 = mode.loadImage("Images/landv1.png")
            width1, height1 = mode.image2.size
            scaleFactor1 = 80/width1
            mode.image2 = mode.scaleImage(mode.image2, scaleFactor1)

            mode.image3 = mode.loadImage("Images/13.png")
            width, height = mode.image3.size
            mode.image3 = mode.scaleImage(mode.image3, 80/width)
            
            mode.image4 = mode.loadImage("Images/decor_9.png")
            width, height = mode.image4.size
            mode.image4 = mode.scaleImage(mode.image4, 80/width)
            
            mode.image5 = mode.loadImage("Images/11.png")
            width, height = mode.image5.size
            mode.image5 = mode.scaleImage(mode.image5, 80/width)
        
            mode.image6 = mode.loadImage("Images/20.png")
            width, height = mode.image6.size
            mode.image6 = mode.scaleImage(mode.image6, 80/width)
            mode.image7 = mode.loadImage("Images/22.png")
            width, height = mode.image7.size
            mode.image7 = mode.scaleImage(mode.image7, 20/width)
            
            mode.lix = None
            mode.liy = None 
            mode.lightning = []
            mode.bolts = []
            

        def addTower(mode, x, y):
            tower = towers.Tower((x,y))
            mode.towers.append(tower)
        
        
        def spawnv2(mode):
            while len(mode.enemies) < 5:
                i = random.randint(0, 3)
                if i == 0:
                    mode.enemies.append(enemies.Enemy(mode.path[0][0], mode.path[0][1]))
                    return 
                elif i == 1:
                    mode.enemies.append(enemies.BlueBalloon(mode.path[0][0], mode.path[0][1]))
                    return 
                elif i == 2:
                    mode.enemies.append(enemies.GreenBalloon(mode.path[0][0], mode.path[0][1]))
                    return 
                elif i == 3:
                    mode.enemies.append(enemies.YellowBalloon(mode.path[0][0], mode.path[0][0]))
                    return 


        def mousePressed(mode, event):
            if mode.gameOver: return 
            if not mode.paused:
                if mode.placetower != None:
                    if mode.legalplace(event.x, event.y, 50):
                        mode.illegal = False
                        towers.position = (event.x, event.y)
                        mode.towers.append(mode.placetower)
                        mode.gold -= mode.placetower.price
                        mode.placetower = None    
                    else:
                        mode.illegal = True 
                if mode.towers != []:
                    for tower in mode.towers:
                        if isinstance(tower, towers.Tower):
                            w,h = mode.image3.size
                            if event.x <= tower.position[0] + w/2 and event.x >= tower.position[0] - w/2:
                                if event.y <= tower.position[1] + h/2 and event.y >=  tower.position[1] - h/2:
                                    tower.selected = True 
                            else:
                                tower.selected = False 
                        elif isinstance(tower, towers.Fasttower):
                            w,h = mode.image5.size
                            if event.x <= tower.position[0] + w/2 and event.x >= tower.position[0] - w/2:
                                if event.y <= tower.position[1] + h/2 and event.y >=  tower.position[1] - h/2:
                                    tower.selected = True 
                            else:
                                tower.selected = False 
                        elif isinstance(tower, towers.bishoptower):
                            w,h = mode.image4.size
                            if event.x <= tower.position[0] + w/2 and event.x >= tower.position[0] - w/2:
                                if event.y <= tower.position[1] + h/2 and event.y >=  tower.position[1] - h/2:
                                    tower.selected = True 
                            else:
                                tower.selected = False 
                        elif isinstance(tower, towers.Wizardtower):
                            w,h = mode.image6.size
                            if event.x <= tower.position[0] + w/2 and event.x >= tower.position[0] - w/2:
                                if event.y <= tower.position[1] + h/2 and event.y >=  tower.position[1] - h/2:
                                    tower.selected = True 
                            else:
                                tower.selected = False 
                if len(mode.bolts) > 0:
                    i = 0
                    while i < len(mode.bolts):
                        bolt = mode.bolts[i]
                        w,h = mode.image7.size
                        if distance(event.x, event.y, bolt[0], bolt[1]) <= h:
                                mode.gold += 50
                                mode.bolts.pop(i)
                                mode.lightning.pop(i)
                        else:
                            i += 1

        
        def mouseMoved(mode, event):
            if mode.placetower != None:
                mode.placetower.position = (event.x, event.y)
        
        def timerFired(mode):
            mode.clock += 1
            if mode.lives <= 0:
                mode.gameOver = True 
            if mode.gameOver: return
            if not mode.paused:
                if mode.clock % 3 == 0:
                    mode.spawnv2()
                    for balloon in mode.enemies:
                        if mode.pathpos < len(mode.path):
                            if isinstance(balloon, enemies.BlueBalloon):
                                balloon.row = mode.path[balloon.pos][0]
                                balloon.col = mode.path[balloon.pos][1]
                                if balloon.pos < len(mode.path) - 1:
                                    balloon.pos += 1
                                else:
                                    mode.removeenemies()
                                    balloon.pos = 0
                        
                            elif isinstance(balloon, enemies.Enemy):
                                balloon.row = mode.path[balloon.pos][0]
                                balloon.col = mode.path[balloon.pos][1]
                                if balloon.pos < len(mode.path) - 1:
                                    balloon.pos += 1
                                else:
                                    mode.removeenemies()
                                    balloon.pos = 0
                            
                            elif isinstance(balloon, enemies.GreenBalloon):
                                balloon.row = mode.path[balloon.pos][0]
                                balloon.col = mode.path[balloon.pos][1]
                                if balloon.pos < len(mode.path) - 1:
                                    balloon.pos += 1
                                else:
                                    mode.removeenemies()
                                    balloon.pos = 0

                            elif isinstance(balloon, enemies.YellowBalloon):
                                balloon.row = mode.path[balloon.pos][0]
                                balloon.col = mode.path[balloon.pos][1]
                                if balloon.pos < len(mode.path) - 1:
                                    balloon.pos += 1
                                else:
                                    mode.removeenemies()
                                    balloon.pos = 0
                
                for tower in mode.towers:
                    if not isinstance(tower, towers.Wizardtower):
                        bul = tower.attack(mode.enemies)
                        mode.bullets.extend(bul)
                    i = 0
                    while i < len(mode.bullets):
                        bullet = mode.bullets[i]
                        x0 = bullet.position[0]
                        y0 = bullet.position[1]
                        x1 = x0 + (bullet.dx * bullet.speed)
                        y1 = y0 + (bullet.dy * bullet.speed)
                        bullet.position = (x1, y1)
                        if bullet.checkcollision(mode.enemies):
                            mode.bullets.pop(i)
                            mode.gold += 3
                        elif distance(x1, y1, tower.position[0], tower.position[1]) >= 200:
                            mode.bullets.pop(i)
                        else:                           
                            i += 1
                            
                if mode.clock % 4 == 0:
                    for tower in mode.towers:
                        if isinstance(tower, towers.Wizardtower):
                            if mode.clock % 5 == 0:
                                if tower.shoot != 0:
                                    (mode.lix, mode.liy, gold) = tower.attack(mode.enemies)
                                    tower.shoot -= 1
                                    mode.gold += gold
                                    mode.lightning.append((mode.lix, mode.liy))
                                    mode.bolts.append((mode.lix, mode.liy))
                                                            
        def removeenemies(mode):
            result = []
            for balloon in mode.enemies:
                if balloon.pos < len(mode.path) - 1:
                    continue
                else:
                    result.append(balloon)
            for balloon in result:
                mode.lives -= balloon.health   
                mode.enemies.remove(balloon)

        def legalplace(mode, x,y, towerrange):
            r,c = getCell(x,y)
            if mode.boardd[r][c] == 1 or (r,c) in mode.path:
                return False 
            for tower in mode.towers:
                if distance(x,y,tower.position[0],tower.position[1]) < tower.radius * 2:
                    return False 
    
            for balloon in mode.enemies:
                x1,y1 = getCell(balloon.row, balloon.col)
                if distance(x,y,x1,y1) < 65:
                    return False 
            return True 

                

        def keyPressed(mode, event):
            if event.key == "p":
                mode.paused = not mode.paused
            if event.key == "a":   
                if mode.gold >= towers.Tower((1,1)).price:  
                    mode.placetower = towers.Tower((1,1))
                    mode.cantafford = False 
                else:
                    mode.cantafford = True 
            elif event.key == "m":
                if mode.gold >= towers.Wizardtower((1,1)).price:  
                    mode.placetower = towers.Wizardtower((1,1))
                    mode.cantafford = False 
                else:
                    mode.cantafford = True 
            elif event.key == "b":
                if mode.gold >= towers.bishoptower((1,1)).price:  
                    mode.placetower = towers.bishoptower((1,1))
                    mode.cantafford = False 
                else:
                    mode.cantafford = True 
            elif event.key == "f":
                if mode.gold >= towers.Fasttower((1,1)).price:  
                    mode.placetower = towers.Fasttower((1,1))
                    mode.cantafford = False 
                else:
                    mode.cantafford = True 
            elif event.key == "l":
                mode.lives = 0
            elif event.key == "z":
                mode.gold = 10000



        def drawenemies(mode, canvas): 
            r = 15
            for balloon in mode.enemies:
                brow = balloon.row
                bcol = balloon.col
                x0,y0,x1,y1 = getCellBounds(brow,bcol)
                cx = (x0+x1)/2
                cy = (y0+y1)/2
                canvas.create_oval(cx-r, cy+r, cx+r, cy-r, fill=balloon.color)
        
        def drawtowerrange(mode, canvas):
            for tower in mode.towers:
                if tower.selected:
                    x,y = x,y = tower.position[0], tower.position[1]
                    r = tower.range
                    canvas.create_oval(x-r, y-r, x+r, y+r)
    
        def drawtowers(mode, canvas):
            for tower in mode.towers:
                x,y = tower.position[0], tower.position[1]
                r = tower.radius - 5 
                if isinstance(tower, towers.Fasttower):
                    canvas.create_image(x, y, image=ImageTk.PhotoImage(mode.image5))
                elif isinstance(tower, towers.bishoptower):
                    canvas.create_image(x, y, image=ImageTk.PhotoImage(mode.image4))
                elif isinstance(tower, towers.Wizardtower):
                    canvas.create_image(x, y, image=ImageTk.PhotoImage(mode.image6))
                elif isinstance(tower, towers.Tower):
                    canvas.create_image(x, y, image=ImageTk.PhotoImage(mode.image3))

        def drawstats(mode, canvas):
            canvas.create_text(1100, 15, text=f"Health: {mode.lives}", fill="red", font="Arial 15 bold")
            canvas.create_text(990, 15, text=f"gold: {mode.gold}", fill="yellow", font="Arial 15 bold")

        def drawbullets(mode, canvas):
            for bullet in mode.bullets:
                x,y = bullet.position[0], bullet.position[1]
                r = bullet.radius
                canvas.create_oval(x-r, y-r, x+r, y+r, fill="black")

        
        def drawlightning(mode, canvas):
            for bolt in mode.lightning:
                x,y = bolt[0], bolt[1]
                canvas.create_image(x,y, image=ImageTk.PhotoImage(mode.image7))
    
        def redrawAll(mode, canvas):
            for row in range(mode.rows):
                for col in range(mode.cols):
                    x0,y0,x1,y1 = getCellBounds(row, col)
                    cx,cy = (x0+x1)/2, (y0+y1)/2
                    if mode.boardd[row][col] == 0:
                        canvas.create_rectangle(x0,y0,x1,y1, fill="lightgreen")
                        canvas.create_image(cx,cy, image=ImageTk.PhotoImage(mode.image))
                    elif mode.boardd[row][col] == 1:
                        canvas.create_rectangle(x0,y0,x1,y1, fill="brown")
                        canvas.create_image(cx,cy,image=ImageTk.PhotoImage(mode.image2))

            mode.drawtowerrange(canvas)    
            mode.drawtowers(canvas)
            mode.drawstats(canvas)            
            mode.drawbullets(canvas)
            mode.drawenemies(canvas)  
            mode.drawlightning(canvas)
            if mode.placetower != None:
                x = mode.placetower.position[0]
                y = mode.placetower.position[1]
                r = 50
                canvas.create_oval(x-r, y-r, x+r, y+r, fill="grey")
            if mode.cantafford == True:
                canvas.create_text(mode.width/2, mode.height/2, text="You can't afford that right now, defeat more balloons in order to earn more gold", font="Arial 20")
            if mode.illegal == True:
                canvas.create_text(mode.width/2, mode.height/2, text="You can't place that here",font="Arial 30")
            if mode.lives <= 0:
                canvas.create_rectangle(20,20, 1000,1000, fill="yellow")
                canvas.create_text(500,300, text="GAMEOVER!", fill="black", font="Arial 50")
                canvas.create_text(500,500, text="You lost all your lives D:", fill="black", font="Arial 50")
            if mode.paused == True:
                canvas.create_oval(300,100, 800,600, w=3, fill="grey")
                canvas.create_rectangle(425,250,475,500, fill="black")
                canvas.create_rectangle(600,250,650,500, fill="black")

    class Nightmare(Normal):
        def appStarted(mode):
            super().appStarted()
            mode.gold = 600
            mode.lives = 50
    class MyModalApp(ModalApp):
        def appStarted(app):
            app.splashscreen = SplashScreenMode()
            app.normal = Normal()
            app.nightmare = Nightmare()
            app.setActiveMode(app.splashscreen)
    app = MyModalApp(width=1200, height=700)

runGame()



