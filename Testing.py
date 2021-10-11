import pygame
from pygame.locals import*

pygame.init()

screen = pygame.display.set_mode((1980, 1080))
pygame.display.set_caption('Platformer')

run = True
while run:

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

pygame.quit()