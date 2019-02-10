import random
import pygame

"""
I''ll try to write game 'Snake'
"""

SNAKE_MOVE_EVENT = pygame.USEREVENT + 1
SNAKE_SPEEDUP_EVENT = pygame.USEREVENT + 2
BERRY_GROWN_EVENT = pygame.USEREVENT + 3
SNAKE_ANIMATE_EVENT = pygame.USEREVENT + 4

TYPES_OF_BERRIES = 6


class GameMode:
    PLAY = 0
    GAME_OVER = 1
    MENU = 2
    PAUSE = 3


class Coord:
    x = 0
    y = 1


class Direction:
    STAND = (0,  0)
    UP = (0, -1)
    RIGHT = (1,  0)
    DOWN = (0,  1)
    LEFT = (-1, 0)


class Painter:
    def __init__(self, size_of_cell, size_of_board, edging=4, font_size=50):
        self.size_of_edging = edging
        self.size_of_cell = size_of_cell
        self.my_font = pygame.font.SysFont('helvetica', font_size)

        # set size of window
        self.screen = pygame.display.set_mode((size_of_board[Coord.x] * self.size_of_cell + self.size_of_edging * 2,
                                               size_of_board[Coord.y] * self.size_of_cell + self.size_of_edging * 2))

        pygame.display.set_icon(pygame.image.load('res/snake_ico.png'))     # set window icon
        pygame.display.set_caption('Snake')                                 # set window title

        # images define
        self.image_back_ground_light = []
        self.image_back_ground_dark = []
        self.image_game_over = []
        self.image_snake_head = []
        self.image_berry = []
        self.image_snake_body = []
        self.image_snake_tail = []
        self.load_images()    # load pictures

        self.edging_color = (200, 200, 200)

    def __del__(self):
        pass

    def update_board_around_snake(self, board):
        x = board.snake.body[0].pos[Coord.x] - board.snake.body[0].direction_from[Coord.x]
        y = board.snake.body[0].pos[Coord.y] - board.snake.body[0].direction_from[Coord.y]
        self.screen.blit(self.image_back_ground_dark if (x + y) % 2 == 0 else self.image_back_ground_light,
                         (x * self.size_of_cell + self.size_of_edging,
                          y * self.size_of_cell + self.size_of_edging))  # draw background

        x = board.snake.body[-1].pos[Coord.x] - board.snake.body[-1].direction_from[Coord.x]
        y = board.snake.body[-1].pos[Coord.y] - board.snake.body[-1].direction_from[Coord.y]

        need_redraw_edging = False
        for tx in range(x - 1, x + 2):
            for ty in range(y - 1, y + 2):
                if 0 <= tx < board.size[Coord.x] and 0 <= ty < board.size[Coord.y]:
                    self.screen.blit(self.image_back_ground_dark if (tx + ty) % 2 == 0 else self.image_back_ground_light,
                                     (tx * self.size_of_cell + self.size_of_edging,
                                      ty * self.size_of_cell + self.size_of_edging))  # draw background
                    for berry in board.berries:
                        if berry.pos == [tx, ty]:
                            self.draw_berry(berry)
                else:
                    need_redraw_edging = True

        if need_redraw_edging:
            self.draw_edging(board)

    def draw_edging(self, board):
        pygame.draw.rect(self.screen, self.edging_color,
                         pygame.Rect(self.size_of_edging / 2 -1, self.size_of_edging / 2 - 1,
                                     board.size[Coord.x] * self.size_of_cell + self.size_of_edging + 1,
                                     board.size[Coord.y] * self.size_of_cell + self.size_of_edging + 1
                                     ), self.size_of_edging
                         )

    def draw_board(self, board):
        for x in range(board.size[Coord.x]):
            for y in range(board.size[Coord.y]):
                self.screen.blit(self.image_back_ground_dark if (x + y) % 2 == 0 else self.image_back_ground_light,
                                 (x * self.size_of_cell + self.size_of_edging,
                                 y * self.size_of_cell + self.size_of_edging))

    def draw_berry(self, berry):
        self.screen.blit(self.image_berry[berry.kind], (berry.pos[Coord.x] * self.size_of_cell + self.size_of_edging,
                                                        berry.pos[Coord.y] * self.size_of_cell + self.size_of_edging))

    def draw_snake(self, snake):
        snake.anim_phase += GameEngine.clock.get_time()
        anim_coefficient = snake.anim_phase / snake.speed
        for part_of_body in snake.body:
            self.draw_part_of_snakes_body(part_of_body, anim_coefficient)

    def draw_part_of_snakes_body(self, part, anim_coefficient):
        if type(part) is Head:
            correction_x = 0
            correction_y = 0

            if part.direction_to == Direction.UP:
                correction_x = - (75 - self.size_of_cell) / 2
                correction_y = - (88 - self.size_of_cell) + (1 - anim_coefficient) * self.size_of_cell
            elif part.direction_to == Direction.RIGHT:
                correction_y = -(75 - self.size_of_cell) / 2
                correction_x = - (1 - anim_coefficient) * self.size_of_cell
            elif part.direction_to == Direction.DOWN:
                correction_x = -(75 - self.size_of_cell) / 2
                correction_y = - (1 - anim_coefficient) * self.size_of_cell
            elif part.direction_to == Direction.LEFT:
                correction_y = -(75 - self.size_of_cell) / 2
                correction_x = -(88 - self.size_of_cell) + (1 - anim_coefficient) * self.size_of_cell

            self.screen.blit(self.image_snake_head[part.direction_to],
                         (part.pos[Coord.x] * self.size_of_cell + self.size_of_edging + correction_x,
                          part.pos[Coord.y] * self.size_of_cell + self.size_of_edging + correction_y))
        elif type(part) is Tail:
            self.screen.blit(self.image_snake_body[(part.direction_from, part.direction_to)],
                             (part.pos[Coord.x] * self.size_of_cell + self.size_of_edging,
                              part.pos[Coord.y] * 64 + self.size_of_edging))

    @staticmethod
    def frame_update():
        pygame.display.update()     # update screen

    def load_images(self):
        self.image_back_ground_light = pygame.image.load('res/bg_light.bmp').convert()
        self.image_back_ground_dark = pygame.image.load('res/bg_dark.bmp').convert()
        self.image_game_over = pygame.image.load('res/game_over.png').convert()

        tmp_image_head = pygame.image.load('res/snake_0_64.png').convert_alpha()
        self.image_snake_head = {
            Direction.UP: tmp_image_head,
            Direction.RIGHT: pygame.transform.rotate(tmp_image_head, -90),
            Direction.DOWN: pygame.transform.rotate(tmp_image_head, 180),
            Direction.LEFT: pygame.transform.rotate(tmp_image_head, 90)
        }

        self.image_berry = [
            pygame.image.load('res/berry_64.png').convert_alpha(),
            pygame.image.load('res/berry_1_64.png').convert_alpha(),
            pygame.image.load('res/berry_2_64.png').convert_alpha(),
            pygame.image.load('res/berry_3_64.png').convert_alpha(),
            pygame.image.load('res/berry_4_64.png').convert_alpha(),
            pygame.image.load('res/poison_berry_1_64.png').convert_alpha(),
            pygame.image.load('res/poison_berry_2_64.png').convert_alpha()
        ]

        tmp_image_corner = pygame.image.load('res/corner_01_64.png').convert_alpha()
        tmp_image_straight = pygame.image.load('res/snake_02_64.png').convert_alpha()

        self.image_snake_body = {
            (Direction.UP, Direction.RIGHT): pygame.transform.rotate(tmp_image_corner, -90),
            (Direction.UP, Direction.UP): tmp_image_straight,
            (Direction.UP, Direction.LEFT): pygame.transform.rotate(tmp_image_corner, 180),
            (Direction.RIGHT, Direction.UP): pygame.transform.rotate(tmp_image_corner, 90),
            (Direction.RIGHT, Direction.RIGHT): pygame.transform.rotate(tmp_image_straight, 90),
            (Direction.RIGHT, Direction.DOWN): pygame.transform.rotate(tmp_image_corner, 180),
            (Direction.DOWN, Direction.LEFT): pygame.transform.rotate(tmp_image_corner, 90),
            (Direction.DOWN, Direction.RIGHT): tmp_image_corner,
            (Direction.DOWN, Direction.DOWN): tmp_image_straight,
            (Direction.LEFT, Direction.UP): tmp_image_corner,
            (Direction.LEFT, Direction.LEFT): pygame.transform.rotate(tmp_image_straight, 90),
            (Direction.LEFT, Direction.DOWN): pygame.transform.rotate(tmp_image_corner, -90)
        }

        self.image_snake_tail.append(pygame.image.load('res/tale_0_64.png').convert_alpha())
        self.image_snake_tail.append(pygame.transform.rotate(self.image_snake_tail[0], -90))
        self.image_snake_tail.append(pygame.transform.rotate(self.image_snake_tail[1], -90))
        self.image_snake_tail.append(pygame.transform.rotate(self.image_snake_tail[2], -90))


class GameEngine:
    clock = pygame.time.Clock()  # create a frames clock

    def __init__(self):

        self.game_mode = GameMode.PLAY              # start game mode
        self.current_score = 0          # score in current game
        self.berry_grow_time = 1000     # start Snake speed
        self.current_direction = None

        self.frequency = 60     # set frame rate
        random.seed()           # init of random
        pygame.font.init()      # init fonts
        self.start_snake_speed = 100
        self.board_size = (17, 17)
        self.board = None
        self.painter = None

    def new_game(self):
        self.board = Board(self.board_size, self.start_snake_speed)                  # create board
        self.painter = Painter(64, self.board.size)     # create painter
        pygame.time.set_timer(SNAKE_MOVE_EVENT, self.board.snake.speed)
        pygame.time.set_timer(BERRY_GROWN_EVENT, self.berry_grow_time)
        self.painter.draw_board(self.board)     # draw all board in start
        self.painter.draw_edging(self.board)    # draw edging
        self.current_direction = Direction.RIGHT

    def run_game(self):
        run = True

        self.new_game()

        while run:

            self.clock.tick(self.frequency)

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    return False
                elif self.game_mode == GameMode.PLAY:
                    self.game_in_play_event(ev)
                elif self.game_mode == GameMode.GAME_OVER:
                    pass
                elif self.game_mode == GameMode.MENU:
                    pass
                elif self.game_mode == GameMode.PAUSE:
                    pass
                    # self.painter.draw_snake(self.board.snake)

            if self.game_mode == 0:
                self.painter.update_board_around_snake(self.board)
                self.painter.draw_snake(self.board.snake)

            Painter.frame_update()

        pygame.quit()

    def __del__(self):
        pygame.font.quit()

    def game_in_play_event(self, ev):
        if ev.type == pygame.KEYDOWN:
            # get pressed keys
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                return False
            elif keys[pygame.K_LEFT] and self.board.snake.body[-1].direction_to != Direction.RIGHT:
                self.current_direction = Direction.LEFT
            elif keys[pygame.K_UP] and self.board.snake.body[-1].direction_to != Direction.DOWN:
                self.current_direction = Direction.UP
            elif keys[pygame.K_DOWN] and self.board.snake.body[-1].direction_to != Direction.UP:
                self.current_direction = Direction.DOWN
            elif keys[pygame.K_RIGHT] and self.board.snake.body[-1].direction_to != Direction.LEFT:
                self.current_direction = Direction.RIGHT
            elif keys[pygame.K_DELETE]:
                del self.board
                self.new_game()
        elif ev.type == SNAKE_MOVE_EVENT:
            self.board.move_snake(self.current_direction)
            if self.board.snake_check():
                self.game_mode = 1
        elif ev.type == BERRY_GROWN_EVENT:
            self.painter.draw_berry(self.board.add_berry())
        return True

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
                    self.text += ev.unicode
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
    def __init__(self, size, start_snake_speed):
        # create board and init it

        self.snake = Snake(start_snake_speed)   # create snake
        self.berries = []                       # create massive of berries
        self.size = size                        # size of the board

    def __del__(self):
        del self.snake
        for b in range(len(self.berries) - 1):
            del self.berries[b]

    def move_snake(self, direction):
        if direction != Direction.STAND:
            new_direction = direction
            self.snake.anim_phase = 0
            for part_of_body in self.snake.body[::-1]:
                part_of_body.move(new_direction)
                new_direction = part_of_body.direction_from

    def add_berry(self):        # create one more berry
        again = True
        while again:
            pos_x = random.randint(0, self.size[Coord.x])       # try to create a berry in random location
            pos_y = random.randint(0, self.size[Coord.y])       #

            again = False                       # we suggest that we have no problem with the position of the berry

            for tail in self.snake.body:
                if tail.pos[Coord.x] == pos_x and tail.pos[Coord.y] == pos_y:   # if the berry get into the snake
                    again = True                          # we will try to find new place for the berry
            for b in self.berries:
                if b.pos[Coord.x] == pos_x and b.pos[Coord.y] == pos_y:       # if the berry get into another berry
                    again = True                                # we will try to find new place for the berry
                    break

        self.berries.append(Berry([pos_x, pos_y]))
        return self.berries[-1]

    def snake_check(self):      # this function check snake break and ete
        head = self.snake.body[-1]

        for berry in self.berries:      # check berries eat
            if berry.pos == head.pos:
                self.snake.grow()
                self.berries.remove(berry)
                break

        if self.size[Coord.x] == head.pos[Coord.x] or self.size[Coord.y] == head.pos[Coord.y] \
                or head.pos[Coord.x] == -1 or head.pos[Coord.y] == -1:
            return True

        return False


class Berry:
    def __init__(self, pos):
        self.kind = random.randint(0, TYPES_OF_BERRIES - 1)
        self.pos = pos


class PartOfSnakesBody:
    def __init__(self, coord, direction):
        self.pos = coord
        self.direction_to = direction


class Head(PartOfSnakesBody):
    def __init__(self, coord, direction_to, direction_from):
        super(Head, self).__init__(coord, direction_to)
        self.color = (78, 125, 240)
        self.direction_from = direction_from

    def move(self, direction):
        self.pos[0] += direction[0]
        self.pos[1] += direction[1]
        self.direction_from = direction
        self.direction_to = direction


class Tail(PartOfSnakesBody):
    def __init__(self, coord, direction_to, direction_from):
        super(Tail, self).__init__(coord, direction_to)
        self.direction_from = direction_from

    def move(self, direction):
        self.pos[0] += self.direction_to[0]
        self.pos[1] += self.direction_to[1]
        self.direction_from = self.direction_to
        self.direction_to = direction


class Snake:
    def __init__(self, start_speed):
        # create start body
        self.direction = Direction.RIGHT
        self.speed = start_speed
        self.anim_phase = 0
        self.body = []
        self.body.append(Tail([2, 8], Direction.RIGHT, Direction.RIGHT))
        self.body.append(Tail([3, 8], Direction.RIGHT, Direction.RIGHT))
        self.body.append(Head([4, 8], Direction.RIGHT, Direction.RIGHT))

    def __len__(self):
        return len(self.body)

    def grow(self):
        pos = [0, 0]
        pos[0] = self.body[0].pos[0] - self.body[0].direction_from[0]
        pos[1] = self.body[0].pos[1] - self.body[0].direction_from[1]
        self.body.insert(0, Tail(pos, self.body[0].direction_from, self.body[0].direction_from))

    def set_speed(self, new_speed):
        self.speed = new_speed
        pygame.time.set_timer(SNAKE_MOVE_EVENT, new_speed)



game = GameEngine()
game.run_game()
