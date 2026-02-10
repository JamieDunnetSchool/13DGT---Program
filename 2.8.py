
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
text_colour = (0, 0, 0)
quit_game = False



clock = pygame.time.Clock()
snake_x = 490
snake_y = 350
snake_x_change = 0
snake_y_change = 0
pygame.draw.rect(screen, red, [snake_x, snake_y, 20, 20])
pygame.display.update()
font = pygame.font.Font("freesansbold.ttf", 50)
def message(msg,txt_colour, bkgd_colour):
    txt = font.render(msg, True, text_colour, bkgd_colour)
    text_box = txt.get_rect(center = (500, 360))
    screen.blit(txt, text_box)

while not quit_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake_x_change = -20
                snake_y_change = 0
            elif event.key == pygame.K_RIGHT:
                snake_x_change = 20
                snake_y_change = 0
            elif event.key == pygame.K_UP:
                snake_y_change = -20
                snake_x_change = 0
            elif event.key == pygame.K_DOWN:
                snake_y_change = 20
                snake_x_change = 0

    if snake_x >= 1000 or snake_x < 0 or snake_y >= 720 or snake_y < 0:
        message ("You died!", black, white)
        pygame.display.update()
        time.sleep(3)
        quit_game = True
    snake_x += snake_x_change
    snake_y += snake_y_change
    screen.fill(green)
    pygame.draw.rect(screen, red, [snake_x, snake_y, 20, 20])
    pygame.display.update()
    clock.tick(10)


pygame.quit()
quit()


