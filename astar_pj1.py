# importing the necessary modules
import os
import sys
import pygame   # importing the pygame module
import time     # importing the time module
import random   # importing the random module
from pygame import mixer


def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# defining the speed of the snake
speed_of_snake = 10
num_wall = 20
# defining the size of the window
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 460

# defining  the colors
midnight_blue = pygame.Color(25, 25, 112)
mint_cream = pygame.Color(245, 255, 250)
crimson_red = pygame.Color(220, 20, 60)
lawn_green = pygame.Color(124, 252, 0)
orange_red = pygame.Color(255, 69, 0)
wall_color = pygame.Color(0, 0, 0)

# initializing the pygame window using the pygame.init() function
pygame.init()

# using the set_mode() function of the pygame.display module to set the size of the screen
display_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# setting the title of the application using the set_caption() function
pygame.display.set_caption('SNAKE')

# creating an object of the Clock() class of the pygame.time module
game_clock = pygame.time.Clock()

# defining the default position of the snake
position_of_snake = [100, 50]

# defining the first four blocks of snake body
body_of_snake = [
    [100, 50],
    [90, 50],
    [80, 50],
    [70, 50]
]
wall_list = []
# position of the fruit
position_of_fruit = [
    random.randrange(1, (SCREEN_WIDTH//10)) * 10,
    random.randrange(1, (SCREEN_HEIGHT//10)) * 10
]
spawning_of_fruit = True
playing_music = True
music_volume = 0.3
# setting the default direction of the snake towards RIGHT
initial_direction = 'RIGHT'
snake_direction = initial_direction

# initial score
player_score = 0
# bg music
bg_music_path = resource_path("background.mp3")

# random wall function


def random_wall():
    wall_list.clear()
    for i in range(num_wall):
        x = random.randrange(1, (SCREEN_WIDTH//10)) * 10
        y = random.randrange(1, (SCREEN_HEIGHT//10)) * 10
        while [x, y] in body_of_snake or [x, y] in wall_list or (x, y) == tuple(position_of_fruit) or euclideanDistance(x, position_of_fruit[0], y, position_of_fruit[1]) <= 1800:
            x = random.randrange(1, (SCREEN_WIDTH//10)) * 10
            y = random.randrange(1, (SCREEN_HEIGHT//10)) * 10
        wall_list.append([x, y])


def text_objects(text, font):
    text_surface = font.render(text, True, pygame.Color(219, 129, 252))
    return text_surface, text_surface.get_rect()


def display_button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(display_screen, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(display_screen, ic, (x, y, w, h))

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    display_screen.blit(textSurf, textRect)


def display_score(selection, font_color, font_style, font_size):

    # creating the font object
    score_font_style = pygame.font.SysFont(font_style, font_size)

    # creating the display surface object
    score_surface = score_font_style.render(
        f'Your Score : {str(player_score)}', True, font_color
    )

    # creating a rectangular object for the text placement
    score_rectangle = score_surface.get_rect()

    # displaying the text
    display_screen.blit(score_surface, score_rectangle)

# function to over the game


def game_over():

    # creating the font object
    game_over_font_style = pygame.font.SysFont('times new roman', 50)

    # creating the display surface object
    game_over_surface = game_over_font_style.render(
        f'Your Score is : {str(player_score)}', True, crimson_red
    )

    # creating a rectangular object for the text placement
    game_over_rectangle = game_over_surface.get_rect()

    # setting the position of the text
    game_over_rectangle.midtop = (SCREEN_WIDTH/2, SCREEN_HEIGHT/4)

    # displaying the text on the screen
    display_screen.blit(game_over_surface, game_over_rectangle)

    # using the flip() function to update the small portion of the screen
    pygame.display.flip()

    # suspending the execution of the current thread for 2 seconds
    time.sleep(2)

    # calling the quit() function
    pygame.quit()

    # quiting the application
    sys.exit()


def get_neighbor(current, direct):
    neighs = []
    up = [current[0], current[1] - 10]
    down = [current[0], current[1] + 10]
    left = [current[0] - 10, current[1]]
    right = [current[0] + 10, current[1]]
    neighs += [up] if direct != "DOWN" else []
    neighs += [down] if direct != "UP" else []
    neighs += [left] if direct != "RIGHT" else []
    neighs += [right] if direct != "LEFT" else []
    return tuple(tuple(inner) for inner in neighs)


def euclideanDistance(x1, x2, y1, y2):
    return (x1-x2)*(x1-x2) + (y1-y2)*(y1-y2)


def manhattanDistance(x1, x2, y1, y2):
    return abs(x1-x2) + abs(y1 - y2)


def chebyshevDistance(x1, x2, y1, y2):
    return max(abs(x1-x2), abs(y1 - y2))


def getpath_Astar(food1, snake1, h_func):
    direct = initial_direction
    snake1 = tuple(tuple(inner) for inner in snake1)
    openset = [snake1[0]]
    f = {snake1[0]: 0}
    g = {snake1[0]: 0}
    closedset = []
    dir_array1 = []
    parent = {snake1[0]: False}
    while openset:
        current1 = min(openset, key=lambda x: f[x])
        openset = [openset[i]
                   for i in range(len(openset)) if openset[i] != current1]
        closedset.append(current1)
        # update direct
        if parent[current1]:
            if current1[0] == parent[current1][0] and current1[1] < parent[current1][1]:
                direct = "UP"
            elif current1[0] == parent[current1][0] and current1[1] > parent[current1][1]:
                direct = "DOWN"
            elif current1[0] < parent[current1][0] and current1[1] == parent[current1][1]:
                direct = "LEFT"
            elif current1[0] > parent[current1][0] and current1[1] == parent[current1][1]:
                direct = "RIGHT"
        for neighbor in get_neighbor(current1, direct):
            if neighbor[0] < 0 or neighbor[0] > SCREEN_WIDTH - 10 or neighbor[1] < 0 or neighbor[1] > SCREEN_HEIGHT - 10:
                continue
            if neighbor not in closedset and list(neighbor) not in tuple(body_of_snake) and list(neighbor) not in tuple(wall_list):
                tempg = g[current1] + 10
                if neighbor in openset:
                    if tempg < g[neighbor]:
                        g[neighbor] = tempg
                else:
                    g[neighbor] = tempg
                    openset.append(neighbor)
                h_neighbor = h_func(
                    neighbor[0], food1[0], neighbor[1], food1[1])
                f[neighbor] = g[neighbor] + h_neighbor
                parent[neighbor] = current1
        if current1[0] == food1[0] and current1[1] == food1[1]:
            break

    if not parent[current1]:
        # No valid path found
        return []
    while parent[current1]:
        if current1[0] == parent[current1][0] and current1[1] < parent[current1][1]:
            dir_array1.append("UP")
        elif current1[0] == parent[current1][0] and current1[1] > parent[current1][1]:
            dir_array1.append("DOWN")
        elif current1[0] < parent[current1][0] and current1[1] == parent[current1][1]:
            dir_array1.append("LEFT")
        elif current1[0] > parent[current1][0] and current1[1] == parent[current1][1]:
            dir_array1.append("RIGHT")
        current1 = parent[current1]
    # print(dir_array1)
    dir_array1.reverse()
    return dir_array1


def game_loop_player():
    global initial_direction, snake_direction, player_score, spawning_of_fruit, num_wall, \
        position_of_fruit, body_of_snake, position_of_snake, wall_list, speed_of_snake, playing_music
    if playing_music:
        mixer.music.load(bg_music_path)
        mixer.music.set_volume(music_volume)
        mixer.music.play(-1)
    while True:
        random_wall()
        path = getpath_Astar(
            position_of_fruit, body_of_snake, euclideanDistance)
        if (len(path) > 0):
            break
    # setting the run flag value to True
    game_run = True
    wait_key_flag = True
    # the game loop
    # using the while loop
    while game_run:
        # iterating through the events in the pygame.event module
        for event in pygame.event.get():
            # setting the variable value to False if the event's type is equivalent to pygame's QUIT constant
            if event.type == pygame.QUIT:
                # setting the flag value to False
                game_run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    snake_direction = 'UP'
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    snake_direction = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    snake_direction = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    snake_direction = 'RIGHT'
                if event.key == pygame.K_ESCAPE:
                    game_over()
                if event.key == pygame.K_p and playing_music:
                    mixer.music.pause()
                    playing_music = False
                elif event.key == pygame.K_p and not playing_music:
                    mixer.music.unpause()
                    playing_music = True
        # neglecting the action taken if the key of opposite direction is pressed
        if snake_direction == 'UP' and initial_direction != 'DOWN':
            initial_direction = 'UP'
        if snake_direction == 'DOWN' and initial_direction != 'UP':
            initial_direction = 'DOWN'
        if snake_direction == 'LEFT' and initial_direction != 'RIGHT':
            initial_direction = 'LEFT'
        if snake_direction == 'RIGHT' and initial_direction != 'LEFT':
            initial_direction = 'RIGHT'

        # updating the position of the snake for every direction
        if initial_direction == 'UP':
            position_of_snake[1] -= 10
        if initial_direction == 'DOWN':
            position_of_snake[1] += 10
        if initial_direction == 'LEFT':
            position_of_snake[0] -= 10
        if initial_direction == 'RIGHT':
            position_of_snake[0] += 10
        # updating the body of the snake
        body_of_snake.insert(0, list(position_of_snake))
        if position_of_snake[0] == position_of_fruit[0] and position_of_snake[1] == position_of_fruit[1]:
            # incrementing the player's score by 1
            player_score += 1
            num_wall += 15 if player_score % 10 == 0 else 0
            spawning_of_fruit = False
            speed_of_snake += 1 if player_score % 5 == 0 else 0
            # wait key to continue when get 10 points
            wait_key_flag = True if player_score % 10 == 0 else False
            # print(path)
        else:
            body_of_snake.pop()

        # randomly spawning the fruit
        while (not spawning_of_fruit):
            position_of_fruit = [
                random.randrange(1, (SCREEN_WIDTH//10)) * 10,
                random.randrange(1, (SCREEN_HEIGHT//10)) * 10
            ]
            if player_score % 10 == 0:
                while True:
                    random_wall()
                    path = getpath_Astar(
                        position_of_fruit, body_of_snake, euclideanDistance)
                    if (len(path) > 0):
                        break
            if position_of_fruit in body_of_snake or position_of_fruit in wall_list:
                continue
            break
        # randomly spawning the wall

        spawning_of_fruit = True

        # filling the color on the screen
        display_screen.fill(mint_cream)

        # drawing the game objects on the screen
        pygame.draw.rect(display_screen, midnight_blue,
                         pygame.Rect(body_of_snake[0][0], body_of_snake[0][1], 10, 10))
        for position in body_of_snake[1:]:
            pygame.draw.rect(display_screen, lawn_green,
                             pygame.Rect(position[0], position[1], 10, 10))
            pygame.draw.rect(display_screen, orange_red, pygame.Rect(
                position_of_fruit[0], position_of_fruit[1], 10, 10))
        for position in wall_list:
            pygame.draw.rect(display_screen, wall_color,
                             pygame.Rect(position[0], position[1], 10, 10))

        # conditions for the game to over
        if position_of_snake[0] < 0 or position_of_snake[0] > SCREEN_WIDTH - 10:
            game_over()
        if position_of_snake[1] < 0 or position_of_snake[1] > SCREEN_HEIGHT - 10:
            game_over()

        # touching the snake body
        for block in body_of_snake[1:]:
            if position_of_snake[0] == block[0] and position_of_snake[1] == block[1]:
                game_over()
        # touching the wall
        for block in wall_list:
            if position_of_snake[0] == block[0] and position_of_snake[1] == block[1]:
                game_over()
        # displaying the score continuously
        display_score(1, midnight_blue, 'times new roman', 20)

        if wait_key_flag:
            pygame.display.update()
            smallText = pygame.font.SysFont("times new roman", 24)
            msg = "You get 10 points, press SPACE key to continue!" if player_score != 0 else "press SPACE key to start game!"
            textSurf, textRect = text_objects(
                msg, smallText)
            textRect.center = ((SCREEN_WIDTH/2), (SCREEN_HEIGHT/2))
            display_screen.blit(textSurf, textRect)
            pygame.display.update()
            wait_key = True
            while wait_key:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        wait_key = False
                        wait_key_flag = False
                game_clock.tick(speed_of_snake)

        # refreshing the game screen
        pygame.display.update()

        # refresh rate
        game_clock.tick(speed_of_snake)


def game_loop_bot():

    global initial_direction, snake_direction, player_score, spawning_of_fruit, num_wall, \
        position_of_fruit, body_of_snake, position_of_snake, wall_list, speed_of_snake, playing_music
    if playing_music:
        mixer.music.load(bg_music_path)
        mixer.music.set_volume(music_volume)
        mixer.music.play(-1)
    while True:
        random_wall()
        path = getpath_Astar(
            position_of_fruit, body_of_snake, euclideanDistance)
        if (len(path) > 0):
            break
    # setting the run flag value to True
    game_run = True
    # the game loop
    # using the while loop
    while game_run:
        # iterating through the events in the pygame.event module
        for event in pygame.event.get():
            # setting the variable value to False if the event's type is equivalent to pygame's QUIT constant
            if event.type == pygame.QUIT:
                # setting the flag value to False
                game_run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over()
                if event.key == pygame.K_p and playing_music:
                    mixer.music.pause()
                    playing_music = False
                elif event.key == pygame.K_p and not playing_music:
                    mixer.music.unpause()
                    playing_music = True
        path = getpath_Astar(
            position_of_fruit, body_of_snake, euclideanDistance)
        snake_direction = path.pop(0) if len(path) > 0 else snake_direction

        # neglecting the action taken if the key of opposite direction is pressed
        if snake_direction == 'UP' and initial_direction != 'DOWN':
            initial_direction = 'UP'
        if snake_direction == 'DOWN' and initial_direction != 'UP':
            initial_direction = 'DOWN'
        if snake_direction == 'LEFT' and initial_direction != 'RIGHT':
            initial_direction = 'LEFT'
        if snake_direction == 'RIGHT' and initial_direction != 'LEFT':
            initial_direction = 'RIGHT'

        # updating the position of the snake for every direction
        if initial_direction == 'UP':
            position_of_snake[1] -= 10
        if initial_direction == 'DOWN':
            position_of_snake[1] += 10
        if initial_direction == 'LEFT':
            position_of_snake[0] -= 10
        if initial_direction == 'RIGHT':
            position_of_snake[0] += 10
        # updating the body of the snake
        body_of_snake.insert(0, list(position_of_snake))
        if position_of_snake[0] == position_of_fruit[0] and position_of_snake[1] == position_of_fruit[1]:
            # incrementing the player's score by 1
            player_score += 1
            num_wall += 10 if player_score % 10 == 0 else 0
            spawning_of_fruit = False
            speed_of_snake += 2 if player_score % 5 == 0 else 0
            # print(path)
        else:
            body_of_snake.pop()

        # randomly spawning the fruit
        while (not spawning_of_fruit):
            position_of_fruit = [
                random.randrange(1, (SCREEN_WIDTH//10)) * 10,
                random.randrange(1, (SCREEN_HEIGHT//10)) * 10
            ]
            if player_score % 10 == 0:
                while True:
                    random_wall()
                    path = getpath_Astar(
                        position_of_fruit, body_of_snake, euclideanDistance)
                    if (len(path) > 0):
                        break
            if position_of_fruit in body_of_snake or position_of_fruit in wall_list:
                continue
            break
        # randomly spawning the wall

        spawning_of_fruit = True

        # filling the color on the screen
        display_screen.fill(mint_cream)

        # drawing the game objects on the screen
        pygame.draw.rect(display_screen, midnight_blue,
                         pygame.Rect(body_of_snake[0][0], body_of_snake[0][1], 10, 10))
        for position in body_of_snake[1:]:
            pygame.draw.rect(display_screen, lawn_green,
                             pygame.Rect(position[0], position[1], 10, 10))
            pygame.draw.rect(display_screen, orange_red, pygame.Rect(
                position_of_fruit[0], position_of_fruit[1], 10, 10))
        for position in wall_list:
            pygame.draw.rect(display_screen, wall_color,
                             pygame.Rect(position[0], position[1], 10, 10))

        # conditions for the game to over
        if position_of_snake[0] < 0 or position_of_snake[0] > SCREEN_WIDTH - 10:
            game_over()
        if position_of_snake[1] < 0 or position_of_snake[1] > SCREEN_HEIGHT - 10:
            game_over()

        # touching the snake body
        for block in body_of_snake[1:]:
            if position_of_snake[0] == block[0] and position_of_snake[1] == block[1]:
                game_over()
        # touching the wall
        for block in wall_list:
            if position_of_snake[0] == block[0] and position_of_snake[1] == block[1]:
                game_over()
        # displaying the score continuously
        display_score(1, midnight_blue, 'times new roman', 20)

        # refreshing the game screen
        pygame.display.update()

        # refresh rate
        game_clock.tick(speed_of_snake)


def start_game():
    global playing_music
    mixer.init()
    mixer.music.load(bg_music_path)
    mixer.music.set_volume(music_volume)
    mixer.music.play(-1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and playing_music:
                    mixer.music.pause()
                    playing_music = False
                elif event.key == pygame.K_p and not playing_music:
                    mixer.music.unpause()
                    playing_music = True
        # Fill the screen and add title
        display_screen.fill(mint_cream)
        largeText = pygame.font.Font('freesansbold.ttf', 30)
        TextSurf, TextRect = text_objects("Snake Game", largeText)
        TextRect.center = ((SCREEN_WIDTH/2), (SCREEN_HEIGHT/2 - 50))
        display_screen.blit(TextSurf, TextRect)
        smallText = pygame.font.SysFont("times new roman", 16)
        textSurf, textRect = text_objects(
            "use WASD or ARROW button to navigate the snake", smallText)
        textRect.center = ((SCREEN_WIDTH - 180), (SCREEN_HEIGHT - 40))
        display_screen.blit(textSurf, textRect)
        smallText = pygame.font.SysFont("times new roman", 16)
        textSurf, textRect = text_objects(
            "press ESC to exit, press P to pause/unpause music", smallText)
        textRect.center = ((SCREEN_WIDTH - 170), (SCREEN_HEIGHT - 20))
        display_screen.blit(textSurf, textRect)
        # Draw button
        display_button("Start(player)", 270, 250, 160, 50,
                       lawn_green, midnight_blue, game_loop_player)
        display_button("Start(bot)", 270, 310, 160, 50,
                       lawn_green, midnight_blue, game_loop_bot)
        pygame.display.update()
        game_clock.tick(speed_of_snake)


# calling the start_game() function to start the game
start_game()


# calling the quit() function to quit the application
pygame.quit()
