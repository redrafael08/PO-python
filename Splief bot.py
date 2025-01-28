import math
import pygame
from sys import exit
import random
import pygame.gfxdraw

pygame.init()
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
screenDistance = 400
screenWidth, screenHeight = screen.get_size()
screenCenter = (screenWidth / 2, screenHeight / 2)
horizontalVelCap = 10
verticalVelCap = 10

test1 = 0
test2 = 0
test3 = 0

class Player():
    def __init__(self, pos, vel, onGround):
        self.pos = pos
        self.vel = vel
        self.onGround = onGround
    
    def AddExplosionVel(self, explosionPos):
        difference = [self.pos[0] - explosionPos[0], self.pos[1] - explosionPos[1], self.pos[2] - explosionPos[2]]
        distance = length(difference)
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

player = Player([10, 25, 10], [0,0,0], False)
playerAngle = [0, 0]
shotCooldown = 0
playerShotColor = (0,0,0)
projectileSpeed = 10
mouseSensitivity = 0.006

walkSpeed = 3

bot = Player([200, 25, 200], [0,0,0], False)
botcooldown = 60
botSpeed = 3
botShotColor = (200,200,200)
lastMinDistance = 1000000000
targetPos = [200, 25, 200]

gridSize = 20
tiles = []
clock = pygame.time.Clock()
font = pygame.font.Font(None, 50)
pygame.mouse.set_visible(False)

projectiles = []

botimg = pygame.image.load('popetje 2.png')



for z in range(20):
    row = []
    for x in range(20):
        if (x+z)%1 == 0:
            row.append(1)
        else:
            row.append(0)

    tiles.append(row)


def length(vector):
    return (vector[0]**2 + vector[1]**2 + vector[2]**2)**0.5

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
        if (-size < position[0] < 20*gridSize+size and -size < position[2] < 20*gridSize+size) and (tiles[int((position[2]-size)/gridSize)][int((position[0]-size)/gridSize)] or tiles[int((position[2]-size)/gridSize)][int((position[0]+size)/gridSize)] == 1 or tiles[int((position[2]+size)/gridSize)][int((position[0]-size)/gridSize)] == 1 or tiles[int((position[2]+size)/gridSize)][int((position[0]+size)/gridSize)] == 1) and position[0] - size <= gridSize*20:
            return True
    return False

class Projectile():
    def __init__(self, pos, vel, onGround, fromPlayer):
        self.pos = pos
        randomness = 0.5
        self.vel = [vel[0] + (random.random() - 0.5) * randomness, vel[1] + (random.random() - 0.5) * randomness, vel[2] + (random.random() - 0.5) * randomness]
        self.onGround = onGround
        self.fromPlayer = fromPlayer


while True:
    clock.tick(30)
    screen.fill((174, 255, 255))


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
        walkSpeed = 0.1

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
        player.vel[1] = 2.5
        player.pos[1] = 21
        player.onGround = False
    if (keys[pygame.K_q] or mouseclick[0]) and shotCooldown == 0:
        shotCooldown = 10
        test1 = [sina * cosb * -5, sinb * 5, cosa * cosb * 5]
        test2 = length(test1)
        projectiles.append(Projectile(player.pos.copy(), [sina * cosb * -projectileSpeed + player.vel[0], sinb * projectileSpeed + player.vel[1], cosa * cosb * projectileSpeed + player.vel[2]], False, True))
    if (keys[pygame.K_e] or mouseclick[2]):
        for projectile in projectiles:
            if projectile.onGround and projectile.fromPlayer:
                player.AddExplosionVel(projectile.pos)
                bot.AddExplosionVel(projectile.pos)

                tiles[int(projectile.pos[2]/gridSize)][int(projectile.pos[0]/gridSize)] = 0
                projectiles.remove(projectile)
                
        player.CapVel()
        bot.CapVel()

    if player.onGround == False:
        player.vel[1] -= 0.1

    if shotCooldown != 0:
        shotCooldown -= 1

    oldplayery = player.pos[1]
    player.pos[0] += player.vel[0]
    player.pos[1] += player.vel[1]
    player.pos[2] += player.vel[2]

    if player.onGround == False:
        player.vel[0] *= 0.99
        player.vel[2] *= 0.99
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
            player.vel[1] = 0
            player.onGround = True
    else:
        player.onGround = False

    for projectile in projectiles:

        oldy = projectile.pos[1]
        if projectile.onGround == False:
            projectile.pos[0] += projectile.vel[0]
            projectile.pos[1] += projectile.vel[1]
            projectile.pos[2] += projectile.vel[2]
            projectile.vel[1] -= 0.1

        if oldy > 2 and 0 < projectile.pos[0] < 20*gridSize and 0 < projectile.pos[2] < 20*gridSize and projectile.pos[1] <= 2 and tiles[int(projectile.pos[2]/gridSize)][int(projectile.pos[0]/gridSize)] == 1:
            projectile.vel = [0,0,0]
            projectile.pos[1] = 2
            projectile.onGround = True

        if (projectile.pos[1] < 2 and player.pos[1] >= 20) or (projectile.pos[1] >= 2 and player.pos[1] < 20):

            rprojectile = rotate(projectile.pos)
            if rprojectile[2] > 10:
                pprojectile = project(rprojectile)
                if projectile.fromPlayer:
                    pygame.draw.circle(screen, playerShotColor, pprojectile, 2/rprojectile[2]*screenDistance)
                else: 
                    pygame.draw.circle(screen, botShotColor, pprojectile, 2/rprojectile[2]*screenDistance)


        
        elif projectile.pos[1] < -100:
            projectiles.remove(projectile)

    # Bot spul

    if bot.onGround:
        botSpeed = 1
    else:
        botSpeed = 0.1

    if not bot.onGround and not abovegrid(bot.pos, 5):
        if abovegrid(targetPos, 0):
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

    oldboty = bot.pos[1]
    bot.pos[0] += bot.vel[0]
    bot.pos[1] += bot.vel[1]
    bot.pos[2] += bot.vel[2]

    if not bot.onGround:
        bot.vel[1] -= 0.1
    
    if bot.onGround == False:
        bot.vel[0] *= 0.99
        bot.vel[2] *= 0.99
    else:
        bot.vel[0] *= 0.4
        bot.vel[2] *= 0.4
        if bot.vel[0] < 0.001 and bot.vel[0] > -0.001:
            bot.vel[0] = 0
        if bot.vel[2] < 0.001 and bot.vel[0] > -0.001:
            bot.vel[2] = 0

    if bot.pos[1] <= 20 and abovegrid(bot.pos, 5):
        if oldboty > 20:
            bot.pos[1] = 20
            bot.vel[1] = 0
            bot.onGround = True
    else:
        bot.onGround = False

    if botcooldown == 0:
        difference = [player.pos[0] - bot.pos[0], 0, player.pos[2] - bot.pos[2]] 
        distancePlayer = length(difference)
        direction = [difference[0], 0.2 * distancePlayer - 30 - bot.pos[1] * 0.4, difference[2]]
        distanceFactor = projectileSpeed / length(direction)
        direction = [direction[0] * distanceFactor, direction[1] * distanceFactor, direction[2] * distanceFactor]

        projectiles.append(Projectile(bot.pos.copy(), direction + bot.vel, False, False))
        if random.randint(1, 5) == 1:
            for projectile in projectiles:
                if projectile.onGround and not projectile.fromPlayer:
                    player.AddExplosionVel(projectile.pos)
                    bot.AddExplosionVel(projectile.pos)

                    tiles[int(projectile.pos[2]/gridSize)][int(projectile.pos[0]/gridSize)] = 0
                    projectiles.remove(projectile)
                
            player.CapVel()
            bot.CapVel()

        botcooldown = 30
    else:
        botcooldown -= 1

    # Render spul

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

    rbotPos = [rotate(bot.pos),rotate([bot.pos[0]-5,bot.pos[1]-20,bot.pos[2]-5]),rotate([bot.pos[0]+5,bot.pos[1]-20,bot.pos[2]+5]),rotate([bot.pos[0]-5,bot.pos[1]-20,bot.pos[2]+5]),rotate([bot.pos[0]+5,bot.pos[1]-20,bot.pos[2]-5])]
    if rbotPos[0][2] > 10:

        pbot = [project(rbotPos[0]), project(rbotPos[1]), project(rbotPos[2]), project(rbotPos[3]), project(rbotPos[4])]
        
        pygame.draw.polygon(screen, (0,160,0), (pbot[0], pbot[1], pbot[2]))
        pygame.draw.polygon(screen, (0,160,0), (pbot[0], pbot[3], pbot[4]))
        pygame.draw.circle(screen, (255,205,0), pbot[0], 8/rbotPos[0][2]*screenDistance)
      #  size = 20/rbotPos[2]*screenDistance, 30/rbotPos[2]*screenDistance
        #pygame.draw.rect(screen, (0,0,0), (pbot[0]-size[0]*0.5,pbot[1]-size[1]*0.33,size[0],size[1]))
      #  botimgscale = pygame.transform.scale(botimg, size)
      #  screen.blit(botimgscale, (pbot[0]-size[0]*0.5,pbot[1]-size[1]*0.33))


    for projectile in projectiles:
        if (projectile.pos[1] >= 2 and player.pos[1] >= 20) or (projectile.pos[1] < 2 and player.pos[1] < 20):

            rprojectile = rotate(projectile.pos)
            if rprojectile[2] > 10:
                pprojectile = project(rprojectile)
                if projectile.fromPlayer:
                    pygame.draw.circle(screen, playerShotColor, pprojectile, 2/rprojectile[2]*screenDistance)
                else: 
                    pygame.draw.circle(screen, botShotColor, pprojectile, 2/rprojectile[2]*screenDistance)

        

    if player.pos[1] < -10:
        exit()

    pygame.draw.line(screen, (0,200,0), (screenCenter[0]-15,screenCenter[1]), (screenCenter[0]-5,screenCenter[1]),2)
    pygame.draw.line(screen, (0,200,0), (screenCenter[0],screenCenter[1]-15), (screenCenter[0],screenCenter[1]-5),2)
    pygame.draw.line(screen, (0,200,0), (screenCenter[0]+15,screenCenter[1]), (screenCenter[0]+5,screenCenter[1]),2)
    pygame.draw.line(screen, (0,200,0), (screenCenter[0],screenCenter[1]+15), (screenCenter[0],screenCenter[1]+5),2)





    test1 = [round(player.vel[0], 2), round(player.vel[1], 2), round(player.vel[2], 2)]

    text = font.render(f"{round(clock.get_fps())}", True, (0, 0, 0))
    screen.blit(text, (100, 100))
    #text = font.render(f"{round(player.pos[0]), round(player.pos[1]), round(player.pos[2])}", True, (0, 0, 0))
    text = font.render(f"{test1}", True, (0, 0, 0))
    screen.blit(text, (100, 200))
    #text = font.render(f"{round(player.vel[0], 2), round(player.vel[1], 2), round(player.vel[2], 2)}", True, (0, 0, 0))
    #screen.blit(text, (100, 300))
    pygame.display.update()