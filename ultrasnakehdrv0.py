import pygame
import random
from array import array
import math
import time

# Initialize Pygame and its mixer
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Screen setup
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Enhanced Snake Game with Sound")

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# Game settings
block_size = 20
initial_snake_speed = 15
max_speed = 30

# Initialize fonts
font_style = pygame.font.SysFont(None, 50)
font_style_small = pygame.font.SysFont(None, 30)

# Sound generation function
def generate_beep_sound(frequency=440, duration=0.1):
    sample_rate = pygame.mixer.get_init()[0]
    max_amplitude = 2 ** (abs(pygame.mixer.get_init()[1]) - 1) - 1
    samples = int(sample_rate * duration)
    wave = [int(max_amplitude * math.sin(2 * math.pi * frequency * i / sample_rate)) for i in range(samples)]
    sound = pygame.mixer.Sound(buffer=array('h', wave))
    sound.set_volume(0.1)
    return sound

# Sound effects
eat_sound = generate_beep_sound(523.25, 0.1)
game_over_sound = generate_beep_sound(200, 0.5)

# Initial prompt screen
def initial_prompt():
    screen.fill(black)
    prompt_msg = font_style_small.render('Press Z or Enter to Start', True, white)
    screen.blit(prompt_msg, [width // 2 - prompt_msg.get_width() // 2, height // 2 - prompt_msg.get_height() // 2])
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_z or event.key == pygame.K_RETURN):
                waiting = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()

# Loading screen
def loading_screen():
    screen.fill(black)
    for i in range(100):
        screen.fill(black)
        loading_msg = font_style.render(f'Loading {"." * (i % 4)}', True, white)
        screen.blit(loading_msg, [width // 2 - loading_msg.get_width() // 2, height // 2 - loading_msg.get_height() // 2])
        pygame.display.update()
        time.sleep(0.05)

# Function to display the score
def display_score(score):
    value = font_style.render("Your Score: " + str(score), True, white)
    screen.blit(value, [0, 0])

# Function to draw the snake
def draw_snake(snake_block, snake_list):
    for x, y in snake_list:
        pygame.draw.rect(screen, green, [x, y, snake_block, snake_block])

# Function to display credits
def display_credits():
    screen.fill(black)
    credits_text = [
        "CREDIT TO NOKIA",
        "and OPENAI",
        "[C] Flames AI 2024",
    ]

    for i, line in enumerate(credits_text):
        message = font_style.render(line, True, white)
        screen.blit(message, [width // 2 - message.get_width() // 2, 200 + i * 50])
    
    pygame.display.update()
    time.sleep(5)  # Display the credits for 5 seconds before exiting or waiting for a key press

    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                waiting_for_key = False

# Function to display the game over screen
def display_game_over():
    game_over_sound.play()
    msg = font_style.render('Game Over', True, red)
    screen.blit(msg, [width / 2 - msg.get_width() // 2, height / 2 - 80])
    restart_msg = font_style_small.render('Press Y to restart, N to quit', True, white)
    screen.blit(restart_msg, [width / 2 - restart_msg.get_width() // 2, height / 2 + 20])
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    game_loop()
                elif event.key == pygame.K_n:
                    display_credits()
                    pygame.quit()
                    quit()

# Main game loop
def game_loop():
    snake_x = width / 2
    snake_y = height / 2
    snake_x_change = 0
    snake_y_change = 0

    snake_list = []
    snake_length = 1

    food_x = round(random.randrange(0, width - block_size) / block_size) * block_size
    food_y = round(random.randrange(0, height - block_size) / block_size) * block_size

    snake_speed = initial_snake_speed
    clock = pygame.time.Clock()

    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT and snake_x_change == 0):
                    snake_x_change = -block_size
                    snake_y_change = 0
                elif (event.key == pygame.K_RIGHT and snake_x_change == 0):
                    snake_x_change = block_size
                    snake_y_change = 0
                elif (event.key == pygame.K_UP and snake_y_change == 0):
                    snake_y_change = -block_size
                    snake_x_change = 0
                elif (event.key == pygame.K_DOWN and snake_y_change == 0):
                    snake_y_change = block_size
                    snake_x_change = 0

        # Update snake position
        snake_x += snake_x_change
        snake_y += snake_y_change

        # End game if snake hits the boundaries
        if snake_x >= width or snake_x < 0 or snake_y >= height or snake_y < 0:
            display_game_over()

        screen.fill(black)
        pygame.draw.rect(screen, red, [food_x, food_y, block_size, block_size])

        snake_head = [snake_x, snake_y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # End game if snake collides with itself
        for segment in snake_list[:-1]:
            if segment == snake_head:
                display_game_over()

        draw_snake(block_size, snake_list)
        display_score(snake_length - 1)

        pygame.display.update()

        # Check if the snake has eaten the food
        if snake_x == food_x and snake_y == food_y:
            eat_sound.play()
            food_x = round(random.randrange(0, width - block_size) / block_size) * block_size
            food_y = round(random.randrange(0, height - block_size) / block_size) * block_size
            snake_length += 1
            snake_speed = min(snake_speed + 1, max_speed)

        clock.tick(snake_speed)

# Start sequence
initial_prompt()
loading_screen()
game_loop()

pygame.quit()
