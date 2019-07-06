import pygame
import sys
import random

size = width, height = (500, 500)
screen = pygame.display.set_mode(size)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game constants
unit = 10
speed_list = [unit, unit]
FPS = 16

# Snake
snake = []
colors = []
length = len(snake)
init_length = 10
init_color = WHITE

# Food
food_coords = food_x, food_y = (0, 0) 

def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r,g,b)

def new_food_coords(): 
    food_x = random.randint(0, (width - unit) / unit) * unit
    food_y = random.randint(0, (height - unit) / unit) * unit
    return food_x, food_y

def text_objects(text, font):
    text_surface = font.render(text, True, WHITE)
    return text_surface, text_surface.get_rect()

def show_score(score):
    score_font = pygame.font.Font(None, 50)
    TextSurf, TextRect = text_objects(str(score), score_font)
    TextRect.center = (width - 20, height - 30)
    screen.blit(TextSurf, TextRect)

def main():
    running = True
    score = 0
    color = init_color
    food_color = random_color()
    pygame.init()
    clock = pygame.time.Clock()
    head_x = 350
    head_y = 250
    old_head_x, old_head_y = head_x, head_y
    speed_x= unit
    speed_y = 0
    x, y = head_x, head_y

    show_score(0)

    # Initialize snake
    snake.append((head_x, head_y))
    colors.append(init_color)
    for i in range(1, init_length):
        snake.append((snake[i - 1][0] - unit, head_y))
        colors.append(init_color)

    # Initialize food
    food_x, food_y = new_food_coords()
    food_color = random_color()

    # Game loop
    while running:
        screen.fill(BLACK)

        # Draw head
        head = pygame.draw.rect(screen, color, [snake[0][0], snake[0][1], unit, unit])

        # Draw body, based on location of head
        for seg in range(1, len(snake) - 2):
            pygame.draw.rect(screen, colors[seg], [snake[seg][0], snake[seg][1], unit, unit])

        # Draw food
        food = pygame.draw.rect(screen, food_color, [food_x, food_y, unit, unit])

        # Controls (pygame events)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and speed_y == 0:
                    speed_x = 0
                    speed_y = -unit
                if event.key == pygame.K_DOWN and speed_y == 0:
                    speed_x = 0
                    speed_y = unit
                if event.key == pygame.K_LEFT and speed_x == 0:
                    speed_x = -unit
                    speed_y = 0
                if event.key == pygame.K_RIGHT and speed_x == 0:
                    speed_x = unit
                    speed_y = 0
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Update head coords (and save old)
        old_head_x = head_x
        old_head_y = head_y
        head_x += speed_x
        head_y += speed_y
        head = head.move(head_x, head_y)
        r,g,b = color
        for i in range(len(snake) - 1, 0, -1):
            snake[i] = snake[i - 1]
            colors[i] = colors[i - 1]
        snake[0] = (head_x, head_y)
        colors[0] = color

        # Looping bounds
        if head_x < 0:
            head_x = width - unit
        if head_y < 0:
            head_y = height - unit
        if head_x >= width:
            head_x = 0
        if head_y >= height:
            head_y = 0
        
        # Check if snake is hitting self
        if (head_x, head_y) in snake[1:]:
            print("You lose.")
            running = False

        # Check if food is being eaten
        if (head_x, head_y) == (food_x, food_y):
            score += 1
            show_score(score)
            print("Score: " + str(score))
            food_x, food_y = new_food_coords()
            color = food_color
            food_color = random_color()
            print("New food at " + str((food_x, food_y)))
            last_seg = last_x, last_y = snake[len(snake) - 1]
            if speed_y > 0:
                seg = (last_x, last_y - unit)
            if speed_y < 0:
                seg = (last_x, last_y + unit)
            if speed_x > 0:
                seg = (last_x - unit, last_y)
            if speed_x < 0:
                seg = (last_x + unit, last_y)
            snake.append(seg)
            colors.append(init_color)

        # Update screen
        show_score(score)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
