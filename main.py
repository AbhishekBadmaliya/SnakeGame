import pygame
from pygame import font
from pygame.constants import KEYDOWN
from pygame.math import Vector2
import sys
import random

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(0,0)
        self.new_block = False

        self.head_up = pygame.image.load('imgs/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('imgs/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('imgs/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('imgs/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('imgs/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('imgs/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('imgs/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('imgs/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('imgs/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('imgs/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('imgs/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('imgs/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('imgs/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('imgs/body_bl.png').convert_alpha()

        self.game_sound = pygame.mixer.Sound('audio/sound.wav')

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        
        for index,block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rectangle = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            
            if index == 0:
                screen.blit(self.head, block_rectangle)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rectangle)
            else:
                prev_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if prev_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rectangle)
                elif prev_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rectangle)
                else:
                    if prev_block.x == -1 and next_block.y == -1 or prev_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rectangle)
                    elif prev_block.x == -1 and next_block.y == 1 or prev_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rectangle)
                    elif prev_block.x == 1 and next_block.y == -1 or prev_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rectangle)
                    elif prev_block.x == 1 and next_block.y == 1 or prev_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rectangle)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0):
            self.head = self.head_left
        elif head_relation == Vector2(-1,0):
            self.head = self.head_right
        elif head_relation == Vector2(0,1):
            self.head = self.head_up
        elif head_relation == Vector2(0,-1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0,1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1):
            self.tail = self.tail_down

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
    
    def add_block(self):
        self.new_block = True

    def play_sound(self):
        self.game_sound.play()
        
    def reset(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(0,0)

class FRUIT:
    def __init__(self):
        self.randomize()
        
    # draw the fruit at random position
    def draw_fruit(self):
        fruit_rectangle = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size),cell_size,cell_size)
        screen.blit(apple,fruit_rectangle)
        
    # get random position
    def randomize(self):
        self.x = random.randint(0,cell_numberX - 1)
        self.y = random.randint(0,cell_numberY - 1)
        self.pos = Vector2(self.x,self.y)

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
    
    # moves the snake at every second and check if there's
    # collision bw fruit and the snake, and check for game over.
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
        
    # Draws element at the first frame before the game starts
    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
    
    # check if snake body collides with fruit position
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_sound()
        
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()
    
    # check for game over if the snake gets out of boundary
    def check_fail(self):
        print("snakebody:{}".format(self.snake.body[0]))
        if not 0 <= self.snake.body[0].x < cell_numberX or not 0 <= self.snake.body[0].y < cell_numberY:
            self.game_over()
        
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def draw_score(self):
        score_text = str(len(self.snake.body) -3) + ' (HS:{})'.format(highest_score)
        score_surface = g_font.render(score_text, True, (56,74,12))
        score_x = int(cell_size*cell_numberX - 70)
        score_y = int(1*cell_size)
        score_rectangle = score_surface.get_rect(center = (score_x, score_y))
        apple_rectangle = apple.get_rect(midright = (score_rectangle.left, score_rectangle.centery))
        bg_rectangle = pygame.Rect(apple_rectangle.left, apple_rectangle.top, apple_rectangle.width + score_rectangle.width + 5, apple_rectangle.height)

        pygame.draw.rect(screen,(168,189,191), bg_rectangle)
        screen.blit(score_surface, score_rectangle)
        screen.blit(apple, apple_rectangle)
        pygame.draw.rect(screen,(56,74,12), bg_rectangle,2)

    # if game over, reset the snake and check high score
    def game_over(self):
        global highest_score
        score = len(self.snake.body) - 3
        if highest_score < score:
            highest_score = score
        self.snake.reset()

pygame.init()
cell_size = 40
cell_numberX = 30
cell_numberY = 15
screen = pygame.display.set_mode((1200,600)) # resolution
clock = pygame.time.Clock() # will be used later to update the frame at interval
pygame.display.set_caption("SNAKE GAME")
apple = pygame.image.load('imgs/apple.png').convert_alpha()
g_font = pygame.font.Font(None, 25)
pygame.mixer.pre_init(44100,-16,2,512) # frequency and channels etc for music
highest_score = 0

screen_update = pygame.USEREVENT
pygame.time.set_timer(screen_update, 150) # check for events every 150ms.

main_game = MAIN()

while True:
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # frame update, at interval
        if event.type == screen_update:
            main_game.update()
        
        if event.type == KEYDOWN:
            # if snake is not going down and the user presses up, then move up
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0,-1)
            
            # if snake is not going left and the user presses right, then move right
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1,0)
            
            # if snake is not going up and the user presses down, then move down
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0,1)                
            
            # if snake is not going right and the user presses left, then move left
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1,0)                            

    screen.fill((0,0,0))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)