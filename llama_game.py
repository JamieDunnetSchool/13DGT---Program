import pygame
import time
pygame.init()

screen = pygame.display.set_mode((1000, 500))
pygame.display.set_caption("Llama game")

game_icon = pygame.image.load('llama_icon.png')
pygame.display.set_icon(game_icon)

green = (188, 227, 199)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (78, 159, 229)
brown = (150, 75, 0)

ground_size1 = 1000
ground_size2 = 240
quit_game = False

clock = pygame.time.Clock()

llama_x = 100
llama_y = 220
llama_w = 40
llama_h = 40

cactus_x = 300
cactus_y = 220
cactus_w = 40
cactus_h = 40

snake_x_change = 0
snake_y_change = 0

while not quit_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP  or event.key == pygame.K_SPACE:
                snake_y_change = -20
                snake_x_change = 0
            elif event.key == pygame.K_DOWN:
                snake_y_change = 20
                snake_x_change = 0
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                snake_y_change = 0

    llama_y += snake_y_change

    if llama_y < 0:
        llama_y = 0
    if llama_y > 260 - llama_h:
        llama_y = 260 - llama_h

    screen.fill(blue)

    ground_rect = pygame.Rect(0, 500 - ground_size2, ground_size1, ground_size2)
    pygame.draw.rect(screen, brown, ground_rect)

    llama = pygame.Rect(llama_x, llama_y, llama_h, llama_w)
    fakellama = pygame.image.load('Llama.png').convert_alpha()
    resized_llama = pygame.transform.smoothscale(fakellama, [llama_h,llama_w])
    screen.blit(resized_llama, llama)

    cactus = pygame.Rect(cactus_x, cactus_y, cactus_h, cactus_w)
    fakecac = pygame.image.load('cactus.png').convert_alpha()
    resized_cactus = pygame.transform.smoothscale(fakecac, [cactus_h,cactus_w])
    screen.blit(resized_cactus, cactus)


    pygame.display.update()
    clock.tick(10)

pygame.quit()
quit()