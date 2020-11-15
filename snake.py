from enum import Enum
import pygame
import sys
import random

size = width, height = (500, 500)
screen = pygame.display.set_mode(size)

# Colors
class Color(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

class SnakeGame():

    def __init__(self, init_score=0, init_length=10, init_color=Color.WHITE.value):
        self.score = init_score
        self.snake = []
        self.colors = []
        self.INIT_LENGTH = init_length
        self.INIT_COLOR = init_color
        self.UNIT = 10
        self.FPS = 16

    def snake_length(self):
        return len(self.snake)

    def random_color(self):
        return (random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255))

    def new_food_coords(self): 
        x = random.randint(0, (width - self.UNIT) / self.UNIT) * self.UNIT
        y = random.randint(0, (height - self.UNIT) / self.UNIT) * self.UNIT
        return x, y

    def text_objects(self, text, font):
        text_surface = font.render(text, True, Color.WHITE.value)
        return text_surface, text_surface.get_rect()

    def update_scoreboard(self):
        score_font = pygame.font.Font(None, 50)
        text_surf, text_rect = self.text_objects(str(self.score), score_font)
        text_rect.center = (width - 20, height - 30)
        screen.blit(text_surf, text_rect)

    def play(self):
        running = True
        score = 0
        color = self.INIT_COLOR
        food_color = self.random_color()
        pygame.init()
        clock = pygame.time.Clock()
        head_x = 350
        head_y = 250
        speed_x= self.UNIT
        speed_y = 0
        x, y = head_x, head_y

        # Start the scoreboard
        self.update_scoreboard()

        # Start the snake
        self.snake.append((head_x, head_y))
        self.colors.append(self.INIT_COLOR)
        for i in range(1, self.INIT_LENGTH):
            self.snake.append((self.snake[i - 1][0] - self.UNIT, head_y))
            self.colors.append(self.INIT_COLOR)

        # Drop the first food
        food_x, food_y = self.new_food_coords()
        food_color = self.random_color()

        # Game loop
        while running:
            screen.fill(Color.BLACK.value)

            # Draw head
            head = pygame.draw.rect(screen, color, [self.snake[0][0], self.snake[0][1], self.UNIT, self.UNIT])

            # Draw body, based on location of head
            for seg in range(1, len(self.snake) - 2):
                pygame.draw.rect(screen, self.colors[seg], [self.snake[seg][0], self.snake[seg][1], self.UNIT, self.UNIT])

            # Draw food
            pygame.draw.rect(screen, food_color, [food_x, food_y, self.UNIT, self.UNIT])

            # Controls (pygame events)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and speed_y == 0:
                        speed_x = 0
                        speed_y = -self.UNIT
                    if event.key == pygame.K_DOWN and speed_y == 0:
                        speed_x = 0
                        speed_y = self.UNIT
                    if event.key == pygame.K_LEFT and speed_x == 0:
                        speed_x = -self.UNIT
                        speed_y = 0
                    if event.key == pygame.K_RIGHT and speed_x == 0:
                        speed_x = self.UNIT
                        speed_y = 0
                    if event.key == pygame.K_ESCAPE:
                        running = False

            # Update head coords (and save old)
            head_x += speed_x
            head_y += speed_y
            head = head.move(head_x, head_y)
            r,g,b = color
            for i in range(self.snake_length() - 1, 0, -1):
                self.snake[i] = self.snake[i - 1]
                self.colors[i] = self.colors[i - 1]
            self.snake[0] = (head_x, head_y)
            self.colors[0] = color

            # Looping bounds
            if head_x < 0:
                head_x = width - self.UNIT
            if head_y < 0:
                head_y = height - self.UNIT
            if head_x >= width:
                head_x = 0
            if head_y >= height:
                head_y = 0
            
            # Check if snake is hitting self
            if (head_x, head_y) in self.snake[1:]:
                print("You lose.")
                running = False

            # Check if food is being eaten
            if (head_x, head_y) == (food_x, food_y):
                self.score += 1
                self.update_scoreboard()
                print("Score: " + str(self.score))
                food_x, food_y = self.new_food_coords()
                color = food_color
                food_color = self.random_color()
                print("New food at " + str((food_x, food_y)))
                last_x, last_y = self.snake[self.snake_length() - 1]
                if speed_y > 0:
                    seg = (last_x, last_y - self.UNIT)
                if speed_y < 0:
                    seg = (last_x, last_y + self.UNIT)
                if speed_x > 0:
                    seg = (last_x - self.UNIT, last_y)
                if speed_x < 0:
                    seg = (last_x + self.UNIT, last_y)
                self.snake.append(seg)
                self.colors.append(self.INIT_COLOR)

            # Update screen
            self.update_scoreboard()
            pygame.display.flip()
            clock.tick(self.FPS)

if __name__ == '__main__':
    game = SnakeGame()
    game.play()
