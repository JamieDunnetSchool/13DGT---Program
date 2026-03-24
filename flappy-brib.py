### this program is a flappy brib game for playing

import pygame
import time
import random

pygame.init()  # starts pygame

# Screen and icon set up
screen = pygame.display.set_mode((288, 512))  # creates game window
pygame.display.set_caption("Fabbly- prip")  # window title
game_icon = pygame.image.load("favicon.ico")  # loads icon image
pygame.display.set_icon(game_icon)  # sets icon

#Backround 
background = pygame.image.load("background-day.png").convert()  # loads background image
background = pygame.transform.smoothscale(background, (288, 512))  # resizes background
pygame.key.set_repeat()  # allows holding keys

# colours
green = (188, 227, 199)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (78, 159, 229)
brown = (150, 75, 0)

FPS = 30  # frames per second
quit_game = False  # controls main loop
textX = 10
textY = 10
clock = pygame.time.Clock()  # controls timing

# bird position and size
brid_x = 100
brid_y = 220
brid_w = 30
brid_h = 30

# pipe starting position and size
pipe_x = 1200
pipe_y = -250
pipe_w = 40
pipe_h = 400

# movement variables
llama_x_change = 0
brid_y_change = 0

start_time = time.time()  # start timer for score

ground_y = 512 - brid_h  # ground level

gravity = 1  # gravity pulling bird down
jump_power = -12  # jump strength

# scoring
score = 0
pass_score = 0
final_score = 0

# game states
game_over = False
game_ending = False

font = pygame.font.Font("freesansbold.ttf", 20)  # font for text

# Message settings
def message(msg, txt_colour, bkgd_colour):
    txt = font.render(msg, True, txt_colour, bkgd_colour)  # renders text
    text_box = txt.get_rect(center=(144, 256))  # centers text
    screen.blit(txt, text_box)  # draws text

# Score settings
def show_score(x, y): 
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))  # score text
    hi_text = font.render("High: " + str(high_score), True, (255, 255, 255))  # high score text
    screen.blit(score_text, (x, y))  # draw score
    screen.blit(hi_text, (x, y + 25))  # draw high score

#high score settings
def load_high_score():
    try:
        with open("highsocre.txt", "r") as hi_score_file:  # read file
            value = hi_score_file.read().strip()
    except FileNotFoundError:
        with open("highsocre.txt", "w") as hi_score_file:  # create file if missing
            hi_score_file.write("0")
        value = "0"

    if value == "":
        return 0
    return int(value)

def save_high_score(value):
    with open("highsocre.txt", "w") as hi_score_file:  # save score to file
        hi_score_file.write(str(value))

high_score = load_high_score()  # load high score at start

#Pipe settings
class pipe:
    def __init__(self, pipe_x, pipe_y, name, w, h, speed, points):
        self.pipe_x = pipe_x  # x position
        self.pipe_y = pipe_y  # y position
        self.name = name  # name of pipe
        self.w = w  # width
        self.h = h  # height
        self.speed = speed  # movement speed
        self.points = points  # points given

    def make_food(self):
        pipetu = pygame.Rect(self.pipe_x, self.pipe_y, self.w, self.h)  # pipe hitbox
        pip = pygame.image.load("pipe-green.png").convert_alpha()  # load pipe image
        pipe_flip = pygame.transform.flip(pip, False, True)  # flip pipe
        resized_pipe = pygame.transform.smoothscale(pipe_flip, [self.w, self.h])  # resize
        screen.blit(resized_pipe, pipetu)  # draw pipe

    def hit(self, brid_x, brid_y, brid_w, brid_h):
        global game_ending, final_score, score
        self.pipe_x -= self.speed  # move pipe left

        cactus_rect = pygame.Rect(self.pipe_x, self.pipe_y, self.w, self.h)  # pipe hitbox
        llama_rect = pygame.Rect(brid_x, brid_y, brid_w, brid_h)  # bird hitbox

        if llama_rect.colliderect(cactus_rect):  # collision check
            if game_ending == False:
                final_score = int(time.time() - start_time) + pass_score  # final score
                score = final_score
            game_ending = True  # end game

        if self.pipe_x < -self.w: 
            self.pipe_x = 1000 + random.randint(200, 600)  #Respawn pipe
            pipe_y = self.pipe_y = random.randrange(-300, -100, 40)  # Hight of pipe
            print(self.pipe_y)
            return self.points  # add points
        return 0

def reset_game():
    global brid_x, brid_y, brid_y_change, touch_ground, jump_lock
    global score, pass_score, start_time, game_ending, final_score
    global pipe1, pipe2, pipe3, cactus_list

    brid_x = 100  # reset bird position
    brid_y = 220
    brid_y_change = 0
    touch_ground = False
    jump_lock = False

    score = 0  # reset scores
    pass_score = 0
    final_score = 0
    start_time = time.time()
    game_ending = False

    # recreate pipes
    pipe1 = pipe(1200, pipe_y, "pipe1", pipe_w, pipe_h, 10, 1)
    pipe2 = pipe(1600, pipe_y, "pipe2", pipe_w, pipe_h, 10, 1)
    pipe3 = pipe(2000, pipe_y, "pipe3", pipe_w, pipe_h, 10, 1)
    cactus_list = [pipe1, pipe2, pipe3]

# create pipes
pipe1 = pipe(1200, pipe_y, "pipe1", pipe_w, pipe_h, 10, 1)
pipe2 = pipe(1600, pipe_y, "pipe2", pipe_w, pipe_h, 10, 1)
pipe3 = pipe(2000, pipe_y, "pipe3", pipe_w, pipe_h, 10, 1)
cactus_list = [pipe1, pipe2, pipe3]

# main game loop
while not quit_game:

    # game over screen loop
    while game_ending == True:
        score = final_score
        
        if score > high_score:
            high_score = score
            save_high_score(high_score)
        
        screen.blit(background, (0, 0))  # draw background
        show_score(textX, textY)  # show score
        message("You died! Press X to quit, C to play again", black, white)  # show message
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
                    reset_game()  # restart game
                    break

        clock.tick(FPS)

    # input handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game = True

        if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.music.load('wing.wav')
                pygame.mixer.music.play()
                brid_y_change = jump_power  # jump
                touch_ground = False
                jump_lock = True

    # apply movement
    brid_y += brid_y_change
    brid_y_change += gravity
        
    if brid_y >= ground_y:  # ground collision
        brid_y = ground_y
        brid_y_change = 0
        touch_ground = True

    if brid_y < 0:  # ceiling limit
        brid_y = 0
        brid_y_change = 0
    score = int(time.time() - start_time) + pass_score  # update score

    screen.blit(background, (0, 0))  # draw background
   
    # draw bird
    prip = pygame.Rect(brid_x, brid_y, brid_h, brid_w)
    fakeprip = pygame.image.load("yellowbird-midflap.png").convert_alpha()
    resized_prip = pygame.transform.smoothscale(fakeprip, [brid_h, brid_w])
    screen.blit(resized_prip, prip)

    # (duplicate draw - acts like extra render)
    floor = pygame.Rect(brid_x, brid_y, brid_h, brid_w)
    fakefloor = pygame.image.load("yellowbird-midflap.png").convert_alpha()
    resized_floor = pygame.transform.smoothscale(fakeprip, [brid_h, brid_w])
    screen.blit(resized_prip, prip)

    if brid_y == 472:  # if hits ground
            game_ending = True

    # pipes loop
    for items in cactus_list:
        items.make_food()  # draw pipe
        pass_score += items.hit(brid_x, brid_y, brid_w, brid_h)  # check collision + scoring

    show_score(textX, textY)  # display score
    pygame.display.update()
    clock.tick(FPS)

# save score on exit
score = final_score if game_ending else int(time.time() - start_time) + pass_score
if score > high_score:
    high_score = score
save_high_score(high_score)

pygame.quit()
quit()