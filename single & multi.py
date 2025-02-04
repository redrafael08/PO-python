import math
import pygame
from sys import exit
import random
import subprocess
import pygame.gfxdraw
import socket

# -------------------------------------
#             Home screen
# -------------------------------------

pygame.init()
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
screenWidth, screenHeight = screen.get_size()
screenCenter = (screenWidth / 2, screenHeight / 2)
singleplayer = True

bg = pygame.image.load('background.png')

font = pygame.font.Font(None, 100)

def Button(pos,size,text,command):
    buttons.append([pos[0]-size[0]/2, pos[1]-size[1]/2, pos[0]+size[0]/2, pos[1]+size[1]/2, command])
    buttonsurface = pygame.Surface(size, pygame.SRCALPHA)
    pygame.draw.rect(buttonsurface, (255,255,255,175), (0,0,size[0],size[1]))
    screen.blit(buttonsurface, (pos[0]-size[0]/2, pos[1]-size[1]/2))
    pygame.draw.rect(screen, (0,200,0), (pos[0]-size[0]/2,pos[1]-size[1]/2,size[0],size[1]), 5)
    text = font.render(f"{text}", True, (0, 200, 0))
    screen.blit(text, (pos[0]-text.get_width()/2, pos[1]-text.get_height()/2))

def difpage(newpage):
    global currentButtons
    currentButtons = newpage

def server():
    global running
    subprocess.Popen(["python", "server.py"])
    running = False

mainbuttons = [
    lambda: Button([screenCenter[0],screenCenter[1]],[500,100], 'Singleplayer',lambda: subprocess.Popen(["python", "Splief bot.py"])),
    lambda: Button([screenCenter[0],screenCenter[1]+150],[500,100], 'Multiplayer',lambda: difpage(multiplayerbuttons)),
    lambda: Button([screenCenter[0],screenCenter[1]+300],[500,100], 'Quit', lambda: exit())
]

multiplayerbuttons = [
    lambda: Button([screenCenter[0],screenCenter[1]],[500,100], 'Create server',server),
    lambda: Button([screenCenter[0],screenCenter[1]+150],[500,100], 'Join server',lambda: difpage(joinbuttons)),
    lambda: Button([screenCenter[0],screenCenter[1]+300],[500,100], 'Back', lambda: difpage(mainbuttons))
]
joinbuttons = [
    lambda: Button([screenCenter[0],screenCenter[1]],[500,100], 'E',lambda: print('e')),
    lambda: Button([screenCenter[0],screenCenter[1]+150],[500,100], 'Join server',lambda: print('e')),
    lambda: Button([screenCenter[0],screenCenter[1]+300],[500,100], 'Back', lambda: difpage(mainbuttons))  
]

currentButtons = mainbuttons

clock = pygame.time.Clock()
running = True
while running:
    clock.tick(60)
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()

            for button in buttons:
                if button[0] < mouse[0] < button[2] and button[1] < mouse[1] < button[3]:
                    button[4]()

   

    screen.blit(bg, (0,0))
    buttons = []
    for button in currentButtons:
        button()


    pygame.display.update()


# -------------------------------------
#                 Game
# -------------------------------------

# Connect client to server
if not singleplayer:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = socket.gethostbyname(socket.gethostname()) 
    print(ip)
    s.connect((input('give ip addres of the server: '), 5555))

pygame.init()

# Sounds
shootSound = pygame.mixer.Sound('laserShoot.wav')
explodesound = pygame.mixer.Sound('explosion.wav')
jumpSound = pygame.mixer.Sound('jump.wav')
player2ShootSound = pygame.mixer.Sound('laserShoot.wav')
player2JumpSound = pygame.mixer.Sound('jump.wav')

# Screen values
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
screenDistance = 400
screenWidth, screenHeight = screen.get_size()
screenCenter = (screenWidth / 2, screenHeight / 2)

# Constants
horizontalVelCap = 10
verticalVelCap = 10
projectileSpeed = 20
gridSize = 20
gravity = 0.2

def Length(vector):
    return (vector[0]**2 + vector[1]**2 + vector[2]**2)**0.5

def Difference(vector1, vector2):
    return [vector1[0] - vector2[0], vector1[1] - vector2[1], vector1[2] - vector2[2]]

class Player():
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

class Projectile():
    def __init__(self, pos, vel, onGround, fromPlayer):
        self.pos = pos
        randomness = 0.5
        self.vel = [vel[0] + (random.random() - 0.5) * randomness, vel[1] + (random.random() - 0.5) * randomness, vel[2] + (random.random() - 0.5) * randomness]
        self.onGround = onGround
        self.fromPlayer = fromPlayer

player = Player([200, 25, 200], [0,0,0], False)
walkSpeed = 3
playerAngle = [0, 0]
shotCooldown = 0
mouseSensitivity = 0.006
lives = 5
hasShot = False
hasJumped = False

player2Lives = 5
player2Pos = [0,25,0]

bot = Player([200, 25, 200], [0,0,0], False)
botcooldown = 60
botSpeed = 3
botShotColor = (200,200,200)
lastMinDistance = 1000000000
targetPos = [200, 25, 200]

tiles = []
clock = pygame.time.Clock()
font = pygame.font.Font(None, 50)
pygame.mouse.set_visible(False)

projectiles = []
thisExplosions = []
projectilesPos = []

veldown = 0

# Create tiles
for z in range(20):
    row = []
    for x in range(20):
        row.append(1)
    tiles.append(row)


# Render functions

def LineIntersection(point1, point2):
    t = (10 - point1[2]) / (point2[2] - point1[2])
    x = point1[0] + t * (point2[0] - point1[0])
    y = point1[1] + t * (point2[1] - point1[1])
    return [x, y, 10]

def Rotate(point):
    dx, dy, dz = point[0] - player.pos[0], point[1] - player.pos[1], point[2] - player.pos[2]
    xr = dz * sina + dx * cosa
    zr = dz * cosa - dx * sina
    yr = dy
    x = xr
    y = yr * cosb - zr * sinb
    z = zr * cosb + yr * sinb
    return [x, y, z]

def Project(point):

    projX = (point[0]) / (point[2]) * screenDistance + screenCenter[0]
    projY = -(point[1]) / (point[2]) * screenDistance + screenCenter[1]
    return [projX, projY]


def AboveGrid(position, size):
    if position[0] - size <= gridSize*20 and position[2] - size <= gridSize*20 and position[0] + size >= 0 and position[2] + size >= 0:
        if (-size < position[0] < 20*gridSize+size and -size < position[2] < 20*gridSize+size) and (tiles[int((position[2]-size)/gridSize)][int((position[0]-size)/gridSize)] or tiles[int((position[2]-size)/gridSize)][int((position[0]+size)/gridSize)] == 1 or tiles[int((position[2]+size)/gridSize)][int((position[0]-size)/gridSize)] == 1 or tiles[int((position[2]+size)/gridSize)][int((position[0]+size)/gridSize)] == 1):
            return True
    return False

def ResetWorld():
    global lives
    for z in range(20):
        for x in range(20):
            tiles[z][x] = 1
    player.pos = [200, 25, 200]
    player.vel = [0,0,0]
    player.onGround = False
    projectiles.clear()


while True:
    clock.tick(30)
    screen.fill((174, 255, 255))
    explosions = []
    
    # Communicat with server
    if not singleplayer:
        projectilesPos.clear()
        for projectile in projectiles:
            projectilesPos.append([round(projectile.pos[0]),round(projectile.pos[1]),round(projectile.pos[2])])

        message = str([player.pos, projectilesPos, thisExplosions, lives, hasShot, hasJumped])
        message = message.encode()
        s.sendall(message)

        data = s.recv(4096)
        data = data.decode('utf-8')
        data = eval(data)
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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    # Get inputs
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_rel()
    mouseClick = pygame.mouse.get_pressed()
    
    # Turn camera
    playerAngle[0] -= mouse[0]*mouseSensitivity
    playerAngle[1] -= mouse[1]*mouseSensitivity
    pygame.mouse.set_pos(screenCenter)

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
        player.vel[0] += walkSpeed * math.cos(playerAngle[0] + math.radians(90)) 
        player.vel[2] += walkSpeed * math.sin(playerAngle[0] + math.radians(90)) 
    if keys[pygame.K_s]:
        player.vel[0] -= walkSpeed * math.cos(playerAngle[0] + math.radians(90)) 
        player.vel[2] -= walkSpeed * math.sin(playerAngle[0] + math.radians(90)) 

    # Jump
    if keys[pygame.K_SPACE] and player.onGround:
        player.vel[1] += 5
        player.pos[1] = 21
        player.onGround = False
        pygame.mixer.Sound.play(jumpSound)

    # Shoot projectile
    if (keys[pygame.K_q] or mouseClick[0]) and shotCooldown == 0:
        shotCooldown = 5
        projectiles.append(Projectile(player.pos.copy(), [sina * cosb * -projectileSpeed + player.vel[0], sinb * projectileSpeed + player.vel[1], cosa * cosb * projectileSpeed + player.vel[2]], False, True))
        pygame.mixer.Sound.play(shootSound)
        hasShot = True

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
            player.vel[1] = 0
            player.onGround = True
    else:
        player.onGround = False

    # Bot logic
    if singleplayer:
        if bot.onGround:
            botSpeed = 1
        else:
            botSpeed = 0.1

        if not bot.onGround and not AboveGrid(bot.pos, 5):
            if AboveGrid(targetPos, 0):
                minDistance = lastMinDistance
            else:
                minDistance = 100000000
            for z, row in enumerate(tiles):
                for x, column in enumerate(row):
                    if column == 1:
                        tilePos = [(x + 0.5) * gridSize, 0, (z + 0.5) * gridSize]
                        relativeDistance = (tilePos[0] - bot.pos[0])**2 + (tilePos[2] - bot.pos[2])**2
                        if relativeDistance < minDistance:
                            targetPos = tilePos
                            minDistance = relativeDistance
            lastMinDistance = minDistance

        if bot.pos[0] < targetPos[0] -5:
            bot.vel[0] += botSpeed
        elif bot.pos[0] > targetPos[0] + 5:
            bot.vel[0] -= botSpeed 
        if bot.pos[2] < targetPos[2] -5:
            bot.vel[2] += botSpeed
        elif bot.pos[2] > targetPos[2] + 5:
            bot.vel[2] -= botSpeed

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
                bot.vel[1] = 0
                bot.onGround = True
        else:
            bot.onGround = False

        if botcooldown == 0:
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

                        tiles[int(projectile.pos[2]/gridSize)][int(projectile.pos[0]/gridSize)] = 0
                        player2Projectiles.remove(projectile)

            botcooldown = 30
        else:
            botcooldown -= 1

    # Calculate explosions
    for explosion in explosions:
        if AboveGrid([explosion[0], 0, explosion[1]], 0):
            tiles[int(explosion[1]/gridSize)][int(explosion[0]/gridSize)] = 0
        player.AddExplosionVel(explosion)
        if singleplayer:
            bot.AddExplosionVel(explosion)
        pygame.mixer.Sound.play(explodesound)
    
    player.CapVel()
    if singleplayer:
        bot.CapVel()

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
            projectile.vel[1] -= gravity

        if oldY > 2 and projectile.pos[1] <= 2 and AboveGrid(projectile.pos,1) == 1:
            projectile.vel = [0,0,0]
            projectile.pos[1] = 2
            projectile.onGround = True

        if projectile.pos[1] < -10:
            projectiles.remove(projectile)

        if (projectile.pos[1] < 2 and player.pos[1] >= 20) or (projectile.pos[1] >= 2 and player.pos[1] < 20):
            rotatedProjectile = Rotate(projectile.pos)
            if rotatedProjectile[2] > 10:
                projectedProjectile = Project(rotatedProjectile)
                pygame.draw.circle(screen, (0,0,0), projectedProjectile, 2/rotatedProjectile[2]*screenDistance)

    # ---------------------------
    #          Renderer
    # ---------------------------

    polygons = []

    cache = {}

    a = 0

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
                            a += 1
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
                                    a +=1

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
                                    a +=1

                if len(polygon)>2:
                    maxx = max(polygon, key=lambda x: x[0])[0]
                    minx = min(polygon, key=lambda x: x[0])[0]
                    maxy = max(polygon, key=lambda x: x[1])[1]
                    miny = min(polygon, key=lambda x: x[1])[1]
                    
                    if (0 < maxx < screenWidth or 0 < maxy < screenHeight or 0 < minx < screenWidth or 0 < miny < screenHeight):
                        color = ((tile[0][0]+tile[0][2])%155+100,0,0)
                        pygame.gfxdraw.filled_polygon(screen, polygon, color)
    if singleplayer:
        rbotPos = [Rotate(bot.pos),Rotate([bot.pos[0]-5,bot.pos[1]-20,bot.pos[2]-5]),Rotate([bot.pos[0]+5,bot.pos[1]-20,bot.pos[2]+5]),Rotate([bot.pos[0]-5,bot.pos[1]-20,bot.pos[2]+5]),Rotate([bot.pos[0]+5,bot.pos[1]-20,bot.pos[2]-5])]
    else:
        rbotPos = [Rotate(player2Pos),Rotate([player2Pos[0]-5,player2Pos[1]-20,player2Pos[2]-5]),Rotate([player2Pos[0]+5,player2Pos[1]-20,player2Pos[2]+5]),Rotate([player2Pos[0]-5,player2Pos[1]-20,player2Pos[2]+5]),Rotate([player2Pos[0]+5,player2Pos[1]-20,player2Pos[2]-5])]
    if rbotPos[0][2] > 10:

        pbot = [Project(rbotPos[0]), Project(rbotPos[1]), Project(rbotPos[2]), Project(rbotPos[3]), Project(rbotPos[4])]
        
        pygame.draw.polygon(screen, (0,160,0), (pbot[0], pbot[1], pbot[2]))
        pygame.draw.polygon(screen, (0,160,0), (pbot[0], pbot[3], pbot[4]))
        pygame.draw.circle(screen, (255,205,0), pbot[0], 8/rbotPos[0][2]*screenDistance)

    for projectile in projectilesPos:
        if (projectile.vel >= 2 and player.pos[1] >= 20) or (projectile.vel < 2 and player.pos[1] < 20):

            rotatedProjectile = Rotate(projectile)
            if rotatedProjectile[2] > 10:
                projectedProjectile = Project(rotatedProjectile)
                if projectile.fromPlayer:
                    pygame.draw.circle(screen, (0,0,0), projectedProjectile, 2/rotatedProjectile[2]*screenDistance)
                else:
                    pygame.draw.circle(screen, (255,0,0), projectedProjectile, 2/rotatedProjectile[2]*screenDistance)
    
    for projectile in player2Projectiles:
        if (projectile.vel >= 2 and player.pos[1] >= 20) or (projectile.vel < 2 and player.pos[1] < 20):

            rotatedProjectile = Rotate(projectile)
            if rotatedProjectile[2] > 10:
                projectedProjectile = Project(rotatedProjectile)
                pygame.draw.circle(screen, (255,0,0), projectedProjectile, 2/rotatedProjectile[2]*screenDistance)

    if player.pos[1] < -10:
        ResetWorld()
        lives -= 1

    pygame.draw.line(screen, (0,200,0), (screenCenter[0]-15,screenCenter[1]), (screenCenter[0]-5,screenCenter[1]),2)
    pygame.draw.line(screen, (0,200,0), (screenCenter[0],screenCenter[1]-15), (screenCenter[0],screenCenter[1]-5),2)
    pygame.draw.line(screen, (0,200,0), (screenCenter[0]+15,screenCenter[1]), (screenCenter[0]+5,screenCenter[1]),2)
    pygame.draw.line(screen, (0,200,0), (screenCenter[0],screenCenter[1]+15), (screenCenter[0],screenCenter[1]+5),2)






    '''
    text = font.render(f"{round(clock.get_fps())}", True, (0, 0, 0))
    screen.blit(text, (100, 100))
    text = font.render(f"{round(player.pos[0]), round(player.pos[1]), round(player.pos[2])}", True, (0, 0, 0))
    screen.blit(text, (100, 200))
    text = font.render(f"{round(player.vel[0]), round(player.vel[1]), round(player.vel[2])}", True, (0, 0, 0))
    screen.blit(text, (100, 300))
    text = font.render(f"{playerAngle}", True, (0, 0, 0))
    screen.blit(text, (100, 400))
    text = font.render(f"{len(projectiles)}", True, (0, 0, 0))
    screen.blit(text, (100, 500))
    '''
    pygame.display.update()
