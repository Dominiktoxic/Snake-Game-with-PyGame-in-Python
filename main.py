import pygame
import random
import sys
from pygame import Vector2

pygame.init()

class Fruit:

    def __init__(self):
        self.x = random.randint(1, cells - 1)
        self.y = random.randint(1, cells - 1)
        self.pos = Vector2(self.x, self.y)
    
    def spawn_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        pygame.draw.rect(screen, (255, 0, 0), fruit_rect)

class Snake:

    def __init__(self):
        self.body = [Vector2(10, 10), Vector2(10, 9), Vector2(10, 8)]
        self.direction = Vector2(1, 0)
        self.new_block = False
    
    def draw_snake(self):
        for block in self.body:
            x = int(block.x * cell_size)
            y = int(block.y * cell_size)
            pos = Vector2(x, y)

            snake_rect = pygame.Rect(pos.x, pos.y, cell_size - 3, cell_size - 3)
            pygame.draw.rect(screen, SNAKE_COLOUR, snake_rect)
    
    def move(self):
        if self.new_block:
            bodyDuplicate = self.body[:]
            bodyDuplicate.insert(0, bodyDuplicate[0] + self.direction)
            self.body = bodyDuplicate[:]
            self.new_block = False
        else:
            bodyDuplicate = self.body[:-1]
            bodyDuplicate.insert(0, bodyDuplicate[0] + self.direction)
            self.body = bodyDuplicate[:]
    
    def add_block(self):
        self.new_block = True

class Main:

    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
    
    def update(self):
        self.snake.move()
        self.check_collisions()
        self.check_fail()
    
    def spawnFruit(self):
        self.fruit.spawn_fruit()
    
    def spawnSnake(self):
        self.snake.draw_snake()
    
    def check_collisions(self):
        if self.fruit.pos == self.snake.body[0]:
            print("Collision between Fruit and Snake.")
            self.fruit = Fruit()
            self.snake.add_block()
    
    def check_fail(self):
        if not 0 <= self.snake.body[0].x <= cells:
            self.game_over()
        elif not 0 <= self.snake.body[0].y <= cells:
            self.game_over()
        
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
    
    def game_over(self):
        pygame.quit()
        sys.exit()

# Variables
cell_size = 40
cells = 20
WIDTH = cell_size * cells
HEIGHT = cell_size * cells
title = "Snake - A Remake"
FPS = 60
clock = pygame.time.Clock()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(title)

# Colours
BG = (14, 194, 18)
SNAKE_COLOUR = (8, 117, 10)

screen.fill(BG)
main = Main()

while True:
    screen.fill(BG)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == SCREEN_UPDATE:
            main.update()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                main.snake.direction = Vector2(0, -1)
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                main.snake.direction = Vector2(-1, 0)
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                main.snake.direction = Vector2(1, 0)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                main.snake.direction = Vector2(0, 1)
    
    main.spawnFruit()
    main.spawnSnake()

    pygame.display.update()
    clock.tick(FPS)