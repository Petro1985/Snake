import random
import pygame

"""
I''ll try to write game 'Snake'
for direction i used numbers that mean: 0 - up, 1 - right, 2 - down, 3 - left and -1 - no direction  
"""


class ScoreBoard:
    def __init__(self):
        pass

    def save_to_file(self):
        pass

    def draw(self):
        pass


class InputBox:

    def __init__(self, x, y, w, h, title=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (255, 128, 0)
        self.text = ''
        self.txt_surface = my_font.render('', True, self.color)
        self.title = title

    def handle_event(self, ev):
        if ev.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                text = self.text
                self.text = ''
                return text
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if len(self.text) < 20:
                    self.text += event.unicode
            # Re-render the text.
            self.txt_surface = my_font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        pygame.draw.rect(screen, (128, 64, 64), pygame.Rect(self.rect.x - 20, self.rect.y - 75, self.rect.w + 40, self.rect.h + 100))
        screen.blit(my_font.render(self.title, True, self.color), (self.rect.x + (self.rect.w/2 - 175), self.rect.y - 65))
        pygame.draw.rect(screen, self.color, self.rect, 2)
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+10, self.rect.y+5))
        # Blit the rect.


class Board:            # this class represent game board
    def __init__(self, width=17, height=17):
        # create board and init it
        self.board = []
        for i in range(width):
            self.board.append([0]*height)
        self.count_of_eaten_berries = 0

        self.game_mode = 0              # if it is 1 that mean game over
        self.snake = Snake(20)          # create snake
        self.berries = []               # create massive of berries
        self.berry_timer = 0            # init berries timer
        self.berry_frequency = 100      # it means how often new berry will show
        self.speed_up_frequency = 1000  # how often snakes will speed up
        self.speed_up_time = self.speed_up_frequency
        self.current_score = 0

    def __del__(self):
        del self.snake
        for b in range(len(self.berries) - 1):
            del self.berries[b]

    def add_berry(self):        # create one more berry
        again = True
        while again:
            pos_x = random.randint(0, 16)      # try to create a berry in random location
            pos_y = random.randint(0, 16)      #

            again = False                           # we suggest that we have no problem with the position of the berry

            for tale in self.snake.body:
                if tale.x == pos_x and tale.y == pos_y:   # if the berry get into the snake
                    again = True                          # we will try to find new place for the berry
            for b in self.berries:
                if b.pos_x == pos_x and b.pos_y == pos_y:       # if the berry get into another berry
                    again = True                                # we will try to find new place for the berry
                    break

        self.berries.append(Berry(pos_x, pos_y))

    def turn(self):     # this function contain logic of the game

        if not self.game_mode == 1:      # if not game over yet
            if self.speed_up_time == 0:     # may be it's a time for speed up?
                self.speed_up_time = self.speed_up_frequency        # if it is, speed up the snake and reset timer
                self.snake.speed_up()                               #
            else:
                self.speed_up_time -= 1

            if self.berry_timer == 0:  # add a new berry if it's time to timer
                self.berry_timer = self.berry_frequency
                self.add_berry()
            else:
                self.berry_timer -= 1   # else reduce timer

            if self.snake.try_to_move():    # if the snake moved then
                head = self.snake.body[-1]
                if head.x < 0 or head.y < 0 or head.x > 16 or head.y > 16:
                    self.game_mode = 1
                for part_of_body in self.snake.body[:len(self.snake.body)-1]:
                    if head.x == part_of_body.x and head.y == part_of_body.y:
                        self.game_mode = 1

                # may be the snake ate the berry?
                for b in self.berries:
                    if head.x == b.pos_x and head.y == b.pos_y:
                        self.current_score += 1
                        self.berries.remove(b)
                        if self.snake.body[0].direction_from == 0:
                            last_x = self.snake.body[0].x
                            last_y = self.snake.body[0].y + 1
                        elif self.snake.body[0].direction_from == 1:
                            last_x = self.snake.body[0].x - 1
                            last_y = self.snake.body[0].y
                        elif self.snake.body[0].direction_from == 2:
                            last_x = self.snake.body[0].x
                            last_y = self.snake.body[0].y - 1
                        elif self.snake.body[0].direction_from == 3:
                            last_x = self.snake.body[0].x + 1
                            last_y = self.snake.body[0].y

                        self.snake.body.insert(
                            0,
                            Tale(
                                last_x,
                                last_y,
                                self.snake.body[0].direction_from,
                                -1
                            )
                        )
                        break       # if we find the eaten berry, there is no need to continue searching

    def draw(self):
        win.blit(bg, (0, 0))  # draw background
        pygame.draw.rect(win, (100, 100, 100), pygame.Rect(0, 1092, 1092, 64))  # scoreboard
        # win.blit(my_font.render('You score: ' + str(self.curent_score) + " Time until speed up: " + str(round(self.speed_up_time / 60)), 1, (200, 80, 230)), (10, 1092))  # draw background

        for b in self.berries:      # draw berries
            b.draw()                #

        self.snake.draw()           # draw snake

        if self.game_mode == 1:          # if game over draw "Game Over"
            win.blit(game_over, (300, 200))
            inp.draw(win)

        pygame.display.update()     # update screen


class Berry:
    def __init__(self, x, y):
        self.kind = random.randint(0, len(berry) - 1)
        self.pos_x = x
        self.pos_y = y

    def draw(self):
        win.blit(berry[self.kind], (self.pos_x * 64 + 2, self.pos_y * 64 + 2))  # draw background


class BodyOfSnake:
    def __init__(self, x, y, direction_to, direction_from):
        self.x = x
        self.y = y
        self.direction_to = direction_to
        self.direction_from = direction_from


class Head(BodyOfSnake):
    def __init__(self, x, y, direction_to, direction_from):
        super(Head, self).__init__(x, y, direction_to, direction_from)
        self.color = (78, 125, 240)

    def draw(self, time, cur_time):
        percent = (time-cur_time)/time
        if self.direction_to == 0:
            win.blit(snake_body_02, (self.x * 64 + 4, self.y * 64 + 4 - percent * 64 + 64))    # it's the snakes neck
            win.blit(snake_head[0], (self.x * 64 - 6 + 2, self.y * 64 - 34 + 2 - percent * 64 + 64))
        if self.direction_to == 1:
            win.blit(snake_body_13, (self.x * 64 + 4 + percent * 64 - 64, self.y * 64 + 4))    # it's the snakes neck
            win.blit(snake_head[1], (self.x * 64 + 2 + percent * 64 - 64, self.y * 64 - 6 + 2))
        if self.direction_to == 2:
            win.blit(snake_body_02, (self.x * 64 + 4, self.y * 64 + 4 + percent * 64 - 64))    # it's the snakes neck
            win.blit(snake_head[2], (self.x * 64 - 8 + 2, self.y * 64 + 2 + percent * 64 - 64))
        if self.direction_to == 3:
            win.blit(snake_body_13, (self.x * 64 + 4 - percent * 64 + 64, self.y * 64 + 4))    # it's the snakes neck
            win.blit(snake_head[3], (self.x * 64 - 34 + 2 - percent * 64 + 64, self.y * 64 - 8 + 2))

    def move(self, new_direction):
        if new_direction == 0:
            self.y -= 1
        elif new_direction == 1:
            self.x += 1
        elif new_direction == 2:
            self.y += 1
        elif new_direction == 3:
            self.x -= 1
        self.direction_from = new_direction
        self.direction_to = new_direction


class Tale(BodyOfSnake):
    def __init__(self, x, y, direction_to, direction_from):
        super(Tale, self).__init__(x, y, direction_to, direction_from)
        self.color = (98, 145, 220)

    def draw(self, time, cur_time, is_tale=False):
        if is_tale:         # if it's a last one then draw the tale
            percent = (time - cur_time) / time
            x = self.x * 64 + 4
            y = self.y * 64 + 4
            win.blit(snake_tale[self.direction_to], (x, y))
        else:               # otherwise we draw a part of the body
            if (self.direction_to == 1 and self.direction_from == 2) \
                    or (self.direction_to == 0 and self.direction_from == 3):
                win.blit(snake_body_01, (self.x * 64 + 4, self.y * 64 + 4))
            elif (self.direction_to == 1 and self.direction_from == 0) \
                    or (self.direction_to == 2 and self.direction_from == 3):
                win.blit(snake_body_12, (self.x * 64 + 4, self.y * 64 + 4))
            elif (self.direction_to == 2 and self.direction_from == 1) \
                    or (self.direction_to == 3 and self.direction_from == 0):
                win.blit(snake_body_23, (self.x * 64 + 4, self.y * 64 + 4))
            elif (self.direction_to == 0 and self.direction_from == 1) \
                    or (self.direction_to == 3 and self.direction_from == 2):
                win.blit(snake_body_30, (self.x * 64 + 4, self.y * 64 + 4))
            elif (self.direction_to == 0 and self.direction_from == 0) \
                    or (self.direction_to == 2 and self.direction_from == 2):
                win.blit(snake_body_02, (self.x * 64 + 4, self.y * 64 + 4))
            elif (self.direction_to == 1 and self.direction_from == 1) \
                    or (self.direction_to == 3 and self.direction_from == 3):
                win.blit(snake_body_13, (self.x * 64 + 4, self.y * 64 + 4))

    def move(self, new_direction):
        if self.direction_to == 0:
            self.y -= 1
        elif self.direction_to == 1:
            self.x += 1
        elif self.direction_to == 2:
            self.y += 1
        elif self.direction_to == 3:
            self.x -= 1
        self.direction_from = self.direction_to
        self.direction_to = new_direction


class Snake:
    def __init__(self, speed = 10):
        # if time_to_move = 0 that mean time to move ^^
        self.time_to_move = speed

        # create start body
        self.direction = 1
        self.body = []
        self.body.append(Tale(2, 8, 1, 1))
        self.body.append(Tale(3, 8, 1, 1))
        self.body.append(Head(4, 8, 1, 1))
        self.snake_speed = speed

    def speed_up(self):
        self.snake_speed -= 1

    def speed_down(self):
        self.snake_speed += 1

    def draw(self):
        self.body[-1].draw(self.snake_speed, self.time_to_move)
        for part_of_body in self.body[1:]:
            part_of_body.draw(self.snake_speed, self.time_to_move)
        self.body[0].draw(self.snake_speed, self.time_to_move, True)

    def try_to_move(self):
        self.time_to_move -= 1

        if self.time_to_move == 0:      # of time_to_move = 0 that mean that time to move ^^
            self.time_to_move = self.snake_speed
            new_direction = self.direction
            for part_of_body in self.body[::-1]:
                part_of_body.move(new_direction)
                new_direction = part_of_body.direction_from
            return True
        else:
            return False


random.seed()           # init of random

win = pygame.display.set_mode((1092, 1156))
pygame.display.set_icon(pygame.image.load('snake_ico.png'))
pygame.display.set_caption('Snake')

clock = pygame.time.Clock()

bg = pygame.image.load('bg_64.bmp')
game_over = pygame.image.load('game_over.png')

snake_head = [
    pygame.image.load('snake_0_64.png').convert_alpha(),
    pygame.image.load('snake_1_64.png').convert_alpha(),
    pygame.image.load('snake_2_64.png').convert_alpha(),
    pygame.image.load('snake_3_64.png').convert_alpha()
]

berry = [
    pygame.image.load('berry_64.png').convert_alpha(),
    pygame.image.load('berry_1_64.png').convert_alpha(),
    pygame.image.load('berry_2_64.png').convert_alpha(),
    pygame.image.load('berry_3_64.png').convert_alpha(),
    pygame.image.load('berry_4_64.png').convert_alpha(),
    pygame.image.load('poison_berry_1_64.png').convert_alpha(),
    pygame.image.load('poison_berry_2_64.png').convert_alpha()
]

snake_body_01 = pygame.image.load('corner_01_64.png').convert_alpha()
snake_body_12 = pygame.image.load('corner_12_64.png').convert_alpha()
snake_body_23 = pygame.image.load('corner_23_64.png').convert_alpha()
snake_body_30 = pygame.image.load('corner_30_64.png').convert_alpha()

snake_body_02 = pygame.image.load('snake_02_64.png').convert_alpha()
snake_body_13 = pygame.image.load('snake_13_64.png').convert_alpha()

snake_tale = [
    pygame.image.load('tale_0_64.png').convert_alpha(),
    pygame.image.load('tale_1_64.png').convert_alpha(),
    pygame.image.load('tale_2_64.png').convert_alpha(),
    pygame.image.load('tale_3_64.png').convert_alpha()
]

board = Board()      # create board

pygame.font.init()  # init fonts
my_font = pygame.font.SysFont('helvetica', 50)


pygame.init()

run = True
inp = InputBox(245, 800, 600, 70, 'Enter your name')

while run:

    clock.tick(60)

    for event in pygame.event.get():
        if board.game_mode == 1:
            name = inp.handle_event(event)
            if name:
                # save_to_file(name, board.curent_score)
                board = Board()

        if event.type == pygame.QUIT:
            run = False

    # get pressed keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        run = False
    if keys[pygame.K_LEFT] and board.snake.body[-1].direction_from != 1:
        board.snake.direction = 3
    elif keys[pygame.K_UP] and board.snake.body[-1].direction_from != 2:
        board.snake.direction = 0
    elif keys[pygame.K_DOWN] and board.snake.body[-1].direction_from != 0:
        board.snake.direction = 2
    elif keys[pygame.K_RIGHT] and board.snake.body[-1].direction_from != 3:
        board.snake.direction = 1
    elif board.game_mode == 1 and keys[pygame.K_DELETE]:
        board = Board()

    board.turn()
    board.draw()

pygame.quit()



