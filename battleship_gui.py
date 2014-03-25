
import random, pygame, sys
from pygame.locals import *

FPS = 10
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0  
assert WINDOWHEIGHT % CELLSIZE == 0 
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

# Set the colors
#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = ( 0,   0,   0)
RED       = (255,  0,   0)
BLUE      = ( 0,   0,  255)
DARKGREEN = ( 0,  155,  0)
GREEN     = ( 0,  255,  0)
DARKGRAY  = ( 40,  40, 40)
BGCOLOR   = BLUE

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)

    mousex = 0  # store the x coordinate of mouse event
    mousey = 0  # store the y coordinate of mouse event
    pygame.display.set_caption('Battleship')

    firstSelection = None

    pygame.mixer.music.load('bgm.mp3') # load the background music
    pygame.mixer.music.play(-1, 0.0)
    showStartScreen()
    
    while True:
        runGame()
        #showGameOverScreen() -- need to be implement
    pygame.mixer.music.stop
                
def runGame():
    mouseClicked = False
    DISPLAYSURF.fill(BGCOLOR)
    drawGrid()
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            mousex, mousey = event.pos
        elif event.type == MOUSEBUTTONUP:
            mousex, mousey = event.pos
            mouseClicked = True
            
#    shipx, shipy = getShipAtPixel(mousex, mousey)
#    if shipx != None and shipy != None:
# ---- Need to implement the content while playing the game 
    pygame.display.update()
    FPSCLOCK.tick(FPS)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press any key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

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
        degrees1 += 3 
        degrees2 += 7 
'''
def getShipAtPixel(mousex, mousey)
'''

def terminate():
    pygame.quit()
    sys.exit()

def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): 
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): 
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()






