from cmu_112_graphics import *
import enemies
import PIL
import math 
import n
import tkinter
import towers
import random
import arrow
import fire
from other import *

####All tower images are from CraftPix.net
### map from: https://craftpix.net/product/tower-defense-2d-game-kit/
###main towers from: https://craftpix.net/product/archer-tower-game-assets/
### magic tower from: https://craftpix.net/product/magic-tower-game-assets/
### fire from: https://www.storyblocks.com/video/search/blue+flames
##Background from wallpapertip.com, https://www.wallpapertip.com/wpic/miTixR_abstract-art-cool-backgrounds/ 
##Animations, graphics from cmu 15112 graphics :https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
##modal app from https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html


def runGame():
    def board(rows, cols):
        return [[0] * cols for row in range(rows)]
    class SplashScreenMode(Mode):
        def appStarted(mode):
            mode.startimg = mode.loadImage("Images/start.jpg")
            width, height = mode.startimg.size
            mode.startimg = mode.scaleImage(mode.startimg, mode.width/width)
            mode.help = False 
            mode.helpimg = mode.loadImage("Images/e.png")
            width, height = mode.helpimg.size
            mode.helpimg = mode.scaleImage(mode.helpimg, (mode.height - 10)/height)
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
            mode.placefire = None 

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
            
            mode.image5 = mode.loadImage("Images/11.png")
            width, height = mode.image5.size
            mode.image5 = mode.scaleImage(mode.image5, 80/width)
        
            mode.image6 = mode.loadImage("Images/20.png")
            width, height = mode.image6.size
            mode.image6 = mode.scaleImage(mode.image6, 80/width)
            mode.image7 = mode.loadImage("Images/22.png")
            width, height = mode.image7.size
            mode.image7 = mode.scaleImage(mode.image7, 20/width)

            mode.image8 = mode.loadImage("Images/freeze1.png")
            width, height = mode.image8.size
            mode.image8 = mode.scaleImage(mode.image8, 80/width)

            mode.image9 = mode.loadImage("Images/flame1.png")
            width, height = mode.image9.size
            mode.image9 = mode.scaleImage(mode.image9, 25/width)
            
            mode.lix = None
            mode.liy = None 
            mode.lightning = []
            mode.bolts = []
            mode.fire = []
         #   mode.timerDelay = 200
            

        def addTower(mode, x, y):
            tower = towers.Tower((x,y))
            mode.towers.append(tower)
        
        def addFire(mode, x, y):
            flame = fire.Fire((x,y))
            mode.fire.append(flame)
        
        
        def spawnv2(mode):
            while len(mode.enemies) < 6:
                i = random.randint(0, 4)
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
                elif i == 4:
                    mode.enemies.append(enemies.MetalBalloon(mode.path[0][0], mode.path[0][1]))
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
                if mode.placefire != None:
                    if mode.legalplace2(event.x, event.y, 50):
                        mode.illegal = False
                        fire.position = (event.x, event.y)
                        mode.fire.append(mode.placefire)
                        mode.gold -= mode.placefire.price
                        mode.placefire = None 
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
                        elif isinstance(tower, towers.Wizardtower):
                            w,h = mode.image6.size
                            if event.x <= tower.position[0] + w/2 and event.x >= tower.position[0] - w/2:
                                if event.y <= tower.position[1] + h/2 and event.y >=  tower.position[1] - h/2:
                                    tower.selected = True 
                            else:
                                tower.selected = False 
                        elif isinstance(tower, towers.Freezetower):
                            w,h = mode.image8.size
                            if event.x <= tower.position[0] + w/2 and event.x >= tower.position[0] - w/2:
                                if event.y <= tower.position[1] + h/2 and event.y >=  tower.position[1] - h/2:
                                    tower.selected = True 
                            else:
                                tower.selected = False 
                    if mode.fire != []:
                        for flame in mode.fire:
                            w,h = mode.image9.size
                            if event.x <= flame.position[0] + w/2 and event.x >= flame.position[0] - w/2:
                                if event.y <= flame.position[1] + h/2 and event.y >=  flame.position[1] - h/2:
                                    flame.selected = True 
                            else:
                                flame.selected = False 
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
            elif mode.placefire != None:
                mode.placefire.position = (event.x, event.y)
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
                                if balloon.freeze == False:
                                    balloon.row = mode.path[balloon.pos][0]
                                    balloon.col = mode.path[balloon.pos][1]
                                    if balloon.pos < len(mode.path) - 1:
                                        balloon.pos += 1
                                    else:
                                        mode.removeenemies()
                                        balloon.pos = 0
                        
                            elif isinstance(balloon, enemies.Enemy):
                                if balloon.freeze == False:
                                    balloon.row = mode.path[balloon.pos][0]
                                    balloon.col = mode.path[balloon.pos][1]
                                    if balloon.pos < len(mode.path) - 1:
                                        balloon.pos += 1
                                    else:
                                        mode.removeenemies()
                                        balloon.pos = 0
                            elif isinstance(balloon, enemies.MetalBalloon):
                                if balloon.freeze == False:
                                    balloon.row = mode.path[balloon.pos][0]
                                    balloon.col = mode.path[balloon.pos][1]
                                    if balloon.pos < len(mode.path) - 1:
                                        balloon.pos += 1
                                    else:
                                        mode.removeenemies()
                                        balloon.pos = 0
                            elif isinstance(balloon, enemies.GreenBalloon):
                                if balloon.freeze == False:
                                    balloon.row = mode.path[balloon.pos][0]
                                    balloon.col = mode.path[balloon.pos][1]
                                    if balloon.pos < len(mode.path) - 1:
                                        balloon.pos += 1
                                    else:
                                        mode.removeenemies()
                                        balloon.pos = 0

                            elif isinstance(balloon, enemies.YellowBalloon):
                                if balloon.freeze == False:
                                    balloon.row = mode.path[balloon.pos][0]
                                    balloon.col = mode.path[balloon.pos][1]
                                    if balloon.pos < len(mode.path) - 1:
                                        balloon.pos += 1
                                    else:
                                        mode.removeenemies()
                                        balloon.pos = 0
                
                for tower in mode.towers:
                    if not isinstance(tower, towers.Wizardtower):
                        if isinstance(tower, towers.Fasttower):
                            if tower.shoot > 0:
                                bul = tower.attack(mode.enemies)
                                mode.bullets.extend(bul)
                                tower.shoot -= 1
                            elif tower.shoot <= 0:
                                if mode.clock % 10 == 0:
                                        tower.shoot = 15
                        elif isinstance(tower, towers.Freezetower):
                            for balloon in mode.enemies:
                                i = random.randint(0, len(mode.enemies) - 1)
                                bl = mode.enemies[i]
                                br, bc = bl.row, bl.col
                                bx, by, bx1, by1 = getCellBounds(br, bc)
                                bcx, bcy = (bx+bx1)/2, (by+by1)/2
                                tx = tower.position[0]
                                ty = tower.position[1]
                                if distance(bcx, bcy, tx, ty) < tower.range: 
                                    if mode.clock % 10 == 0:
                                        mode.enemies[i].freeze = True 
                                    elif mode.clock % 15 == 0:
                                        mode.enemies[i].freeze = False 


                        elif isinstance(tower, towers.Tower):
                            if tower.shoot > 0:
                                bul = tower.attack(mode.enemies)
                                mode.bullets.extend(bul)
                                tower.shoot -= 2
                            elif tower.shoot <= 0:
                                if mode.clock % 20 == 0:
                                        tower.shoot = 15
                    if mode.clock % 4 == 0:
                        if isinstance(tower, towers.Wizardtower):
                            if mode.clock % 5 == 0:
                                    (mode.lix, mode.liy, gold) = tower.attack(mode.enemies)
                                    tower.shoot -= 1
                                    mode.gold += gold
                                    mode.lightning.append((mode.lix, mode.liy))
                                    mode.bolts.append((mode.lix, mode.liy))

                for flame in mode.fire:
                    if mode.clock % 10 == 0:
                        for balloon in mode.enemies:
                            br, bc = balloon.row, balloon.col
                            bx, by, bx1, by1 = getCellBounds(br, bc)
                            bcx, bcy = (bx+bx1)/2, (by+by1)/2
                            fx = flame.position[0]
                            fy = flame.position[1]
                            if distance(bcx, bcy, fx, fy) < flame.radius + 15:
                                if not isinstance(balloon, enemies.MetalBalloon):
                                    newbloon = balloon.weakerballoon()
                                    mode.enemies.remove(balloon) 
                                    if newbloon.health > 0:
                                        mode.enemies.append(newbloon)
                                else:
                                    newbloon = enemies.YellowBalloon(balloon.row, balloon.col)
                                    mode.enemies.remove(balloon) 
                                    mode.enemies.append(newbloon)




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

        def legalplace2(mode, x,y, towerrange):
            r,c = getCell(x,y)
            if mode.boardd[r][c] == 0 or (r,c) not in mode.path:
                return False 
            for fire in mode.fire:
                if distance(x,y,fire.position[0],fire.position[1]) < fire.radius * 2:
                    return False 
            return True
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
            elif event.key == "f":
                if mode.gold >= towers.Fasttower((1,1)).price:  
                    mode.placetower = towers.Fasttower((1,1))
                    mode.cantafford = False 
                else:
                    mode.cantafford = True 
            elif event.key == "i":
                if mode.gold >= towers.Freezetower((1,1)).price:  
                    mode.placetower = towers.Freezetower((1,1))
                    mode.cantafford = False 
                else:
                    mode.cantafford = True 
            elif event.key == "h":
                if mode.gold >= fire.Fire((1,1)).price:  
                    mode.placefire = fire.Fire((1,1))
                    mode.cantafford = False 
                else:
                    mode.cantafford = True     
            ###short cuts 
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
                if isinstance(balloon, enemies.MetalBalloon):
                    brow = balloon.row
                    bcol = balloon.col
                    x0,y0,x1,y1 = getCellBounds(brow,bcol)
                    cx = (x0+x1)/2
                    cy = (y0+y1)/2
                    if balloon.freeze == False:
                        canvas.create_oval(cx-r, cy+r, cx+r, cy-r, fill=balloon.color)
                        canvas.create_text(cx, cy, text=f"{balloon.health}", fill="white")
                    else:
                        canvas.create_oval(cx-r, cy+r, cx+r, cy-r, fill="white")
                        canvas.create_text(cx, cy, text=f"{balloon.health}", fill="black")
                else:
                    if balloon.freeze == False:
                        canvas.create_oval(cx-r, cy+r, cx+r, cy-r, fill=balloon.color)
                    else:
                        canvas.create_oval(cx-r, cy+r, cx+r, cy-r, fill="white")
        
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
                elif isinstance(tower, towers.Wizardtower):
                    canvas.create_image(x, y, image=ImageTk.PhotoImage(mode.image6))
                elif isinstance(tower, towers.Freezetower):
                    canvas.create_image(x, y, image=ImageTk.PhotoImage(mode.image8))
                elif isinstance(tower, towers.Tower):
                    canvas.create_image(x, y, image=ImageTk.PhotoImage(mode.image3))
        def drawfire(mode, canvas):
            for flame in mode.fire:
                x,y = flame.position[0], flame.position[1]
                r = flame.radius - 5 
                canvas.create_image(x, y, image=ImageTk.PhotoImage(mode.image9))

        def drawstats(mode, canvas):
            canvas.create_text(1100, 15, text=f"Health: {mode.lives}", fill="red", font="Arial 15 bold")
            canvas.create_text(990, 15, text=f"gold: {mode.gold}", fill="yellow", font="Arial 15 bold")

        def drawbullets(mode, canvas):
            for bullet in mode.bullets:
                x,y = bullet.position[0], bullet.position[1]
                r = bullet.radius
                canvas.create_oval(x-r, y-r, x+r, y+r, fill="grey")

        
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
            mode.drawfire(canvas)
            mode.drawenemies(canvas)  
            mode.drawlightning(canvas)
 
            if mode.placetower != None:
                x = mode.placetower.position[0]
                y = mode.placetower.position[1]
                r = 50
                canvas.create_oval(x-r, y-r, x+r, y+r, fill="grey")
            if mode.placefire != None:
                x = mode.placefire.position[0]
                y = mode.placefire.position[1]
                r = 50
                canvas.create_oval(x-r, y-r, x+r, y+r, fill="red")
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



