'''
CS 5100 Proj:   Battleship
Team:           BigLeg
Last Modified:  03/28/2014
'''

import random, pygame, sys, time
from pygame.locals import *

from battleship_ai import Map, Agent, Human, init_agent, init_human, array_to_arrangement
from battleship_ai import HEALTH, TEST_ARRANGEMENT

FPS = 30
WINDOWWIDTH = 1065
WINDOWHEIGHT = 555
CELLSIZE = 48
# assert WINDOWWIDTH % CELLSIZE == 0
# assert WINDOWHEIGHT % CELLSIZE == 0
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)
BOARDSIZE = 10  # 10x10 board
MARGIN = 5

# Define colors
#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = ( 0,   0,   0)
RED       = (255,  0,   0)
BLUE      = ( 0,   0,  255)
DARKGREEN = ( 0,  155,  0)
GREEN     = ( 0,  255,  0)
DARKGRAY  = ( 40,  40, 40)
LIGHTBLUE = (135, 206, 250)
BGCOLOR   = BLUE
NAVY = (0, 0, 128)

SHIPS = [5,4,3,3,2]


# boardImage = pygame.image.load('bgi.jpg')

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, SMALLFONT, GRID

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    SMALLFONT = pygame.font.Font('freesansbold.ttf', 12)

    mousex = 0  # store the x coordinate of mouse event
    mousey = 0  # store the y coordinate of mouse event
    pygame.display.set_caption('Battleship')

    firstSelection = None

    # pygame.mixer.music.load('bgm.mp3') # load the background music
    # pygame.mixer.music.play(-1, 0.0)

    GRID = init_grid()

    showStartScreen()
    
    arrangement()
        #showGameOverScreen() -- need to be implement
    game()
    pygame.mixer.music.stop
                
def arrangement():
    mouseClicked = False
    DISPLAYSURF.fill(BGCOLOR)

    drawGrid()

    while SHIPS:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit(0)
            # elif event.type == MOUSEMOTION:
            #     mousex, mousey = event.pos
            # elif event.type == MOUSEBUTTONUP:
            #     mousex, mousey = event.pos
            #     mouseClicked = True
            elif event.type == MOUSEBUTTONDOWN:
                # mark selected positions
                pos = event.pos
                x = pos[0] // (CELLSIZE + MARGIN)
                y = pos[1] // (CELLSIZE + MARGIN)
                if x < BOARDSIZE:  # only place ship on human side
                    place_ship(x, y)
                    # grid1[row][column] = 1
                # else:
                #     grid2[row][column - BOARDSIZE] = 1

        drawGrid()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

#    shipx, shipy = getShipAtPixel(mousex, mousey)
#    if shipx != None and shipy != None:
# ---- Need to implement the content while playing the game 
        

def game():
    human_turn = True
    human = init_human(BOARDSIZE, array_to_arrangement(GRID), HEALTH)
    agent = init_agent(BOARDSIZE, TEST_ARRANGEMENT, HEALTH)
    x = 0
    y = 0

    while True:
        drawScore(human.health, agent.health, human_turn)
        pygame.display.update()

        if human_turn:
            # wait for a choice
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit(0)
                elif event.type == MOUSEBUTTONDOWN:
                    pos = event.pos
                    x = pos[0] // (CELLSIZE + MARGIN)
                    y = pos[1] // (CELLSIZE + MARGIN)

            if x >= BOARDSIZE:
                # mark selected cell as candidate
                GRID[x][y] = 'C'

                drawGrid()
                pygame.display.update()

                pygame.time.wait(500)

                result = human.attack(agent, (x - BOARDSIZE,y))
                GRID[x][y] = result

                drawGrid()
                pygame.display.update()

                if result == 'H':
                    pygame.time.wait(500)
                else:
                    human_turn = not human_turn

                GRID[x][y] = '0'
                drawGrid()
                pygame.display.update()

                x = 0
                y = 0
        else:
            pygame.time.wait(500)

            x, y = agent.find_target()
            GRID[x][y] = 'C'

            drawGrid()
            pygame.display.update()

            pygame.time.wait(500)

            result = agent.attack(human, (x, y))
            GRID[x][y] = result

            drawGrid()
            pygame.display.update()
            

            if result == 'H':
                pygame.time.wait(500)
            else:
                human_turn = not human_turn

            GRID[x][y] = '0'
            drawGrid()
            pygame.display.update()

            x = 0
            y = 0

        FPSCLOCK.tick(FPS)


    # human firstSelection

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press any key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

def drawMsg(msg, (x, y)):
    word = BASICFONT.render(msg, True, WHITE)
    rect = word.get_rect()
    rect.topleft = (x, y)
    # clear that area first
    DISPLAYSURF.fill(BGCOLOR, rect)
    DISPLAYSURF.blit(word, rect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Battleship!', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('Battleship!', True, GREEN)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() 
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 1
        degrees2 += 3
'''
def getShipAtPixel(mousex, mousey)
'''

def terminate():
    pygame.quit()
    sys.exit()

def init_grid():
    return [[0 for y in range(BOARDSIZE)] for y in range(BOARDSIZE * 2)]

def drawScore(human_score, agent_score, human_turn):
    # erase previous msgs
    rect = pygame.Rect(0, WINDOWHEIGHT - 20, WINDOWWIDTH, 20)
    DISPLAYSURF.fill(BGCOLOR, rect)

    drawMsg('Score: ' + str(human_score), (20, WINDOWHEIGHT - 20))
    drawMsg('Score: ' + str(agent_score), (WINDOWWIDTH - 100, WINDOWHEIGHT - 20))
    if human_turn:
        drawMsg('Your turn', (WINDOWWIDTH / 2 - 40, WINDOWHEIGHT - 20))
    else:
        drawMsg('AI turn', (WINDOWWIDTH / 2 - 40, WINDOWHEIGHT - 20))

def drawGrid():
    # for x in range(0, WINDOWWIDTH, CELLSIZE): 
    #     pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    # for y in range(0, WINDOWHEIGHT, CELLSIZE): 
    #     pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))

    # draw a line in the middle
    pygame.draw.line(DISPLAYSURF, NAVY, (WINDOWWIDTH / 2, 5), (WINDOWWIDTH / 2, WINDOWHEIGHT - 25), 5)

    for x in range(BOARDSIZE):
        for y in range(BOARDSIZE):
            color = WHITE
            if GRID[x][y] == 1:
                color = GREEN
            elif GRID[x][y] == '0':
                color = WHITE
            elif GRID[x][y] == 'M':
                color = WHITE
            elif GRID[x][y] == 'H':
                color = RED
            pygame.draw.rect(DISPLAYSURF,
                             color,
                             [(MARGIN + CELLSIZE) * x + MARGIN,
                              (MARGIN + CELLSIZE) * y + MARGIN,
                              CELLSIZE,
                              CELLSIZE])
            if GRID[x][y] == 'C':
                pygame.draw.circle(DISPLAYSURF,
                                NAVY,
                                ((MARGIN + CELLSIZE) * x + MARGIN + 24, (MARGIN + CELLSIZE) * y + MARGIN + 24),
                                24,
                                2)

    for x in range(BOARDSIZE, 2 * BOARDSIZE):
        for y in range(BOARDSIZE):
            color = LIGHTBLUE
            if GRID[x][y] == '0':
                color = WHITE
            elif GRID[x][y] == 'M':
                color = WHITE
            elif GRID[x][y] == 'H':
                color = RED
            pygame.draw.rect(DISPLAYSURF,
                             color,
                             [(MARGIN + CELLSIZE) * x + MARGIN,
                              (MARGIN + CELLSIZE) * y + MARGIN,
                              CELLSIZE,
                              CELLSIZE])
            if GRID[x][y] == 'C':
                pygame.draw.circle(DISPLAYSURF,
                                WHITE,
                                ((MARGIN + CELLSIZE) * x + MARGIN + 24, (MARGIN + CELLSIZE) * y + MARGIN + 24),
                                24,
                                2)


def place_ship(x, y):
    if SHIPS:
        crnt_ship = SHIPS[0]
        # place ship based on x and y
        GRID[x][y] = 1
        if x <= BOARDSIZE - crnt_ship:
            # place horizontally
            for i in range(x, x + crnt_ship):
                GRID[i][y] = 1
        else:
            # not enough space, stick to right edge
            for i in range(BOARDSIZE - crnt_ship, BOARDSIZE):
                GRID[i][y] = 1

        del SHIPS[0]


if __name__ == '__main__':
    main()






