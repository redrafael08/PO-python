import math
import pygame
from sys import exit
import random
import numpy as np


pygame.init()
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
screenWidth, screenHeight = screen.get_size()
screenCenter = (screenWidth / 2, screenHeight / 2)

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
    global currentbuttons
    currentbuttons = newpage



buttons = []

mainbuttons = [
    lambda: Button([screenCenter[0],screenCenter[1]],[500,100], 'Singleplayer',lambda: print('he')),
    lambda: Button([screenCenter[0],screenCenter[1]+150],[500,100], 'Multiplayer',lambda: difpage(multiplayerbuttons)),
    lambda: Button([screenCenter[0],screenCenter[1]+300],[500,100], 'Quit', lambda: exit())
]

multiplayerbuttons = []
joinbuttons = []

currentbuttons = mainbuttons

clock = pygame.time.Clock()
while True:
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
    for button in currentbuttons:
        button()





    pygame.display.update()
