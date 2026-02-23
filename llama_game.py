
import pygame
import time
pygame.init()

screen = pygame.display.set_mode((1000,500))

pygame.display.set_caption("Snake Game by Me")

green = (188, 227, 199)
black = (0, 0, 0)
white = (255, 255, 255) 
red = (255, 0, 0)
blue = (78, 159, 229)

quit_game = False

clock = pygame.time.Clock()

pygame.display.update()


while not quit_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake_y_change = -20
                snake_x_change = 0
            elif event.key == pygame.K_DOWN:
                snake_y_change = 20
                snake_x_change = 0

    screen.fill(blue)
    pygame.display.update()
    clock.tick(10)


pygame.quit()
quit()


