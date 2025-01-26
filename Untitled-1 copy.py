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


playerPos = [200, 200, 200]
playerSpeed = [0,0,0]
walkSpeed = 0.1*50
playerAngle = [0, 0]


touchground = False
gridSize = 20
tiles = []
clock = pygame.time.Clock()
font = pygame.font.Font(None, 50)
pygame.mouse.set_visible(False)

projectiles = []

veldown = 0


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




while True:
    clock.tick(30)
    screen.fill((174, 255, 255))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    currentframe = clock.get_time()
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

    if keys[pygame.K_a]:
        playerPos[0] -= walkSpeed * cosa 
        playerPos[2] -= walkSpeed * sina 
    if keys[pygame.K_d]:
        playerPos[0] += walkSpeed * cosa 
        playerPos[2] += walkSpeed * sina 
    if keys[pygame.K_w]:
        playerPos[0] += walkSpeed * math.cos(playerAngle[0] + math.radians(90)) 
        playerPos[2] += walkSpeed * math.sin(playerAngle[0] + math.radians(90)) 
    if keys[pygame.K_s]:
        playerPos[0] -= walkSpeed * math.cos(playerAngle[0] + math.radians(90)) 
        playerPos[2] -= walkSpeed * math.sin(playerAngle[0] + math.radians(90)) 
    if keys[pygame.K_SPACE] and playerPos[1] == 20:
        veldown = -2.5
        playerPos[1] = 21
    if keys[pygame.K_q]:
        projectiles.append([playerPos.copy(),[sina,sinb,cosa],0,False])
    if keys[pygame.K_e]:
        for projectile in projectiles:

            if projectile[3] == True:
                tiles[int(projectile[0][2]/gridSize)][int(projectile[0][0]/gridSize)] = 0
                distance = ((projectile[0][0]-playerPos[0])**2+(projectile[0][1]-playerPos[1])**2+(projectile[0][2]-playerPos[2])**2)**0.5
            # if distance < 20:


                if projectile[0][0]-playerPos[0] != 0:
                    playerSpeed[0] -= 10000/(projectile[0][0]-playerPos[0])
                    if playerSpeed[0] > 5:
                        playerSpeed[0] = 5
                    if playerSpeed[0] < -5:
                        playerSpeed[0] = -5
                if (projectile[0][1]-20)-playerPos[1] != 0:
                    playerSpeed[1] -= 10000/((projectile[0][1]-20)-playerPos[1])
                    if playerSpeed[1] > 20:
                        playerSpeed[1] = 20
                    if playerSpeed[1] < -20:
                        playerSpeed[1] = -20
                if projectile[0][2]-playerPos[2] != 0:
                    playerSpeed[2] -= 10000/(projectile[0][2]-playerPos[2])
                    if playerSpeed[2] > 5:
                        playerSpeed[2] = 5
                    if playerSpeed[2] < -5:
                        playerSpeed[2] = -5

                projectiles.remove(projectile)




    oldplayery = playerPos[1]
    playerPos[0] += playerSpeed[0]
    playerPos[1] += playerSpeed[1]
    playerPos[2] += playerSpeed[2]

    playerSpeed[0] *= 0.99
    playerSpeed[1] *= 0.99
    playerSpeed[2] *= 0.99


    if touchground == False:
        playerPos[1] -= veldown
        veldown += 0.1

    

    if playerPos[1] <= 20 and 0 < playerPos[0] < 20*gridSize and 0 < playerPos[2] < 20*gridSize and tiles[int(playerPos[2]/gridSize)][int(playerPos[0]/gridSize)] == 1:
        if oldplayery > 20:
            playerPos[1] = 20
            playerSpeed = [0,0,0]
            veldown = 0
            touchground = True
    else:
        touchground = False

    # projection


    for projectile in projectiles:

        oldy = projectile[0][1]
        if projectile[3] == False:
            projectile[0][0] -= projectile[1][0]*5
            projectile[0][1] += projectile[1][1]*5-projectile[2]
            projectile[0][2] += projectile[1][2]*5
            projectile[2] += 0.1

        if oldy > 2 and 0 < projectile[0][0] < 20*gridSize and 0 < projectile[0][2] < 20*gridSize and projectile[0][1] <= 2 and tiles[int(projectile[0][2]/gridSize)][int(projectile[0][0]/gridSize)] == 1:
            projectile[1] = [0,0,0]
            projectile[0][1] = 2
            projectile[2] = 0
            projectile[3] = True

        if (projectile[0][1] < 2 and playerPos[1] >= 20) or (projectile[0][1] >= 2 and playerPos[1] < 20):

            rprojectile = rotate(projectile[0])
            if rprojectile[2] > 10:
                pprojectile = project(rprojectile)
                pygame.draw.circle(screen, (0,0,0), pprojectile, 2/rprojectile[2]*screenDistance)


        
        elif projectile[0][1] < -100:
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
                            a +=1

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
        if (projectile[0][1] >= 2 and playerPos[1] >= 20) or (projectile[0][1] < 2 and playerPos[1] < 20):

            rprojectile = rotate(projectile[0])
            if rprojectile[2] > 10:
                pprojectile = project(rprojectile)
                pygame.draw.circle(screen, (0,0,0), pprojectile, 2/rprojectile[2]*screenDistance)


    pygame.draw.line(screen, (0,255,0), (screenCenter[0]-15,screenCenter[1]), (screenCenter[0]-5,screenCenter[1]),2)
    pygame.draw.line(screen, (0,255,0), (screenCenter[0],screenCenter[1]-15), (screenCenter[0],screenCenter[1]-5),2)
    pygame.draw.line(screen, (0,255,0), (screenCenter[0]+15,screenCenter[1]), (screenCenter[0]+5,screenCenter[1]),2)
    pygame.draw.line(screen, (0,255,0), (screenCenter[0],screenCenter[1]+15), (screenCenter[0],screenCenter[1]+5),2)







    text = font.render(f"{round(clock.get_fps())}", True, (0, 0, 0))
    screen.blit(text, (100, 100))
    text = font.render(f"{playerPos}", True, (0, 0, 0))
    screen.blit(text, (100, 200))
    text = font.render(f"{a}", True, (0, 0, 0))
    screen.blit(text, (100, 300))
    pygame.display.update()





