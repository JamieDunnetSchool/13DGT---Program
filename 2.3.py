import pygame
import time
pygame.init()

screen = pygame.display.set_mode((1000,720))
## game_icon = pygame.image.load('snake_icon.png')  ### need the png
pygame.display.set_caption("Snake Game by Me")
### pygame.display.set_icon(game_icon)

time.sleep(30)

pygame.quit()
quit()