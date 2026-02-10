import pygame
import time
pygame.init()

screen = pygame.display.set_mode((1000,720))

pygame.display.set_caption("Snake Game by Me")

green = (188, 227, 199)
black = (0, 0, 0)
white = (255, 255, 255) 
red = (255, 0, 0)
blue = (0, 0, 255)

snake_x = 490
snake_y = 350

pygame.draw.rect(screen, red, [snake_x, snake_y, 20, 20])
pygame.display.update()

quit_game = False
while not quit_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game = True




pygame.quit()
quit()