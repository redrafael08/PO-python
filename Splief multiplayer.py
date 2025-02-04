import math
import pygame
from sys import exit
import random
import pygame.gfxdraw
import socket



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = socket.gethostbyname(socket.gethostname()) 
print(ip)
s.connect((input('give ip addres of the server: '), 5555))

pygame.init()

shootsound = pygame.mixer.Sound('laserShoot.wav')
explodesound = pygame.mixer.Sound('explosion.wav')
jumpsound = pygame.mixer.Sound('jump.wav')
enemyshootsound = pygame.mixer.Sound('laserShoot.wav')
enemyjumpsound = pygame.mixer.Sound('jump.wav')

screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
screenDistance = 400
screenWidth, screenHeight = screen.get_size()
screenCenter = (screenWidth / 2, screenHeight / 2)
horizontalVelCap = 10
verticalVelCap = 10

def length(vector):
    return (vector[0]**2 + vector[1]**2 + vector[2]**2)**0.5

def difference(vector1, vector2):
    return [vector1[0] - vector2[0], vector1[1] - vector2[1], vector1[2] - vector2[2]]

class Player():
    def __init__(self, pos, vel, onGround):
        self.pos = pos
        self.vel = vel
        self.onGround = onGround
    
    def AddExplosionVel(self, explosionPos):
        relativePos = [self.pos[0] - explosionPos[0], self.pos[1] - explosionPos[1], self.pos[2] - explosionPos[2]]
        distance = length(relativePos)
        direction = [difference[0] / distance, difference[1] / distance, difference[2] / distance]

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

player = Player([200, 25, 200], [0,0,0], False)
player2Pos = [0,25,0]
walkSpeed = 3
playerAngle = [0, 0]
shotCooldown = 0
mouseSensitivity = 0.006
lives = 5
enemyLives = 5
hasShot = False
hasJumped = False

gridSize = 20
tiles = []
clock = pygame.time.Clock()
font = pygame.font.Font(None, 50)
pygame.mouse.set_visible(False)

projectiles = []
thisExplosions = []
projectilesPos = []


veldown = 0
gravityacc = 0.2



for z in range(20):
    row = []
    for x in range(20):
        row.append(1)
    tiles.append(row)




def line_intersection(point1, point2):
    t = (10 - point1[2]) / (point2[2] - point1[2])
    x = point1[0] + t * (point2[0] - point1[0])
    y = point1[1] + t * (point2[1] - point1[1])
    return [x, y, 10]


def rotate(point):
    dx, dy, dz = point[0] - player.pos[0], point[1] - player.pos[1], point[2] - player.pos[2]
    xr = dz * sina + dx * cosa
    zr = dz * cosa - dx * sina
    yr = dy
    x = xr
    y = yr * cosb - zr * sinb
    z = zr * cosb + yr * sinb
    return [x, y, z]


def project(point):

    projX = (point[0]) / (point[2]) * screenDistance + screenCenter[0]
    projY = -(point[1]) / (point[2]) * screenDistance + screenCenter[1]
    return [projX, projY]

def abovegrid(position, size):
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
    projectilesPos.clear()
    for projectile in projectiles:
        projectilesPos.append([round(projectile[0][0]),round(projectile[0][1]),round(projectile[0][2])])

    message = str([player.pos, projectilesPos, thisExplosions, lives, hasShot, hasJumped])
    message = message.encode()
    s.sendall(message)

    data = s.recv(4096)
    data = data.decode('utf-8')
    data = eval(data)
    player2Pos = data[0]
    enemyProjectiles = data[1]
    explosions = data[2]
    if data[3] < enemyLives:
        ResetWorld()
        enemyLives = data[3]
    enemyShot = data[4]
    enemyJumped = data[5]
        
    thisExplosions.clear()
    hasShot = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    currentframe = clock.get_time()
    
    keys = pygame.key.get_pressed()

    mouse = pygame.mouse.get_rel()
    mouseclick = pygame.mouse.get_pressed()
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

    if keys[pygame.K_SPACE] and player.onGround:
        player.vel[1] += 5
        player.pos[1] = 21
        player.onGround = False
        pygame.mixer.Sound.play(jumpsound)

    if (keys[pygame.K_q] or mouseclick[0]) and shotCooldown == 0:
        shotCooldown = 5
        randomness = 0.5
        xOffset = (random.random() - 0.5) * randomness
        yOffset = (random.random() - 0.5) * randomness
        zOffset = (random.random() - 0.5) * randomness

        projectiles.append([player.pos.copy(), [sina * cosb * -20 + xOffset + player.vel[0], sinb * 20 + yOffset + player.vel[1], cosa * cosb * 20 + zOffset + player.vel[2]], False])
        pygame.mixer.Sound.play(shootsound)
        hasShot = True
    if (keys[pygame.K_e] or mouseclick[2]):
        thisExplosions = []
        for projectile in projectiles:
            if projectile[2] == True:
                explosionPos = [projectile[0][0], projectile[0][2]]
                explosions.append(explosionPos)
                thisExplosions.append(explosionPos)

                projectiles.remove(projectile)
    
    for explosion in explosions:
        if abovegrid([explosion[0], 0, explosion[1]], 0):
            pygame.mixer.Sound.play(explodesound)
            tiles[int(explosion[1]/gridSize)][int(explosion[0]/gridSize)] = 0
        player.AddExplosionVel(explosion)
        player.CapVel()

    enemyDistance = length(difference(player.pos, player2Pos))
    volume = 1 / (1 + enemyDistance)
    enemyshootsound.set_volume(volume)
    enemyjumpsound.set_volume(volume)
    if enemyShot:
        pygame.mixer.Sound.play(enemyshootsound)
    if enemyJumped:
        pygame.mixer.Sound.play(enemyjumpsound)

    if player.onGround == False:
        player.vel[1] -= 0.1

    if shotCooldown != 0:
        shotCooldown -= 1

    oldplayery = player.pos[1]
    player.pos[0] += player.vel[0]
    player.pos[1] += player.vel[1]
    player.pos[2] += player.vel[2]


    player.vel[0] *= 0.9
    player.vel[1] *= 0.98
    player.vel[2] *= 0.9


    if player.onGround == False:
        player.vel[1] -= gravityacc

    else:
        player.vel[0] *= 0.4
        player.vel[2] *= 0.4
        if player.vel[0] < 0.001 and player.vel[0] > -0.001:
            player.vel[0] = 0
        if player.vel[2] < 0.001 and player.vel[0] > -0.001:
            player.vel[2] = 0

    if player.pos[1] <= 20 and abovegrid(player.pos, 5):
        if oldplayery > 20:
            player.pos[1] = 20
            player.vel = [0,0,0]
            player.vel[1] = 0
            player.onGround = True
    else:
        player.onGround = False

    for projectile in projectiles:

        oldy = projectile[0][1]
        if projectile[2] == False:
            projectile[0][0] += projectile[1][0]
            projectile[0][1] += projectile[1][1]
            projectile[0][2] += projectile[1][2]
            projectile[1][1] -= gravityacc

        if oldy > 2 and projectile[0][1] <= 2 and abovegrid(projectile[0],1) == 1:
            projectile[1] = [0,0,0]
            projectile[0][1] = 2
            projectile[2] = True

        if (projectile[0][1] < 2 and player.pos[1] >= 20) or (projectile[0][1] >= 2 and player.pos[1] < 20):

            rprojectile = rotate(projectile[0])
            if rprojectile[2] > 10:
                pprojectile = project(rprojectile)
                pygame.draw.circle(screen, (0,0,0), pprojectile, 2/rprojectile[2]*screenDistance)


        
        if projectile[0][1] < -10:
            projectiles.remove(projectile)



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
                        
                points = [rotate(point) for point in tile]
                polygon = []
                for point in points:
                    tpoint = tuple(point)
                    if tpoint in cache:
                        polygon.append(cache[tpoint])


                    else:

                        
                        if point[2] > 10:
                            ppoint = project(point)
                            polygon.append(ppoint)
                            cache[tpoint] = ppoint
                            a += 1

                        else:
                            point2 = points[points.index(point) - 1]
                            if point2[2] > 10:
                                intpoint = line_intersection(point, point2)
                                tintpoint = tuple(intpoint)
                                if tintpoint in cache:                     
                                    polygon.append(cache[tintpoint])
                                else:
                                    pintpoint = project(intpoint)
                                    polygon.append(pintpoint)
                                    cache[tuple(intpoint)] = pintpoint
                                    a +=1

                            point2 = points[(points.index(point) + 1) % 4]
                            if point2[2] > 10:
                                
                                intpoint = line_intersection(point, point2)
                                tintpoint = tuple(intpoint)
                                if tintpoint in cache:
                                    polygon.append(cache[tintpoint])
                                else:
                                    pintpoint = project(intpoint)
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

    rbotPos = [rotate(player2Pos),rotate([player2Pos[0]-5,player2Pos[1]-20,player2Pos[2]-5]),rotate([player2Pos[0]+5,player2Pos[1]-20,player2Pos[2]+5]),rotate([player2Pos[0]-5,player2Pos[1]-20,player2Pos[2]+5]),rotate([player2Pos[0]+5,player2Pos[1]-20,player2Pos[2]-5])]
    if rbotPos[0][2] > 10:

        pbot = [project(rbotPos[0]), project(rbotPos[1]), project(rbotPos[2]), project(rbotPos[3]), project(rbotPos[4])]
        
        pygame.draw.polygon(screen, (0,160,0), (pbot[0], pbot[1], pbot[2]))
        pygame.draw.polygon(screen, (0,160,0), (pbot[0], pbot[3], pbot[4]))
        pygame.draw.circle(screen, (255,205,0), pbot[0], 8/rbotPos[0][2]*screenDistance)

    for projectile in projectilesPos:
        if (projectile[1] >= 2 and player.pos[1] >= 20) or (projectile[1] < 2 and player.pos[1] < 20):

            rprojectile = rotate(projectile)
            if rprojectile[2] > 10:
                pprojectile = project(rprojectile)
                pygame.draw.circle(screen, (0,0,0), pprojectile, 2/rprojectile[2]*screenDistance)
    
    for projectile in enemyProjectiles:
        if (projectile[1] >= 2 and player.pos[1] >= 20) or (projectile[1] < 2 and player.pos[1] < 20):

            rprojectile = rotate(projectile)
            if rprojectile[2] > 10:
                pprojectile = project(rprojectile)
                pygame.draw.circle(screen, (255,0,0), pprojectile, 2/rprojectile[2]*screenDistance)

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





