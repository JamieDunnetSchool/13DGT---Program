"""This file program is a flappy brib game for playing."""

import pygame
import time
import random

pygame.init()

# Screen and icon set up
screen = pygame.display.set_mode((288, 512))
pygame.display.set_caption("Fabbly-prip")
game_icon = pygame.image.load("favicon.ico")
pygame.display.set_icon(game_icon)

# Backround
background = pygame.image.load("background-day.png").convert()
background = pygame.transform.smoothscale(background, (288, 512))
pygame.key.set_repeat()

# colours
green = (188, 227, 199)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (78, 159, 229)
brown = (150, 75, 0)

FPS = 30
quit_game = False
textx = 10
texty = 10
clock = pygame.time.Clock()

# Bird position and size
brid_x = 100
brid_y = 220
brid_w = 40
brid_h = 40

# Pipe starting position and size
pipe_x = 1200
pipe_y = -250
pipe_w = 60
pipe_h = 400

# Movement variables
llama_x_change = 0
brid_y_change = 0
start_time = time.time()
ground_y = 512 - brid_h
gravity = 1
jump_power = -12

# scoring
score = 0
pass_score = 0
final_score = 0

# game states
game_over = False
game_ending = False
font = pygame.font.Font("freesansbold.ttf", 20)


def message(msg, txt_colour, bkgd_colour):
    """Return the color and font values of the text."""
    txt = font.render(msg, True, txt_colour, bkgd_colour)
    text_box = txt.get_rect(center=(144, 256))
    screen.blit(txt, text_box)


def show_score(x, y):
    """Return the lattuide and landutude values of the text."""
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    hi_text = font.render("High: " + str(high_score), True, (255, 255, 255))
    screen.blit(score_text, (x, y))
    screen.blit(hi_text, (x, y + 25))


def load_high_score():
    """Return the sore values of the score to make the highscore."""
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
    """Return the Highscore  values of the file."""
    with open("highsocre.txt", "w") as hi_score_file:
        hi_score_file.write(str(value))


high_score = load_high_score()

class pipe:
    """Represents a pipe location and points."""
    def __init__(self, pipe_x, pipe_y, name, w, h, speed, points):
        self.pipe_x = pipe_x
        self.pipe_y = pipe_y
        self.name = name
        self.w = w
        self.h = h
        self.speed = speed
        self.points = points
        self.side = random.choice(["top", "bottom"])
        self.passed = False

        if self.side == "top":
            self.pipe_y = 0
            self.h = random.randint(120, 260)
        else:
            self.h = random.randint(120, 260)
            self.pipe_y = 512 - self.h

    def make_food(self):
        pipetu = pygame.Rect(self.pipe_x, self.pipe_y, self.w, self.h)
        pip = pygame.image.load("pipe-green.png").convert_alpha()

        if self.side == "top":
            pipe_flip = pygame.transform.flip(pip, False, True)
            resized_pipe = pygame.transform.smoothscale(pipe_flip, [self.w, self.h])
        else:
            resized_pipe = pygame.transform.smoothscale(pip, [self.w, self.h])

        screen.blit(resized_pipe, pipetu)

    def hit(self, brid_x, brid_y, brid_w, brid_h):
        global game_ending, final_score, score
        self.pipe_x -= self.speed

        cactus_rect = pygame.Rect(self.pipe_x, self.pipe_y, self.w, self.h)
        llama_rect = pygame.Rect(brid_x, brid_y, brid_w, brid_h)

        if llama_rect.colliderect(cactus_rect):
            if game_ending == False:
                final_score = pass_score
                score = final_score
            game_ending = True

        if self.passed == False and self.pipe_x + self.w < brid_x:
            self.passed = True
            return self.points

        if self.pipe_x < -self.w:
            self.pipe_x = 1000 + random.randint(200, 600)
            self.side = random.choice(["top", "bottom"])

            if self.side == "top":
                self.pipe_y = 0
                self.h = random.randint(120, 260)
            else:
                self.h = random.randint(120, 260)
                self.pipe_y = 512 - self.h

            self.passed = False
            return 0

        return 0

def reset_game():
    global brid_x, brid_y, brid_y_change, touch_ground, jump_lock
    global score, pass_score, start_time, game_ending, final_score
    global pipe1, pipe2, pipe3, cactus_list

    brid_x = 100
    brid_y = 220
    brid_y_change = 0
    touch_ground = False
    jump_lock = False

    score = 0
    pass_score = 0
    final_score = 0
    start_time = time.time()
    game_ending = False

    pipe1 = pipe(1200, pipe_y, "pipe1", pipe_w, pipe_h, 10, 1)
    pipe2 = pipe(1600, pipe_y, "pipe2", pipe_w, pipe_h, 10, 1)
    pipe3 = pipe(2000, pipe_y, "pipe3", pipe_w, pipe_h, 10, 1)
    cactus_list = [pipe1, pipe2, pipe3]

pipe1 = pipe(1200, pipe_y, "pipe1", pipe_w, pipe_h, 10, 1)
pipe2 = pipe(1600, pipe_y, "pipe2", pipe_w, pipe_h, 10, 1)
pipe3 = pipe(2000, pipe_y, "pipe3", pipe_w, pipe_h, 10, 1)
cactus_list = [pipe1, pipe2, pipe3]

while not quit_game:

    while game_ending == True:
        score = final_score

        if score > high_score:
            high_score = score
            save_high_score(high_score)

        screen.blit(background, (0, 0))
        show_score(textx, texty)
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

        if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.music.load('wing.wav')
                pygame.mixer.music.play()
                brid_y_change = jump_power
                touch_ground = False
                jump_lock = True

    brid_y += brid_y_change
    brid_y_change += gravity

    if brid_y >= ground_y:
        brid_y = ground_y
        brid_y_change = 0
        touch_ground = True

    if brid_y < 0:
        brid_y = 0
        brid_y_change = 0

    screen.blit(background, (0, 0))

    prip = pygame.Rect(brid_x, brid_y, brid_h, brid_w)
    fakeprip = pygame.image.load("yellowbird-midflap.png").convert_alpha()
    resized_prip = pygame.transform.smoothscale(fakeprip, [brid_h, brid_w])
    screen.blit(resized_prip, prip)

    floor = pygame.Rect(brid_x, brid_y, brid_h, brid_w)
    fakefloor = pygame.image.load("yellowbird-midflap.png").convert_alpha()
    resized_floor = pygame.transform.smoothscale(fakeprip, [brid_h, brid_w])
    screen.blit(resized_prip, prip)

    if brid_y == 472:
            game_ending = True

    for items in cactus_list:
        items.make_food()
        pass_score += items.hit(brid_x, brid_y, brid_w, brid_h)

    score = pass_score

    show_score(textx, texty)
    pygame.display.update()
    clock.tick(FPS)

if score > high_score:
    high_score = score
save_high_score(high_score)

pygame.quit()
quit()