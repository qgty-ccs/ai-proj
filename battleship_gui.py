'''
CS 5100 Proj:   Battleship
Team:           BigLeg
Last Modified:  03/28/2014
'''

import copy
import random
import sys
import time
import pygame
import pygame.gfxdraw
from pygame.locals import *

from PAdLib import draw

from battleship_ai import Map, Agent, Human, init_agent, init_human, array_to_arrangement
from battleship_ai import TEST_ARRANGEMENT, TEST_FLEET, assignailoc, fleet_to_array

# game constants
FPS = 30
WINDOWWIDTH = 945
WINDOWHEIGHT = 600
SCOREBOARDHEIGHT = 25
CELLSIZE = 40
BOARDSIZE = 10  # 10x10 board
MARGIN = 5
SHIPS = [5, 4, 3, 3, 2]
SHIP_PROMPTS = [
    'Carrier: 1',
    'Battleship: 1',
    'Submarine: 1',
    'Cruiser: 1',
    'Destroyer: 1'
]
SHIP_NAMES = [
    'Carrier',
    'Battleship',
    'Submarine',
    'Cruiser',
    'Destroyer'
]

COUNTER = 0
GAME_INFO = ''

# define colors
#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = ( 0,   0,   0)
RED       = (128, 128,  128)
BLUE      = ( 0,   0,  255)
DARKGREEN = ( 0,  155,  0)
GREEN     = ( 0,  255,  0)
DARKGRAY  = ( 40,  40, 40)
LIGHTBLUE = (135, 206, 250)
NAVY      = ( 0,   0,  128)
BGCOLOR   = BLUE

bgimage = pygame.image.load('bgi.jpg')

class Ship:

    coords = []
    # 1 - L5 2 - L4 3 - L3 4 - L3 5 - L2
    t = 0
    head = None
    tail = None

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)


class Board:
    fleet = {}
    grid = []

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def place_ship(self):
        ''' Convert ship candidates into a ship.
        '''
        name = SHIP_NAMES[0]
        ship = []
        for x in range(BOARDSIZE):
            for y in range(BOARDSIZE):
                if self.grid[x][y] == 'C':
                    self.grid[x][y] = '1'
                    ship.append((x,y))

        self.fleet[name] = ship
        del SHIP_NAMES[0]



def shipmaker(x, y, length):
    ''' Create a horizontal arrangement of ship of given length.
    '''
    ship = [(x,y)]
    if x <= BOARDSIZE - length:
        # place horizontally
        for i in range(x, x + length):
            ship.append((i,y))
    else:
        # not enough space, stick to right edge
        for i in range(BOARDSIZE - length, BOARDSIZE):
            ship.append((i,y))


def main():
    global FPSCLOCK, SURFACE, BASICFONT, BOARD, COUNTER, GAME_INFO

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SURFACE = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 14)

    # mousex = 0  # store the x coordinate of mouse event
    # mousey = 0  # store the y coordinate of mouse event

    pygame.display.set_caption('Battleship')

    # pygame.mixer.music.load('bgm.mp3') # load the background music
    # pygame.mixer.music.play(-1, 0.0)

    welcome()
    
    BOARD = Board(grid=init_grid())

    arrangement()

    game()

    # pygame.mixer.music.stop


def welcome():
    ''' Show animated welcome screen.
    '''
    SURFACE.blit(bgimage, (0,0))
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Battleship!', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('Battleship!', True, GREEN)

    degrees1 = 0
    degrees2 = 0
    while True:
        SURFACE.blit(bgimage, (0,0))
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        SURFACE.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        SURFACE.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() 
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 0.5
        degrees2 += 1.5


def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press any key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    SURFACE.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def init_grid():
    ''' Init a 20x10 grid array.
    '''
    return [['0' for y in range(BOARDSIZE)] for x in range(BOARDSIZE * 2)]


def arrangement():
    ''' Let player arrange fleets on board before game begins.
    '''
    SURFACE.blit(bgimage, (0,0))
    draw_grid()
    horizontal = True

    while SHIPS:
        for event in pygame.event.get():
            if termination_detected(event):
                terminate()
            elif event.type == MOUSEMOTION:
                clear_grid()
                pos = event.pos
                if within_range(pos):
                    draw_ship_shape(pos, horizontal)
            elif event.type == MOUSEBUTTONDOWN:
                pos = event.pos
                if within_range(pos):
                    BOARD.place_ship()
                    del SHIPS[0]
                    del SHIP_PROMPTS[0]

        SURFACE.blit(bgimage, (0,0))
        draw_grid()
        fill_below()
        draw_arrangement_indicator()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def within_range((x,y)):
    ''' Tell if (x, y) falls in player's map range.
    '''
    x = x // (CELLSIZE + MARGIN)
    y = y // (CELLSIZE + MARGIN)
    if 0 <= x < BOARDSIZE and 0 <= y < BOARDSIZE:
        return True
    return False


def draw_ship_shape((x,y), horizontal):
    ''' Draw an outlined ship on surface.
    '''
    x = x // (CELLSIZE + MARGIN)
    y = y // (CELLSIZE + MARGIN)

    ship = set([])
    occupied = False
    if SHIPS:
        crnt_ship = SHIPS[0]
        ship.add((x,y))
        if x <= BOARDSIZE - crnt_ship:
            # place horizontally
            for i in range(x, x + crnt_ship):
                ship.add((i,y))
        else:
            # not enough space, stick to right edge
            for i in range(BOARDSIZE - crnt_ship, BOARDSIZE):
                ship.add((i,y))

    for (sx,sy) in ship:
        if BOARD.grid[sx][sy] != '0':
            # occupied
            occupied = True

    if not occupied:
        # mark cells as candidates
        for (sx,sy) in ship:
            BOARD.grid[sx][sy] = 'C'

    draw_grid()
    pygame.display.update()
    FPSCLOCK.tick(FPS)


def clear_grid():
    for x in range(BOARDSIZE):
        for y in range(BOARDSIZE):
            if BOARD.grid[x][y] == 'C':
                BOARD.grid[x][y] = '0'


def draw_grid():
    grid = BOARD.grid
    # draw left side
    for x in range(BOARDSIZE):
        for y in range(BOARDSIZE):

            color = WHITE
            filled = False
            g = grid[x][y]

            if g == 'C':
                color = GREEN
                filled = True
            elif g == '1':
                color = RED
                filled = True
            elif g == 'M':
                draw_miss((x,y), True)
            elif g == 'H':
                draw_hit((x,y), True)
            rect = [(MARGIN + CELLSIZE) * x + MARGIN,
                    (MARGIN + CELLSIZE) * y + MARGIN,
                    CELLSIZE,
                    CELLSIZE]
            if filled:
                pygame.draw.rect(SURFACE, color, rect)
            pygame.draw.rect(SURFACE, WHITE, rect, 2)

    # draw right side
    for x in range(BOARDSIZE, 2 * BOARDSIZE):
        for y in range(BOARDSIZE):

            g = grid[x][y]

            if g == 'M':
                draw_miss((x,y), False)
            elif g == 'H':
                draw_hit((x,y), False)
            rect = [(MARGIN + CELLSIZE) * x + MARGIN + CELLSIZE,
                    (MARGIN + CELLSIZE) * y + MARGIN,
                    CELLSIZE,
                    CELLSIZE]
            pygame.draw.rect(SURFACE, WHITE, rect, 2)


def draw_hit((x,y), human):
    y = (MARGIN + CELLSIZE) * y + MARGIN + CELLSIZE / 2
    if human:
        x = (MARGIN + CELLSIZE) * x + MARGIN + CELLSIZE / 2
    else:
        # right side
        x = (MARGIN + CELLSIZE) * x + MARGIN + 3*CELLSIZE / 2
    draw_occupied((x,y))
    pygame.draw.circle(SURFACE, BLACK, (x, y), 10)


def draw_occupied((x,y)):
    rect = [x-CELLSIZE/2, y-CELLSIZE/2, CELLSIZE, CELLSIZE]
    pygame.draw.rect(SURFACE, RED, rect)
    pygame.draw.rect(SURFACE, WHITE, rect, 2)


def draw_miss((x,y), human):    
    if human:
        rect = [(MARGIN + CELLSIZE) * x + MARGIN,
                (MARGIN + CELLSIZE) * y + MARGIN,
                CELLSIZE,
                CELLSIZE]
    else:
        # right side
        rect = [(MARGIN + CELLSIZE) * x + MARGIN + CELLSIZE,
                (MARGIN + CELLSIZE) * y + MARGIN,
                CELLSIZE,
                CELLSIZE]
        
    pygame.draw.rect(SURFACE, BLUE, rect)
    pygame.draw.rect(SURFACE, WHITE, rect, 2)
    cy = (MARGIN + CELLSIZE) * y + MARGIN + CELLSIZE / 2
    if human:
        cx = (MARGIN + CELLSIZE) * x + MARGIN + CELLSIZE / 2
    else:
        cx = (MARGIN + CELLSIZE) * x + MARGIN + 3*CELLSIZE / 2

    # pygame.draw.circle(SURFACE, WHITE, (cx,cy), 20, 2)
    pygame.draw.circle(SURFACE, WHITE, (cx,cy), 15, 2)
    pygame.draw.circle(SURFACE, WHITE, (cx,cy), 10, 2)
    pygame.draw.circle(SURFACE, WHITE, (cx,cy), 5, 2)


def fill_below():
    # erase all indicators
    rect = pygame.Rect(MARGIN, 460, WINDOWWIDTH - 2 * MARGIN, 130)
    SURFACE.fill(LIGHTBLUE, rect)
    pygame.draw.rect(SURFACE, WHITE, rect, 2)


def draw_arrangement_indicator():
    base = 470
    draw_msg('Please arrange your fleet', (2*MARGIN, base))
    draw_scoreboard(2*MARGIN, SHIP_PROMPTS)


def draw_scoreboard(left, msgs):
    base = 470
    for msg in msgs:
        base = base + 20
        draw_msg(msg, (left, base))


def game():
    global COUNTER, GAME_INFO
    human_turn = True
    alloc = assignailoc()
    human = init_human(BOARDSIZE, array_to_arrangement(BOARD.grid), BOARD.fleet)
    agent = init_agent(BOARDSIZE, fleet_to_array(alloc), alloc)
    x = 0
    y = 0

    while True:
        if human.lose():
            GAME_INFO = 'AI win'
        if agent.lose():
            GAME_INFO = 'You win'

        draw_score(human.getfleet(), agent.getfleet(), human_turn)
        pygame.display.update()

        if human_turn:
            for event in pygame.event.get():
                if termination_detected(event):
                    terminate()
                elif event.type == MOUSEBUTTONDOWN:
                    x = event.pos[0] // (CELLSIZE + MARGIN) - 1
                    y = event.pos[1] // (CELLSIZE + MARGIN)

            if x >= BOARDSIZE:
                resp = human.attack(agent, (x-BOARDSIZE,y))
                result, sunk_ship = resp['result'], resp['sunk_ship']
                BOARD.grid[x][y] = result

                if result == 'M':
                    human_turn = not human_turn

                if sunk_ship:
                    GAME_INFO = 'Enemy\'s ' + sunk_ship + ' was destroyed!'

                COUNTER = COUNTER + 1

                draw_grid()
                pygame.display.update()

                x = 0
                y = 0
        else:
            x, y = agent.find_target()
            resp = agent.attack(human, (x, y))
            result, sunk_ship = resp['result'], resp['sunk_ship']
            BOARD.grid[x][y] = result

            if result == 'M':
                human_turn = not human_turn

            if sunk_ship:
                    GAME_INFO = 'Your ' + sunk_ship + ' was destroyed!'

            COUNTER = COUNTER + 1

            draw_grid()
            pygame.display.update()

            x = 0
            y = 0

        FPSCLOCK.tick(FPS)


def draw_msg(msg, (x,y)):
    word = BASICFONT.render(msg, True, WHITE)
    rect = word.get_rect()
    rect.topleft = (x,y)
    # clear that area first
    SURFACE.fill(LIGHTBLUE, rect)
    SURFACE.blit(word, rect)


def draw_score(human_fleet, ai_fleet, human_turn):
    global GAME_INFO
    # erase previous msgs
    fill_below()

    # print human fleet
    draw_scoreboard(2*MARGIN, human_fleet)

    # print ai fleet
    draw_scoreboard(WINDOWWIDTH - 105, ai_fleet)

    # print turn indicator
    turn = 'Your Turn' if human_turn else 'AI Turn'
    draw_msg(turn, (WINDOWWIDTH / 2 - 40, WINDOWHEIGHT - 30))

    # print counter
    counter = 'Turn: ' + str(COUNTER)
    draw_msg(counter, (WINDOWWIDTH / 2 - 40, 470))

    # print game info
    draw_msg(GAME_INFO, (WINDOWWIDTH / 2 - 40, 500))


def termination_detected(event):
    if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
        return True
    return False


def terminate():
    pygame.quit()
    sys.exit(0)


if __name__ == '__main__':
    main()