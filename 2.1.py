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

def show_score(x, y):
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (x, y))

def draw_snake(snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, red, [x[0], x[1], 20 , 20])

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

    snake_x += snake_x_change
    snake_y += snake_y_change

    if snake_x == food_x and snake_y == food_y:
        food_x = round(random.randrange(20, 1000 - 20) / 20) * 20
        food_y = round(random.randrange(20, 720  - 20) / 20) * 20
        score += 1
        snake_length += 1

    if snake_x >= 1000 or snake_x < 0 or snake_y >= 720 or snake_y < 0:
        screen.fill(green)
        message("You died!", black, white)
        pygame.display.update()
        time.sleep(3)
        quit_game = True
        continue

    screen.fill(green)

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
            screen.fill(green)
            message("You died!", black, white)
            pygame.display.update()
            time.sleep(3)
            quit_game = True

    draw_snake(snake_list)
    show_score(textX, textY)

    pygame.display.update()
    clock.tick(10)

pygame.quit()
quit()