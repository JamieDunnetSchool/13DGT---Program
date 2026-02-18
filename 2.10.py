import pygame
import random
import time
pygame.init()

screen = pygame.display.set_mode((1000, 720))
game_icon = pygame.image.load('snake_icon.png')
pygame.display.set_icon(game_icon)
pygame.display.set_caption("Snake Game by Me")

green = (188, 227, 199)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
text_colour = (0, 0, 0)
score = 0
size_snake1 = 20
size_snake2 = 20
quit_game = False
game_ending = False

clock = pygame.time.Clock()
snake_x = 500
snake_y = 360
snake_x_change = 0
snake_y_change = 0
snake_list = []
snake_length = 1
textX = 750
textY = 10

food_x = round(random.randrange(20, 1000 - 20) / 20) * 20
food_y = round(random.randrange(20, 720  - 20) / 20) * 20

font = pygame.font.Font("freesansbold.ttf", 50)

def message(msg, txt_colour, bkgd_colour):
    txt = font.render(msg, True, txt_colour, bkgd_colour)
    text_box = txt.get_rect(center=(500, 360))
    screen.blit(txt, text_box)

def draw_snake(snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, red, [x[0], x[1], 20 , 20])

def load_high_score():
    try:
        with open("HI_score.txt", "r") as hi_score_file:
            value = hi_score_file.read().strip()
            if value == "":
                return 0
            return int(value)
    except:
        # if file doesn't exist, create it with 0
        with open("HI_score.txt", "w") as hi_score_file:
            hi_score_file.write("0")
        return 0

def save_high_score(value):
    with open("HI_score.txt", "w") as hi_score_file:
        hi_score_file.write(str(value))

# ---- High score setup ----
high_score = load_high_score()

def show_scores(x, y):
    # Display both current score and high score
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    hi_text = font.render("High: " + str(high_score), True, (255, 255, 255))
    screen.blit(score_text, (x, y))
    screen.blit(hi_text, (x, y + 55))  # place high score under score

while not quit_game:

    while game_ending == True:
        screen.fill(green)
        message("You died! Press X to quit, C to play again", black, white)
        show_scores(textX, textY)
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
                    snake_length = 1
                    score = 0
                    snake_x = 500
                    snake_y = 360
                    snake_x_change = 0
                    snake_y_change = 0
                    snake_list = []
                    food_x = round(random.randrange(20, 1000 - 20) / 20) * 20
                    food_y = round(random.randrange(20, 720  - 20) / 20) * 20
                    game_ending = False
                    break

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

    snake_x += snake_x_change
    snake_y += snake_y_change

    if snake_x == food_x and snake_y == food_y:
        food_x = round(random.randrange(20, 1000 - 20) / 20) * 20
        food_y = round(random.randrange(20, 720  - 20) / 20) * 20
        score += 1
        snake_length += 1

        # ---- Update high score in-game ----
        if score > high_score:
            high_score = score

    screen.fill(green)

    if snake_x >= 1000 or snake_x < 0 or snake_y >= 720 or snake_y < 0:
        game_ending = True

    food = pygame.Rect(food_x, food_y, 20, 20)
    apple = pygame.image.load('apple_3.png').convert_alpha()
    resized_apple = pygame.transform.smoothscale(apple, [20,20])
    screen.blit(resized_apple, food)

    snake_head = []
    snake_head.append(snake_x)
    snake_head.append(snake_y)
    snake_list.append(snake_head)

    if len(snake_list) > snake_length:
        del snake_list[0]

    for x in snake_list[:-1]:
        if x == snake_head:
            game_ending = True

    draw_snake(snake_list)

    # ---- Display both scores ----
    show_scores(textX, textY)

    pygame.display.update()
    clock.tick(10)

# ---- Save high score when program closes ----
save_high_score(high_score)

pygame.quit()
quit()