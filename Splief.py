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


playerPos = [200, 25, 200]
playerSpeed = [0,0,0]
walkSpeed = 3
playerAngle = [0, 0]
shotCooldown = 0

touchground = False
gridSize = 20
tiles = []
clock = pygame.time.Clock()
font = pygame.font.Font(None, 50)
pygame.mouse.set_visible(False)

projectiles = []


veldown = 0
gravityacc = 0.3



for z in range(20):
    row = []
    for x in range(20):
        if (x+z)%1 == 0:
            row.append(1)
        else:
            row.append(0)

    tiles.append(row)




def line_intersection(point1, point2):
    t = (10 - point1[2]) / (point2[2] - point1[2])
    x = point1[0] + t * (point2[0] - point1[0])
    y = point1[1] + t * (point2[1] - point1[1])
    return [x, y, 10]


def rotate(point):
    dx, dy, dz = point[0] - playerPos[0], point[1] - playerPos[1], point[2] - playerPos[2]
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
    if (-size < position[0] < 20*gridSize+size and -size < position[2] < 20*gridSize+size) and (tiles[int((position[2]-size)/gridSize)][int((position[0]-size)/gridSize)] or tiles[int((position[2]-size)/gridSize)][int((position[0]+size)/gridSize)] == 1 or tiles[int((position[2]+size)/gridSize)][int((position[0]-size)/gridSize)] == 1 or tiles[int((position[2]+size)/gridSize)][int((position[0]+size)/gridSize)] == 1):
        return True
    else:
        return False

class Projectile():
    def __init__(self, pos, vel, onGround):
        self.pos = pos
        self.vel = vel
        self.onGround = onGround


while True:
    clock.tick(30)
    screen.fill((174, 255, 255))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    currentframe = clock.get_time()
    mouse = pygame.mouse.get_pos()
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

    if touchground:
        walkSpeed = 3
    else:
        walkSpeed = 0.3

    if keys[pygame.K_a]:
        playerSpeed[0] -= walkSpeed * cosa 
        playerSpeed[2] -= walkSpeed * sina 
    if keys[pygame.K_d]:
        playerSpeed[0] += walkSpeed * cosa 
        playerSpeed[2] += walkSpeed * sina 
    if keys[pygame.K_w]:
        playerSpeed[0] += walkSpeed * math.cos(playerAngle[0] + math.radians(90)) 
        playerSpeed[2] += walkSpeed * math.sin(playerAngle[0] + math.radians(90)) 
    if keys[pygame.K_s]:
        playerSpeed[0] -= walkSpeed * math.cos(playerAngle[0] + math.radians(90)) 
        playerSpeed[2] -= walkSpeed * math.sin(playerAngle[0] + math.radians(90)) 

    if keys[pygame.K_SPACE] and touchground:
        playerSpeed[1] += 5
        playerPos[1] = 21
        touchground = False


    if keys[pygame.K_q] and shotCooldown == 0:
        shotCooldown = 10
        randomness = 0.5
        xOffset = (random.random() - 0.5) * randomness
        yOffset = (random.random() - 0.5) * randomness
        zOffset = (random.random() - 0.5) * randomness

        projectiles.append(Projectile(playerPos.copy(), [sina * cosb * -20 + xOffset + playerSpeed[0], sinb * 20 + yOffset + playerSpeed[1], cosa * cosb * 20 + zOffset + playerSpeed[2]], False))

    if keys[pygame.K_e]:
        for projectile in projectiles:

            if projectile.onGround == True:
                difference = [playerPos[0] - projectile.pos[0], playerPos[1] - projectile.pos[1], playerPos[2] - projectile.pos[2]]
                tiles[int(projectile.pos[2]/gridSize)][int(projectile.pos[0]/gridSize)] = 0
                distanceSqrd = (difference[0]**2+difference[1]**2+difference[2]**2)
                distance = distanceSqrd**0.5
                direction = [difference[0] / distance, difference[1] / distance, difference[2] / distance]

                playerSpeed[0] += direction[0] / distance * 10
                playerSpeed[1] -= (direction[1] - 5) / distance * 10
                playerSpeed[2] += direction[2] / distance * 10
                
                if playerSpeed[0] > 5:
                    playerSpeed[0] = 5
                if playerSpeed[0] < -5:
                    playerSpeed[0] = -5
                if playerSpeed[1] > 20:
                    playerSpeed[1] = 20
                if playerSpeed[1] < -20:
                    playerSpeed[1] = -20
                if playerSpeed[2] > 5:
                    playerSpeed[2] = 5
                if playerSpeed[2] < -5:
                    playerSpeed[2] = -5

                projectiles.remove(projectile)

    if touchground == False:
        playerSpeed[1] -= 0.1

    if shotCooldown != 0:
        shotCooldown -= 1

    oldplayery = playerPos[1]
    playerPos[0] += playerSpeed[0]
    playerPos[1] += playerSpeed[1]
    playerPos[2] += playerSpeed[2]


    playerSpeed[0] *= 0.9
    playerSpeed[1] *= 0.98
    playerSpeed[2] *= 0.9


    if touchground == False:
        playerSpeed[1] -= gravityacc

    else:
        playerSpeed[0] *= 0.4
        playerSpeed[2] *= 0.4
        if playerSpeed[0] < 0.001 and playerSpeed[0] > -0.001:
            playerSpeed[0] = 0
        if playerSpeed[2] < 0.001 and playerSpeed[0] > -0.001:
            playerSpeed[2] = 0

    if playerPos[1] <= 20 and abovegrid(playerPos, 5):
        if oldplayery > 20:
            playerPos[1] = 20
            playerSpeed = [0,0,0]
            playerSpeed[1] = 0
            touchground = True
    else:
        touchground = False

    for projectile in projectiles:

        oldy = projectile.pos[1]
        if projectile.onGround == False:
            projectile.pos[0] += projectile.vel[0]
            projectile.pos[1] += projectile.vel[1]
            projectile.pos[2] += projectile.vel[2]
            projectile.vel[1] -= gravityacc

        if oldy > 2 and projectile.pos[1] <= 2 and abovegrid(projectile.pos,1) == 1:
            projectile.vel = [0,0,0]
            projectile.pos[1] = 2
            projectile.onGround = True

        if (projectile.pos[1] < 2 and playerPos[1] >= 20) or (projectile.pos[1] >= 2 and playerPos[1] < 20):

            rprojectile = rotate(projectile.pos)
            if rprojectile[2] > 10:
                pprojectile = project(rprojectile)
                pygame.draw.circle(screen, (0,0,0), pprojectile, 2/rprojectile[2]*screenDistance)


        
        if projectile.pos[1] < -10:
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

    for projectile in projectiles:
        if (projectile.pos[1] >= 2 and playerPos[1] >= 20) or (projectile.pos[1] < 2 and playerPos[1] < 20):

            rprojectile = rotate(projectile.pos)
            if rprojectile[2] > 10:
                pprojectile = project(rprojectile)
                pygame.draw.circle(screen, (0,0,0), pprojectile, 2/rprojectile[2]*screenDistance)

    if playerPos[1] < -10:
        exit()

    pygame.draw.line(screen, (0,200,0), (screenCenter[0]-15,screenCenter[1]), (screenCenter[0]-5,screenCenter[1]),2)
    pygame.draw.line(screen, (0,200,0), (screenCenter[0],screenCenter[1]-15), (screenCenter[0],screenCenter[1]-5),2)
    pygame.draw.line(screen, (0,200,0), (screenCenter[0]+15,screenCenter[1]), (screenCenter[0]+5,screenCenter[1]),2)
    pygame.draw.line(screen, (0,200,0), (screenCenter[0],screenCenter[1]+15), (screenCenter[0],screenCenter[1]+5),2)







    text = font.render(f"{round(clock.get_fps())}", True, (0, 0, 0))
    screen.blit(text, (100, 100))
    text = font.render(f"{round(playerPos[0]), round(playerPos[1]), round(playerPos[2])}", True, (0, 0, 0))
    screen.blit(text, (100, 200))
    text = font.render(f"{round(playerSpeed[0]), round(playerSpeed[1]), round(playerSpeed[2])}", True, (0, 0, 0))
    screen.blit(text, (100, 300))
    text = font.render(f"{len(projectiles)}", True, (0, 0, 0))
    screen.blit(text, (100, 400))
    pygame.display.update()





