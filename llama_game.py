### this program is a llama game for playing

import pygame
import time
import random

pygame.init()

screen = pygame.display.set_mode((1000, 500))
pygame.display.set_caption("Llama game")

game_icon = pygame.image.load("llama_icon.png")
pygame.display.set_icon(game_icon)

pygame.key.set_repeat()

green = (188, 227, 199)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (78, 159, 229)
brown = (150, 75, 0)
FPS = 30
ground_size1 = 1000
ground_size2 = 240
quit_game = False
textX = 750
textY = 10
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
start_time = time.time()
touch_ground = False
jump_lock = False
ground_y = 260 - llama_h
gravity = 5
jump_power = -50
score = 0
pass_score = 0
final_score = 0
game_over = False
game_ending = False
font = pygame.font.Font("freesansbold.ttf", 50)

def message(msg, txt_colour, bkgd_colour):
    txt = font.render(msg, True, txt_colour, bkgd_colour)
    text_box = txt.get_rect(center=(500, 360))
    screen.blit(txt, text_box)

def show_score(x, y):
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    hi_text = font.render("High: " + str(high_score), True, (255, 255, 255))
    screen.blit(score_text, (x, y))
    screen.blit(hi_text, (x, y + 55))

def load_high_score():
    try:
        with open("highsocre.txt", "r") as hi_score_file:
            value = hi_score_file.read().strip()
    except FileNotFoundError:
        with open("highsocre.txt", "w") as hi_score_file:
            hi_score_file.write("0")
        value = "0"

    if value == "":
        return 0
    return int(value)

def save_high_score(value):
    with open("highsocre.txt", "w") as hi_score_file:
        hi_score_file.write(str(value))

high_score = load_high_score()

class cactus:
    def __init__(self, cactus_x, cactus_y, name, w, h, speed, points):
        self.cactus_x = cactus_x
        self.cactus_y = cactus_y
        self.name = name
        self.w = w
        self.h = h
        self.speed = speed
        self.points = points

    def make_food(self):
        cactu = pygame.Rect(self.cactus_x, self.cactus_y, self.w, self.h)
        cac = pygame.image.load("cactus.png").convert_alpha()
        resized_cac = pygame.transform.smoothscale(cac, [self.w, self.h])
        screen.blit(resized_cac, cactu)

    def hit(self, llama_x, llama_y, llama_w, llama_h):
        global game_ending, final_score, score
        self.cactus_x -= self.speed
        cactus_rect = pygame.Rect(self.cactus_x, self.cactus_y, self.w, self.h)
        llama_rect = pygame.Rect(llama_x, llama_y, llama_w, llama_h)

        if llama_rect.colliderect(cactus_rect):
            if game_ending == False:
                final_score = int(time.time() - start_time) + pass_score
                score = final_score
            game_ending = True

        if self.cactus_x < -self.w:
            self.cactus_x = 1000 + random.randint(200, 600)
            return self.points
        return 0

def reset_game():
    global llama_x, llama_y, llama_y_change, touch_ground, jump_lock
    global score, pass_score, start_time, game_ending, final_score
    global cactus1, cactus2, cactus3, cactus_list

    llama_x = 100
    llama_y = 220
    llama_y_change = 0
    touch_ground = False
    jump_lock = False

    score = 0
    pass_score = 0
    final_score = 0
    start_time = time.time()
    game_ending = False

    cactus1 = cactus(1200, cactus_y, "cactus1", cactus_w, cactus_h, 10, 1)
    cactus2 = cactus(1600, cactus_y, "cactus2", cactus_w, cactus_h, 10, 1)
    cactus3 = cactus(2000, cactus_y, "cactus3", cactus_w, cactus_h, 10, 1)
    cactus_list = [cactus1, cactus2, cactus3]

cactus1 = cactus(1200, cactus_y, "cactus1", cactus_w, cactus_h, 10, 1)
cactus2 = cactus(1600, cactus_y, "cactus2", cactus_w, cactus_h, 10, 1)
cactus3 = cactus(2000, cactus_y, "cactus3", cactus_w, cactus_h, 10, 1)
cactus_list = [cactus1, cactus2, cactus3]

while not quit_game:

    while game_ending == True:
        score = final_score

        if score > high_score:
            high_score = score
            save_high_score(high_score)

        screen.fill(blue)
        ground_rect = pygame.Rect(0, 500 - ground_size2, ground_size1, ground_size2)
        pygame.draw.rect(screen, brown, ground_rect)
        show_score(textX, textY)
        message("You died! Press X to quit, C to play again", black, white)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game = True
                game_ending = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    quit_game = True
                    game_ending = False
                    break
                elif event.key == pygame.K_c:
                    reset_game()
                    break

        clock.tick(FPS)

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

    score = int(time.time() - start_time) + pass_score

    screen.fill(blue)
    ground_rect = pygame.Rect(0, 500 - ground_size2, ground_size1, ground_size2)
    pygame.draw.rect(screen, brown, ground_rect)

    llama = pygame.Rect(llama_x, llama_y, llama_h, llama_w)
    fakellama = pygame.image.load("Llama.png").convert_alpha()
    resized_llama = pygame.transform.smoothscale(fakellama, [llama_h, llama_w])
    screen.blit(resized_llama, llama)

    for items in cactus_list:
        items.make_food()
        pass_score += items.hit(llama_x, llama_y, llama_w, llama_h)

    show_score(textX, textY)
    pygame.display.update()
    clock.tick(FPS)

score = final_score if game_ending else int(time.time() - start_time) + pass_score
if score > high_score:
    high_score = score
save_high_score(high_score)

pygame.quit()
quit()