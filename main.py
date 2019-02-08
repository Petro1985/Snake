import pygame
import math
import random

"""I''ll try to write game 'Snake'"""


class Bord:
    def __init__(self, width=30, height=30):
        # create board and init it
        self.board = []
        for i in range(width):
            self.board.append([0]*height)

        self.snake = Snake()
        self.berry = Berry(self)


    def draw(self):
        win.blit(bg, (0, 0))    # draw background

        self.snake.draw()            # draw snake


        # for y in range(len(self.board)):
        #     for x in range(len(self.board[y])):
        #         if self.board[x][y] != 1:   #


class Berry:
    def __init__(self):
        self.pos_x = random.randint(0, 29)
        self.pos_x = random.randint(0, 29)


class Tale:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Snake:
    def __init__(self):
        # start position of the snake
        self.pos_x = 10
        self.pos_y = 10

        # create start body
        self.body = []
        self.body.append(Tale(8, 10))
        self.body.append(Tale(9, 10))
        self.body.append(Tale(10, 10))

    def draw(self):
        pygame.draw.rect(win, (), ())



def draw_window():
    win.blit(bg, (0, 0))    # draw background

    #pygame.draw.rect(win, (0, 0, 255), (x, y, width, height))

    # if anim_count == 30:
    #     anim_count = 0
    #
    # if goLeft:
    #     win.blit(animLeft[anim_count // 5], (x, y))
    #     anim_count += 1
    # elif goRight:
    #     win.blit(animRight[anim_count // 5], (x, y))
    #     anim_count += 1
    # else:
    #     win.blit(animStand, (x, y))

    # for bullet in bullets:
    #     bullet.draw(win)
    pygame.display.update()

random.seed()

pygame.display.set_caption('Snake')
win = pygame.display.set_mode((546, 546))

clock = pygame.time.Clock()

bg = pygame.image.load('bg.bmp')

board = Bord()      # create board
snake = Snake()     # create The Snake

run = True


while run:

    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    # get pressed keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
         run = False
    # if keys[pygame.K_f]:
    #     if len(bullets) < 5:
    #         bullets.append(Cannon(round(x + width // 2), round(y + height // 2), 5, (255, 0, 0), -1 if lastMove == 'left' else 1))
    # if keys[pygame.K_LEFT]:
    #     x -= speed if x >= speed else 0
    #     goRight = False
    #     goLeft = True
    #     lastMove = 'left'
    # elif keys[pygame.K_RIGHT]:
    #     x += speed if x < 500 - speed - width else 0
    #     goRight = True
    #     goLeft = False
    #     lastMove = 'right'
    # else:
    #     goRight = False
    #     goLeft = False

    # if isJump:
    #     if jumpCount >= -10:
    #         y -= (jumpCount ** 2) / 2 if jumpCount > 0 else -(jumpCount ** 2) / 2
    #         jumpCount -= 1
    #     else:
    #         jumpCount = 10
    #         isJump = False
    # else:
    #     if keys[pygame.K_SPACE]:
    #         isJump = True

    board.draw()

pygame.quit()



