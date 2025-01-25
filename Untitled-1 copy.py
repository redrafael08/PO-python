import math
import pygame
from sys import exit
import random
#import numpy as np


pygame.init()
screen = pygame.display.set_mode((1000, 600))
screenDistance = 400
screenWidth, screenHeight = screen.get_size()
screenCenter = (screenWidth / 2, screenHeight / 2)


playerPos = [200, 500, 200]
playerSpeed = 0.1
playerAngle = [0, 0]


gridSize = 100
tiles = []
clock = pygame.time.Clock()
font = pygame.font.Font(None, 50)
pygame.mouse.set_visible(False)


for z in range(30):
    for x in range(30):
        tiles.append(
            [[x * gridSize, 0, z * gridSize],
             [x * gridSize + gridSize, 0, z * gridSize],
             [x * gridSize + gridSize, 0, z * gridSize + gridSize],
             [x * gridSize, 0, z * gridSize + gridSize]]
        )




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
    clock.tick(60)
    screen.fill((255, 255, 255))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    currentframe = clock.get_time()
    keys = pygame.key.get_pressed()


    if keys[pygame.K_LEFT]:
        playerAngle[0] += math.radians(0.1) * currentframe
    if keys[pygame.K_RIGHT]:
        playerAngle[0] -= math.radians(0.1) * currentframe
    if keys[pygame.K_UP]:
        playerAngle[1] += math.radians(0.1) * currentframe
    if keys[pygame.K_DOWN]:
        playerAngle[1] -= math.radians(0.1) * currentframe


    sina, cosa = math.sin(playerAngle[0]), math.cos(playerAngle[0])
    sinb, cosb = math.sin(playerAngle[1]), math.cos(playerAngle[1])

    if keys[pygame.K_a]:
        playerPos[0] -= playerSpeed * cosa * currentframe
        playerPos[2] -= playerSpeed * sina * currentframe
    if keys[pygame.K_d]:
        playerPos[0] += playerSpeed * cosa * currentframe
        playerPos[2] += playerSpeed * sina * currentframe
    if keys[pygame.K_w]:
        playerPos[0] += playerSpeed * math.cos(playerAngle[0] + math.radians(90)) * currentframe
        playerPos[2] += playerSpeed * math.sin(playerAngle[0] + math.radians(90)) * currentframe
    if keys[pygame.K_s]:
        playerPos[0] -= playerSpeed * math.cos(playerAngle[0] + math.radians(90)) * currentframe
        playerPos[2] -= playerSpeed * math.sin(playerAngle[0] + math.radians(90)) * currentframe
    if keys[pygame.K_SPACE]:
        playerPos[1] += 5
    if keys[pygame.K_LSHIFT]:
        playerPos[1] -= 5


    polygons = []

    for tile in tiles:

        points = [rotate(point) for point in tile]
        polygon = []
        for point in points:
            if point[2] > 0:
                polygon.append(project(point))
            else:
                point2 = points[points.index(point) - 1]
                if point2[2] > 0:
                    polygon.append(project(line_intersection(point, point2)))
                point2 = points[(points.index(point) + 1) % len(points)]
                if point2[2] > 0:
                    polygon.append(project(line_intersection(point, point2)))

        if len(polygon) > 2 and any(0 < p[0] < screenWidth and 0 < p[1] < screenHeight for p in polygon):
            polygons.append(polygon)



    for polygon in polygons:
        pygame.draw.polygon(screen, (sum(polygon[0])%255, 0, 0), polygon)


    text = font.render(f"{round(clock.get_fps())}", True, (0, 0, 0))
    screen.blit(text, (100, 100))
    text = font.render(f"{len(polygons)}", True, (0, 0, 0))
    screen.blit(text, (100, 200))

    pygame.display.update()
