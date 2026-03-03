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

score = 0
game_over = False

class cactus:

    def __init__(self, cactus_x, cactus_y, cactus_image, points, name, w, h, speed):
        self.cactus_x = cactus_x
        self.cactus_y = cactus_y
        self.cactus_image = cactus_image
        self.points = points
        self.name = name
        self.w = w
        self.h = h
        self.speed = speed
    def make_food(self):
        cactu = pygame.Rect(self.cactus_x, self.cactus_y, self.w, self.h)
        cactus_png = str(self.cactus_image)
        cac = pygame.image.load(cactus_png).convert_alpha()
        resized_cac = pygame.transform.smoothscale(cac, [self.w, self.h])
        screen.blit(resized_cac, cactu)

    def hit(self, llama_x, llama_y, llama_w, llama_h):
        global quit_game, game_over, score
        self.cactus_x -= self.speed
        cactus_rect = pygame.Rect(self.cactus_x, self.cactus_y, self.w, self.h)
        llama_rect = pygame.Rect(llama_x, llama_y, llama_w, llama_h)
        if llama_rect.colliderect(cactus_rect):
            game_over = True
            quit_game = True
        if self.cactus_x < -self.w:
            self.cactus_x = 1000 + random.randint(200, 600)
            score += self.points

cactus1 = cactus(1200, cactus_y, "cactus.png", 1, "cactus1", cactus_w, cactus_h, 10)
cactus2 = cactus(1600, cactus_y, "cactus.png", 1, "cactus2", cactus_w, cactus_h, 10)
cactus3 = cactus(2000, cactus_y, "cactus.png", 1, "cactus3", cactus_w, cactus_h, 10)

cactus_list = [cactus1, cactus2, cactus3]

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

    for items in cactus_list:
        cactus.make_food(items)
        cactus.hit(items, llama_x, llama_y, llama_w, llama_h)

    pygame.display.update()
    clock.tick(10)

pygame.quit()
quit()