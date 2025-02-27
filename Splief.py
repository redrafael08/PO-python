# importeer bibliotheken
import math
import pygame # https://www.pygame.org/docs/
from sys import exit
import random
import subprocess
import pygame.gfxdraw
import socket
import webbrowser

# https://www.w3schools.com/python/



pygame.init() # initialiseer pygame 
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN) # maak scherm
screenWidth, screenHeight = screen.get_size() # maakt van scherm formaat variablelen
screenCenter = (screenWidth / 2, screenHeight / 2) # maakt tuple van midden scherm
clock = pygame.time.Clock() # maakt klok

bg = pygame.image.load('assets\\background.png') # laad achtergrond in
bg = pygame.transform.scale(bg,(screenWidth,screenHeight)) # maakt achtergrond even groot als scherm

# laad geluiden
shootSound = pygame.mixer.Sound('assets\\laserShoot.wav')
explodesound = pygame.mixer.Sound('assets\\explosion.wav')
jumpSound = pygame.mixer.Sound('assets\\jump.wav')
player2ShootSound = pygame.mixer.Sound('assets\\laserShoot.wav')
player2JumpSound = pygame.mixer.Sound('assets\\jump.wav')
clicksound = pygame.mixer.Sound('assets\\click.wav')


serveron = 0

sound = 'ON'
music = 'ON'

# maak fonts
fontsmall = pygame.font.Font(None, 50)
font = pygame.font.Font(None, 100)

buttonsize = [700,100]

ipaddress = ''

mainbuttons = [
    lambda: Button([screenCenter[0],screenCenter[1]],buttonsize, 'Singleplayer',lambda: startgame('single')),
    lambda: Button([screenCenter[0],screenCenter[1]+150],buttonsize, 'Multiplayer',lambda: difpage(multiplayerbuttons)),
    lambda: Button([screenCenter[0],screenCenter[1]+300],buttonsize, 'Quit', lambda: exit())
]

multiplayerbuttons = [
    lambda: Button([screenCenter[0],screenCenter[1]],buttonsize, 'Create server',lambda: startgame('server')),
    lambda: Button([screenCenter[0],screenCenter[1]+150],buttonsize, 'Join server',lambda: difpage(joinbuttons)),
    lambda: Button([screenCenter[0],screenCenter[1]+300],buttonsize, 'Back', lambda: difpage(mainbuttons))
]
joinbuttons = [
    lambda: Entry([screenCenter[0],screenCenter[1]],buttonsize, 'Type IP server', ipaddress),
    lambda: Button([screenCenter[0],screenCenter[1]+150],buttonsize, 'Join',lambda: startgame('client')),
    lambda: Button([screenCenter[0],screenCenter[1]+300],buttonsize, 'Back', lambda: difpage(multiplayerbuttons))  
]

ipbuttons = [
    lambda: Button([screenCenter[0],screenCenter[1]],buttonsize, ipaddress, lambda: difpage(ipbuttons)),  
    lambda: Button([screenCenter[0],screenCenter[1]+300],buttonsize, 'Back', lambda: difpage(multiplayerbuttons))  
]

settingbuttons = [
    lambda: Button([screenCenter[0],screenCenter[1]],buttonsize, f'Sound {sound}', soundonoff),
    lambda: Button([screenCenter[0],screenCenter[1]+150],buttonsize, f'Music {music}', musiconoff),
    lambda: Button([screenCenter[0],screenCenter[1]+300],buttonsize, 'Quit', quitgame)
]



# gui functies
def Button(pos,size,text,command): # tekent button op scherm en voegt hem toe aan buttons
    buttons.append([pos[0]-size[0]/2, pos[1]-size[1]/2, pos[0]+size[0]/2, pos[1]+size[1]/2, command])
    buttonsurface = pygame.Surface(size, pygame.SRCALPHA)
    pygame.draw.rect(buttonsurface, (255,255,255,175), (0,0,size[0],size[1]))
    screen.blit(buttonsurface, (pos[0]-size[0]/2, pos[1]-size[1]/2))
    pygame.draw.rect(screen, (0,200,0), (pos[0]-size[0]/2,pos[1]-size[1]/2,size[0],size[1]), 5)
    text = font.render(f"{text}", True, (0, 200, 0))
    screen.blit(text, (pos[0]-text.get_width()/2, pos[1]-text.get_height()/2))

def Entry(pos,size,defaulttext,text): # tekent entry
    global entry
    entry = True
    buttonsurface = pygame.Surface(size, pygame.SRCALPHA)
    pygame.draw.rect(buttonsurface, (255,255,255,175), (0,0,size[0],size[1]))
    screen.blit(buttonsurface, (pos[0]-size[0]/2, pos[1]-size[1]/2))
    pygame.draw.rect(screen, (0,200,0), (pos[0]-size[0]/2,pos[1]-size[1]/2,size[0],size[1]), 5)
    if text == '':
        textdisplay = font.render(f"{defaulttext}", True, (0, 200, 0))
    else:
        textdisplay = font.render(f"{text}", True, (0, 200, 0))
    screen.blit(textdisplay, (pos[0]-textdisplay.get_width()/2, pos[1]-textdisplay.get_height()/2))

def difpage(newpage): # gaat naar andere pagina
    global currentbuttons, ipaddress, serveron
    if newpage == joinbuttons:
        ipaddress = ''
    if serveron != 0:
        serveron.kill()
        serveron = 0
        print('server closed')
    currentbuttons = newpage

def musiconoff(): # zet muziek uit
    global music
    if music == 'ON':
        music = 'OFF'
        pygame.mixer.music.stop()
    else:
        music = 'ON'
        pygame.mixer.music.play()

def soundonoff(): # zet soundeffects uit
    global sound
    if sound == 'ON':
        sound = 'OFF'
    else:
        sound = 'ON'

    

def startgame(type): # start spel op
    global running, singleplayer, ipaddress, serveron, s

    difpage(ipbuttons)

    if type == 'server':
        serveron = subprocess.Popen(["python", "server.py"])

        ipaddress = socket.gethostbyname(socket.gethostname())
        singleplayer = False
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ipaddress, 5555))
        s.setblocking(False)

    if type == 'single':
        singleplayer = True
        running = False


    if type == 'client':
        singleplayer = False
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ipaddress, 5555))
        except:
            difpage(joinbuttons)
        s.setblocking(False)

def quitgame(): # stopt spel
    global running
    running = False
    if not singleplayer:
        s.close()


def Length(vector): # bereken lengte vector
    return (vector[0]**2 + vector[1]**2 + vector[2]**2)**0.5

def Difference(vector1, vector2): # bereken verschil tussen twee vectoren
    return [vector1[0] - vector2[0], vector1[1] - vector2[1], vector1[2] - vector2[2]]

# Render functions
def LineIntersection(point1, point2): # berekent waar lijn door twee punten z = 10 snijdt 
    t = (10 - point1[2]) / (point2[2] - point1[2])
    x = point1[0] + t * (point2[0] - point1[0])
    y = point1[1] + t * (point2[1] - point1[1])
    return [x, y, 10]

def Rotate(point): # maakt van punt relatief tot oorsprong punt relatief tot player
    dx, dy, dz = point[0] - player.pos[0], point[1] - player.pos[1], point[2] - player.pos[2]
    xr = dz * sina + dx * cosa
    zr = dz * cosa - dx * sina
    yr = dy
    x = xr
    y = yr * cosb - zr * sinb
    z = zr * cosb + yr * sinb
    return [x, y, z]

def Project(point): # projecteert punt op scherm

    projX = (point[0]) / (point[2]) * screenDistance + screenCenter[0]
    projY = -(point[1]) / (point[2]) * screenDistance + screenCenter[1]
    return [projX, projY]


def AboveGrid(position, size): # kijkt of vierkant boven of onder een tile zit
    ongridpos = [[int((position[2]-size)/gridSize),int((position[0]-size)/gridSize)], [int((position[2]+size)/gridSize),int((position[0]-size)/gridSize)], [int((position[2]-size)/gridSize),int((position[0]+size)/gridSize)], [int((position[2]+size)/gridSize),int((position[0]+size)/gridSize)]]
    for pos in ongridpos:
        if 0 <= pos[0] < len(tiles) and pos[1] < len(tiles[pos[0]]):
            if tiles[pos[0]][pos[1]] == 1:
                return True
    return False

def RandomCoord(): # geeft random coordinaat
    return [random.randint(10,390), 200, random.randint(10,390)]

def RandomCoordAboveGrid(): # geeft random coordinaat dat boven een tile zit
    coord = RandomCoord()
    while not AboveGrid(coord, 0):
        coord = RandomCoord()
    return coord

def ResetWorld(): # reset map
    global lives
    global shotCooldown
    global slowFallStart
    global bots
    for z in range(20):
        for x in range(20):
            tiles[z][x] = 1
    player.pos = [200, 200, 200]
    player.vel = [0,0,0]
    player.onGround = False
    projectiles.clear()
    shotCooldown = 15
    slowFallStart = 90
    
    if singleplayer:
        bots.clear()
        for x in range(botAmount):
            bots.append(Bot(RandomCoord(), [0,0,0], False, RandomCoord()))


class Player():# maakt object speler
    def __init__(self, pos, vel, onGround):
        self.pos = pos
        self.vel = vel
        self.onGround = onGround
    
    def AddExplosionVel(self, explosionPos): 
        relativePos = [self.pos[0] - explosionPos[0], self.pos[1], self.pos[2] - explosionPos[1]]
        distance = Length(relativePos)
        direction = [relativePos[0] / distance, relativePos[1] / distance, relativePos[2] / distance]

        self.vel[0] += direction[0] / distance * 10
        self.vel[1] -= (direction[1] - 5) / distance * 10
        self.vel[2] += direction[2] / distance * 10

    def CapVel(self):
        if self.vel[0] > horizontalVelCap:
            self.vel[0] = horizontalVelCap
        if self.vel[0] < -horizontalVelCap:
            self.vel[0] = -horizontalVelCap
        if self.vel[1] > verticalVelCap:
            self.vel[1] = verticalVelCap
        if self.vel[1] < -verticalVelCap:
            self.vel[1] = -verticalVelCap
        if self.vel[2] > horizontalVelCap:
            self.vel[2] = horizontalVelCap
        if self.vel[2] < -horizontalVelCap:
            self.vel[2] = -horizontalVelCap
    
    def UpdatePos(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.pos[2] += self.vel[2]

class Bot(): # maakt object bot
    def __init__(self, pos, vel, onGround, targetPos):
        self.pos = pos
        self.vel = vel
        self.onGround = onGround
        self.targetPos = targetPos
        self.lastMinDistance = 100000000
        self.shootCooldown = 60
        self.targetPosCooldown = 300
        self.speed = 0.3
    
    def AddExplosionVel(self, explosionPos):
        relativePos = [self.pos[0] - explosionPos[0], self.pos[1], self.pos[2] - explosionPos[1]]
        distance = Length(relativePos)
        direction = [relativePos[0] / distance, relativePos[1] / distance, relativePos[2] / distance]

        self.vel[0] += direction[0] / distance * 10
        self.vel[1] -= (direction[1] - 5) / distance * 10
        self.vel[2] += direction[2] / distance * 10

    def CapVel(self): 
        if self.vel[0] > horizontalVelCap:
            self.vel[0] = horizontalVelCap
        if self.vel[0] < -horizontalVelCap:
            self.vel[0] = -horizontalVelCap
        if self.vel[1] > verticalVelCap:
            self.vel[1] = verticalVelCap
        if self.vel[1] < -verticalVelCap:
            self.vel[1] = -verticalVelCap
        if self.vel[2] > horizontalVelCap:
            self.vel[2] = horizontalVelCap
        if self.vel[2] < -horizontalVelCap:
            self.vel[2] = -horizontalVelCap
    
    def UpdatePos(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.pos[2] += self.vel[2]

class Projectile(): # maakt object projectiel
    def __init__(self, pos, vel, onGround, fromPlayer):
        self.pos = pos
        randomness = 0.5
        self.vel = [vel[0] + (random.random() - 0.5) * randomness, vel[1] + (random.random() - 0.5) * randomness, vel[2] + (random.random() - 0.5) * randomness]
        self.onGround = onGround
        self.fromPlayer = fromPlayer


currenttime = pygame.time.get_ticks() # vraagt tijd op
running = True
# opstart loop
while running:
    # kijkt of spel wordt afgesloten
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
    # stopt opstart loop na 5 secondes
    if pygame.time.get_ticks()-currenttime > 5000:
        break
    
    # text
    text = font.render(f"RMS INC. PRESENTS...", True, (255, 255, 255))
    screen.blit(text, (screenCenter[0]-text.get_width()/2,screenCenter[1]-text.get_height()/2))
    # update scherm
    pygame.display.update()


# spel loop
while True:

    pygame.mouse.set_visible(True)

    currentbuttons = mainbuttons


    # gui loop
    running = True
    while running:
        # muziek 
        if not pygame.mixer.music.get_busy() and music == 'ON':
            pygame.mixer.music.load(f'assets\\song ({random.randint(1,7)}).wav')
            pygame.mixer.music.play()
        
    
        clock.tick(60) # fps cap

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                # kijk of mouse op knop drukt
                for button in buttons:
                    if button[0] < mouse[0] < button[2] and button[1] < mouse[1] < button[3]:
                        if sound == 'ON':
                            pygame.mixer.Sound.play(clicksound)
                        button[4]()


            if event.type == pygame.KEYDOWN:
                if entry:
                    if event.key == pygame.K_BACKSPACE:
                        ipaddress = ipaddress[:-1]  

                    if (event.unicode.isnumeric() or event.unicode == '.') and len(ipaddress) <= 15:
                        ipaddress += event.unicode


        if currentbuttons == ipbuttons and singleplayer == False:
            try:
                data = s.recv(4096).decode()
                if data:
                    running = False
            except:
                pass
    

        screen.blit(bg, (0,0))
        buttons = []
        entry = False
        for widget in currentbuttons:
            widget()


        pygame.display.update()

    # -------------------------------------
    #                 Game
    # -------------------------------------

    if singleplayer == False:
        s.setblocking(True)
        s.settimeout(2)

    screenDistance = screenWidth/(2*math.tan(math.radians(125/2))) # scherm constante voor renderen
    
    # Constants
    horizontalVelCap = 10
    verticalVelCap = 10
    projectileSpeed = 20
    gridSize = 20
    gravity = 0.2

    entry = False

    botAmount = 1
   

    player = Player([200, 200, 200], [0,0,0], False)
    walkSpeed = 3
    playerAngle = [0, 0]
    shotCooldown = 15
    mouseSensitivity = 0.006
    lives = 5
    hasShot = False
    hasJumped = False
    slowFallStart = 90

    player2Lives = 5
    player2Pos = [0,25,0]

    bots = []
    
    for x in range(botAmount):
        bots.append(Bot(RandomCoord(), [0,0,0], False, RandomCoord()))
    botShotColor = (200,200,200)


    pygame.mouse.set_visible(False)

    projectiles = []
    thisExplosions = []
    projectilesPos = []

    # maakt veld van tiles
    tiles = []
    for z in range(20):
        row = []
        for x in range(20):
            row.append(1)
        tiles.append(row)




    pause = -1
    # game loop
    running = True
    while running:
        clock.tick(30) # fps cap
        screen.fill((174, 255, 255)) # achtergrond

        # muziek
        if not pygame.mixer.music.get_busy() and music == 'ON':
            pygame.mixer.music.load(f'assets\\song ({random.randint(1,7)}).wav')
            pygame.mixer.music.play()
        

        # uitwisselen data met server
        explosions = []
        if not singleplayer:
            projectilesPos.clear()
            for projectile in projectiles:
                projectilesPos.append([round(projectile.pos[0]),round(projectile.pos[1]),round(projectile.pos[2])])

            try:
                message = str([player.pos, projectilesPos, thisExplosions, lives, hasShot, hasJumped])
                message = message.encode()
                s.send(message)

                data = s.recv(4096)
                data = data.decode('utf-8')
                try:
                    data = eval(data)
                except:
                    print(data)

                player2Pos = data[0]
                player2Projectiles = data[1]
                explosions = data[2]
                if data[3] < player2Lives:
                    ResetWorld()
                    player2Lives = data[3]
                player2Shot = data[4]
                player2Jumped = data[5]
                    
                thisExplosions.clear()
                hasShot = False
            except:
                print('connection lost' )
                quitgame()
                break


        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause *= -1
                
            if pause == 1:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    for button in buttons:
                        if button[0] < mouse[0] < button[2] and button[1] < mouse[1] < button[3]:
                            if sound == 'ON':
                                pygame.mixer.Sound.play(clicksound)
                            button[4]()               





        if not pause == 1:
            mouse = pygame.mouse.get_rel()
            # Turn camera
            playerAngle[0] -= mouse[0]*mouseSensitivity
            playerAngle[1] -= mouse[1]*mouseSensitivity
        mouseClick = pygame.mouse.get_pressed()
        

        if pause == 1: 
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)
            pygame.mouse.set_pos(screenCenter)

        # controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            playerAngle[0] += math.radians(5)
        if keys[pygame.K_RIGHT]:
            playerAngle[0] -= math.radians(5)
        if keys[pygame.K_UP]:
            playerAngle[1] += math.radians(5)
        if keys[pygame.K_DOWN]:
            playerAngle[1] -= math.radians(5)

        if playerAngle[1] > math.radians(90):
            playerAngle[1] = math.radians(90)
        if playerAngle[1] < math.radians(-90):
            playerAngle[1] = math.radians(-90) 

        sina, cosa = math.sin(playerAngle[0]), math.cos(playerAngle[0])
        sinb, cosb = math.sin(playerAngle[1]), math.cos(playerAngle[1])    

        if player.onGround:
            walkSpeed = 3
        else:
            walkSpeed = 0.3

        # Move
        if keys[pygame.K_a]:
            player.vel[0] -= walkSpeed * cosa 
            player.vel[2] -= walkSpeed * sina 
        if keys[pygame.K_d]:
            player.vel[0] += walkSpeed * cosa 
            player.vel[2] += walkSpeed * sina 
        if keys[pygame.K_w]:
            player.vel[0] -= walkSpeed * sina 
            player.vel[2] += walkSpeed * cosa 
        if keys[pygame.K_s]:
            player.vel[0] += walkSpeed * sina 
            player.vel[2] -= walkSpeed * cosa 

        # Jump
        if keys[pygame.K_SPACE] and player.onGround:
            player.vel[1] += 5
            player.pos[1] = 21
            player.onGround = False
            if sound == 'ON':
                pygame.mixer.Sound.play(jumpSound)

        # Shoot projectile
        if (keys[pygame.K_q] or mouseClick[0]) and shotCooldown == 0:
            shotCooldown = 5
            projectiles.append(Projectile(player.pos.copy(), [sina * cosb * -projectileSpeed + player.vel[0], sinb * projectileSpeed + player.vel[1], cosa * cosb * projectileSpeed + player.vel[2]], False, True))
            if sound == 'ON':
                pygame.mixer.Sound.play(shootSound)
            hasShot = True
            if len(projectiles) > 75:
                projectiles.pop(0)

        # Explode projectiles
        if (keys[pygame.K_e] or mouseClick[2]):
            for projectile in projectiles:
                if projectile.onGround and projectile.fromPlayer:
                    explosionPos = [projectile.pos[0], projectile.pos[2]]
                    explosions.append(explosionPos)

                    if not singleplayer:
                        thisExplosions.append(explosionPos)

                    projectiles.remove(projectile)
    
        # Player logic
        if player.onGround == False:
            player.vel[1] -= 0.1

        if shotCooldown != 0:
            shotCooldown -= 1

        if slowFallStart != 0:
            slowFallStart -= 1
            player.vel[1] = -1

        oldPlayerY = player.pos[1]
        player.pos[0] += player.vel[0]
        player.pos[1] += player.vel[1]
        player.pos[2] += player.vel[2]

        player.vel[0] *= 0.9
        player.vel[1] *= 0.98
        player.vel[2] *= 0.9

        if player.onGround == False:
            player.vel[1] -= gravity

        else:
            player.vel[0] *= 0.4
            player.vel[2] *= 0.4
            if player.vel[0] < 0.001 and player.vel[0] > -0.001:
                player.vel[0] = 0
            if player.vel[2] < 0.001 and player.vel[0] > -0.001:
                player.vel[2] = 0

        if player.pos[1] <= 20 and AboveGrid(player.pos, 5):
            if oldPlayerY > 20:
                player.pos[1] = 20
                player.vel = [0,0,0]
                player.onGround = True
        else:
            player.onGround = False

        # -----------------
        #     Bot logic
        # -----------------

        if singleplayer:
            for bot in bots:
                if bot.onGround:
                    bot.speed = 2
                else:
                    bot.speed = 0.3

                if not bot.onGround and not AboveGrid(bot.pos, 5):
                    if AboveGrid(bot.targetPos, 0):
                        minDistance = bot.lastMinDistance
                    else:
                        minDistance = 100000000
                    if bot.lastMinDistance > (bot.pos[1] - 20) * 5:
                        for z, row in enumerate(tiles):
                            for x, column in enumerate(row):
                                if column == 1:
                                    tilePos = [(x + 0.5) * gridSize, 0, (z + 0.5) * gridSize]
                                    relativeDistance = (tilePos[0] - bot.pos[0])**2 + (tilePos[2] - bot.pos[2])**2
                                    if relativeDistance < minDistance:
                                        bot.targetPos = tilePos
                                        minDistance = relativeDistance
                        bot.lastMinDistance = minDistance
                elif bot.onGround:
                    if bot.pos[0] < bot.targetPos[0] + 8 and bot.pos[0] > bot.targetPos[0] - 8 and bot.pos[2] < bot.targetPos[2] + 8 and bot.pos[2] > bot.targetPos[2] - 8:
                        bot.targetPos = RandomCoordAboveGrid() 	    
                    elif not AboveGrid(bot.pos, 0):
                        bot.vel[1] += 5
                        bot.pos[1] = 21
                    
                    if bot.targetPosCooldown == 0:
                        bot.targetPosCooldown = 300
                        bot.targetPos = RandomCoordAboveGrid()

                if bot.pos[0] < bot.targetPos[0] -5:
                    bot.vel[0] += bot.speed
                elif bot.pos[0] > bot.targetPos[0] + 5:
                    bot.vel[0] -= bot.speed 
                if bot.pos[2] < bot.targetPos[2] -5:
                    bot.vel[2] += bot.speed
                elif bot.pos[2] > bot.targetPos[2] + 5:
                    bot.vel[2] -= bot.speed

                if bot.targetPosCooldown != 0:
                    bot.targetPosCooldown -= 1

                if slowFallStart != 0:
                    bot.vel[1] = -1

                oldBotY = bot.pos[1]
                bot.pos[0] += bot.vel[0]
                bot.pos[1] += bot.vel[1]
                bot.pos[2] += bot.vel[2]

                if not bot.onGround:
                    bot.vel[1] -= gravity
                
                if bot.onGround == False:
                    bot.vel[0] *= 0.9
                    bot.vel[1] *= 0.98
                    bot.vel[2] *= 0.9
                else:
                    bot.vel[0] *= 0.4
                    bot.vel[2] *= 0.4
                    if bot.vel[0] < 0.001 and bot.vel[0] > -0.001:
                        bot.vel[0] = 0
                    if bot.vel[2] < 0.001 and bot.vel[0] > -0.001:
                        bot.vel[2] = 0

                if bot.pos[1] <= 20 and AboveGrid(bot.pos, 5):
                    if oldBotY > 20:
                        bot.pos[1] = 20
                        bot.vel = [0,0,0]
                        bot.onGround = True
                else:
                    bot.onGround = False

                if bot.shootCooldown == 0:
                    difference = [player.pos[0] - bot.pos[0], 0, player.pos[2] - bot.pos[2]] 
                    distancePlayer = Length(difference)
                    direction = [difference[0], 0.2 * distancePlayer - 30 - bot.pos[1] * 0.4, difference[2]]
                    distanceFactor = projectileSpeed / Length(direction)
                    direction = [direction[0] * distanceFactor, direction[1] * distanceFactor, direction[2] * distanceFactor]

                    projectiles.append(Projectile(bot.pos.copy(), direction + bot.vel, False, False))
                    if random.randint(1, 5) == 1:
                        for projectile in projectiles:
                            if projectile.onGround and not projectile.fromPlayer:
                                explosionPos = [projectile.pos[0], projectile.pos[2]]
                                explosions.append(explosionPos)
                                try:
                                    tiles[int(projectile.pos[2]/gridSize)][int(projectile.pos[0]/gridSize)] = 0
                                except:
                                    pass
                                projectiles.remove(projectile)

                    bot.shootCooldown = 30
                else:
                    bot.shootCooldown -= 1

        # Calculate explosions
        for explosion in explosions:
            if AboveGrid([explosion[0], 0, explosion[1]], 0):
                tiles[int(explosion[1]/gridSize)][int(explosion[0]/gridSize)] = 0
            player.AddExplosionVel(explosion)
            if singleplayer:
                bot.AddExplosionVel(explosion)
            if sound == 'ON':
                pygame.mixer.Sound.play(explodesound)
        
        player.CapVel()
        if singleplayer:
            bot.CapVel()
        if sound == 'ON':
            if singleplayer:
                player2Distance = Length(Difference(player.pos, bot.pos))
            else:
                player2Distance = Length(Difference(player.pos, player2Pos))
                volume = 1 / (1 + player2Distance)
                player2ShootSound.set_volume(volume)
                player2JumpSound.set_volume(volume)

                if player2Shot:
                    pygame.mixer.Sound.play(player2ShootSound)
                if player2Jumped:
                    pygame.mixer.Sound.play(player2JumpSound)

        for projectile in projectiles:
            oldY = projectile.pos[1]
            if projectile.onGround == False:
                projectile.pos[0] += projectile.vel[0]
                projectile.pos[1] += projectile.vel[1]
                projectile.pos[2] += projectile.vel[2]

                if oldY > 2 and projectile.pos[1] <= 2:

                    posYNeeded = projectile.pos[1] - 2
                    projectile.pos[0] -= projectile.vel[0] / projectile.vel[1] * posYNeeded
                    projectile.pos[1] -= posYNeeded
                    projectile.pos[2] -= projectile.vel[2] / projectile.vel[1] * posYNeeded
                    if AboveGrid(projectile.pos,2) == 1:
                        projectile.onGround = True
                    else:
                        projectile.pos[0] += projectile.vel[0] / projectile.vel[1] * posYNeeded
                        projectile.pos[1] += posYNeeded
                        projectile.pos[2] += projectile.vel[2] / projectile.vel[1] * posYNeeded                       

                projectile.vel[1] -= gravity

            if projectile.pos[1] < -10:
                projectiles.remove(projectile)


        if player.pos[1] < -10:
            ResetWorld()
            lives -= 1
            if lives == 0:
                losttimer = 0



        if singleplayer:
            for bot in bots:
                if bot.pos[1] < -10:
                    bots.remove(bot)
                if len(bots) == 0:
                    botAmount += 1
                    ResetWorld()

        # ---------------------------
        #          Renderer
        # ---------------------------

        # tile renderer
        polygons = []

        cache = {}

        for z, row in enumerate(tiles):
            for x, column in enumerate(row):
                if column == 1:     
                    tile = [[x*gridSize,0,z*gridSize],
                            [x*gridSize,0,(z+1)*gridSize],
                            [(x+1)*gridSize,0,(z+1)*gridSize],
                            [(x+1)*gridSize,0,z*gridSize]]            
                    points = [Rotate(point) for point in tile]
                    polygon = []
                    for point in points:
                        tpoint = tuple(point)
                        if tpoint in cache:
                            polygon.append(cache[tpoint])
                        else:
                            if point[2] > 10:
                                ppoint = Project(point)
                                polygon.append(ppoint)
                                cache[tpoint] = ppoint
                            else:
                                point2 = points[points.index(point) - 1]
                                if point2[2] > 10:
                                    intpoint = LineIntersection(point, point2)
                                    tintpoint = tuple(intpoint)
                                    if tintpoint in cache:                     
                                        polygon.append(cache[tintpoint])
                                    else:
                                        pintpoint = Project(intpoint)
                                        polygon.append(pintpoint)
                                        cache[tuple(intpoint)] = pintpoint

                                point2 = points[(points.index(point) + 1) % 4]
                                if point2[2] > 10:
                                    intpoint = LineIntersection(point, point2)
                                    tintpoint = tuple(intpoint)
                                    if tintpoint in cache:
                                        polygon.append(cache[tintpoint])
                                    else:
                                        pintpoint = Project(intpoint)
                                        polygon.append(pintpoint)
                                        cache[tuple(intpoint)] = pintpoint

                    if len(polygon)>2:
                        maxx = max(polygon, key=lambda x: x[0])[0]
                        minx = min(polygon, key=lambda x: x[0])[0]
                        maxy = max(polygon, key=lambda x: x[1])[1]
                        miny = min(polygon, key=lambda x: x[1])[1]
                        
                        if (0 < maxx < screenWidth or 0 < maxy < screenHeight or 0 < minx < screenWidth or 0 < miny < screenHeight):
                            color = ((tile[0][0]+tile[0][2])%155+100,0,0)
                            pygame.gfxdraw.filled_polygon(screen, polygon, color)

        # sprite renderer
        sprites = []

        if singleplayer:
            for bot in bots:
                rbotPos = [Rotate(bot.pos),Rotate([bot.pos[0]-5,bot.pos[1]-20,bot.pos[2]-5]),Rotate([bot.pos[0]+5,bot.pos[1]-20,bot.pos[2]+5]),Rotate([bot.pos[0]-5,bot.pos[1]-20,bot.pos[2]+5]),Rotate([bot.pos[0]+5,bot.pos[1]-20,bot.pos[2]-5])]
                if rbotPos[0][2] > 10:
                    pbot = [Project(rbotPos[0]), Project(rbotPos[1]), Project(rbotPos[2]), Project(rbotPos[3]), Project(rbotPos[4])]
                    sprites.append([pbot,rbotPos[0][2],'enemy'])
        else:
            rPlayer2Pos = [Rotate(player2Pos),Rotate([player2Pos[0]-5,player2Pos[1]-20,player2Pos[2]-5]),Rotate([player2Pos[0]+5,player2Pos[1]-20,player2Pos[2]+5]),Rotate([player2Pos[0]-5,player2Pos[1]-20,player2Pos[2]+5]),Rotate([player2Pos[0]+5,player2Pos[1]-20,player2Pos[2]-5])]
            if rPlayer2Pos[0][2] > 10:
                pPlayer2 = [Project(rPlayer2Pos[0]), Project(rPlayer2Pos[1]), Project(rPlayer2Pos[2]), Project(rPlayer2Pos[3]), Project(rPlayer2Pos[4])]
                sprites.append([pPlayer2,rPlayer2Pos[0][2],'enemy'])

        for projectile in projectiles:
            rotatedProjectile = Rotate(projectile.pos)
            if rotatedProjectile[2] > 10:
                projectedProjectile = Project(rotatedProjectile)
                if projectile.fromPlayer:
                    sprites.append([projectedProjectile,rotatedProjectile[2],'projectile'])
                else:
                    sprites.append([projectedProjectile,rotatedProjectile[2],'projectile enemy'])
        
        if not singleplayer:
            for projectile in player2Projectiles:
                rotatedProjectile = Rotate(projectile)
                if rotatedProjectile[2] > 10:
                    projectedProjectile = Project(rotatedProjectile)
                    sprites.append([projectedProjectile,rotatedProjectile[2],'projectile enemy'])

        sprites.sort(reverse=True, key=lambda x:x[1])
        
        for sprite in sprites:
            if sprite[2] == 'projectile':
                pygame.draw.circle(screen, (0,0,0), sprite[0], 2/sprite[1]*screenDistance)
            if sprite[2] == 'projectile enemy':
                pygame.draw.circle(screen, (100,100,100), sprite[0], 2/sprite[1]*screenDistance)
            if sprite[2] == 'enemy':
                pygame.draw.polygon(screen, (0,160,0), (sprite[0][0], sprite[0][1], sprite[0][2]))
                pygame.draw.polygon(screen, (0,160,0), (sprite[0][0], sprite[0][3], sprite[0][4]))
                pygame.draw.circle(screen, (255,205,0), sprite[0][0], 8/sprite[1]*screenDistance)

        # crosshair
        pygame.draw.line(screen, (0,200,0), (screenCenter[0]-15,screenCenter[1]), (screenCenter[0]-5,screenCenter[1]),2)
        pygame.draw.line(screen, (0,200,0), (screenCenter[0],screenCenter[1]-15), (screenCenter[0],screenCenter[1]-5),2)
        pygame.draw.line(screen, (0,200,0), (screenCenter[0]+15,screenCenter[1]), (screenCenter[0]+5,screenCenter[1]),2)
        pygame.draw.line(screen, (0,200,0), (screenCenter[0],screenCenter[1]+15), (screenCenter[0],screenCenter[1]+5),2)


        if not singleplayer:
            pygame.draw.rect(screen, (0,200,0), (10,10,280,130),3)
            text = fontsmall.render(f"Player 1 lives: {lives}", True, (0, 200, 0))
            screen.blit(text, (20, 20))
            text = fontsmall.render(f"Player 2 lives: {player2Lives}", True, (0, 200, 0))
            screen.blit(text, (20, 100))
        else:
            pygame.draw.rect(screen, (0,200,0), (10,10,200,130),3)
            text = fontsmall.render(f"Lives: {lives}", True, (0, 200, 0))
            screen.blit(text, (20, 20))
            text = fontsmall.render(f"Bots left: {len(bots)}", True, (0, 200, 0))
            screen.blit(text, (20, 100))
        if lives <= 0:
            text = font.render(f"You lost", True, (0, 200, 0))
            screen.blit(text, (screenCenter[0]-text.get_width()/2, screenCenter[1]-text.get_height()/2))
            losttimer += 1
            if losttimer > 60:
                quitgame()
        if not singleplayer and player2Lives <= 0:
            text = font.render(f"You Won", True, (0, 200, 0))
            screen.blit(text, (screenCenter[0]-text.get_width()/2, screenCenter[1]-text.get_height()/2))


        if pause == 1:
            buttons = []
            for button in settingbuttons:
                button()

        pygame.display.update()

    if botAmount > 9:
        webbrowser.open('credits.html')
