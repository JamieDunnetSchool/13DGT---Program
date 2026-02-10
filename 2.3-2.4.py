import pygame
import time
pygame.init()

screen = pygame.display.set_mode((1000,720))

pygame.display.set_caption("Snake Game by Me")

green = (188, 227, 199)

quit_game = False
while not quit_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game = True

pygame.quit()
quit()