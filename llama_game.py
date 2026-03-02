import pygame
import time
import random
pygame.init()

screen = pygame.display.set_mode((1000, 500))
pygame.display.set_caption("Llama game")

game_icon = pygame.image.load('llama_icon.png')
pygame.display.set_icon(game_icon)

pygame.key.set_repeat()

green = (188, 227, 199)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (78, 159, 229)
brown = (150, 75, 0)
fps = 60
ground_size1 = 1000
ground_size2 = 240
quit_game = False

clock = pygame.time.Clock()

llama_x = 100
llama_y = 220
llama_w = 40
llama_h = 40

cactus_x = 1200
cactus_y = 220
cactus_w = 40
cactus_h = 40

llama_x_change = 0
llama_y_change = 0

touch_ground = False
jump_lock = False

ground_y = 260 - llama_h
gravity = 10
jump_power = -50

while not quit_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game = True

        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == pygame.K_SPACE) and touch_ground == True and jump_lock == False:
                llama_y_change = jump_power
                touch_ground = False
                jump_lock = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                jump_lock = False

    llama_y += llama_y_change
    llama_y_change += gravity

    cactus_x -= 10

    if llama_y >= ground_y:
        llama_y = ground_y
        llama_y_change = 0
        touch_ground = True

    if llama_y < 0:
        llama_y = 0
        llama_y_change = 0

    screen.fill(blue)

    ground_rect = pygame.Rect(0, 500 - ground_size2, ground_size1, ground_size2)
    pygame.draw.rect(screen, brown, ground_rect)

    llama = pygame.Rect(llama_x, llama_y, llama_h, llama_w)
    fakellama = pygame.image.load('Llama.png').convert_alpha()
    resized_llama = pygame.transform.smoothscale(fakellama, [llama_h, llama_w])
    screen.blit(resized_llama, llama)

    cactus = pygame.Rect(cactus_x, cactus_y, cactus_h, cactus_w)
    fakecac = pygame.image.load('cactus.png').convert_alpha()
    resized_cactus = pygame.transform.smoothscale(fakecac, [cactus_h, cactus_w])
    screen.blit(resized_cactus, cactus)

    pygame.display.update()
    clock.tick(10)

pygame.quit()
quit()