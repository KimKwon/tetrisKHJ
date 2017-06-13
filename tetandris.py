# Tetromino (a Tetris clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, time, pygame, sys, menu
from pygame.locals import *

'''
@author: avalanchy (at) google mail dot com
@version: 0.1; python 2.7; pygame 1.9.2pre; SDL 1.2.14; MS Windows XP SP3
@date: 2012-04-08
@license: This document is under GNU GPL v3

README on the bottom of document.

@font: from http://www.dafont.com/coders-crux.font
      more abuot license you can find in data/coders-crux/license.txt
'''
#
# if not pygame.display.get_init():
#     pygame.display.init()
#
# if not pygame.font.get_init():
#     pygame.font.init()
class Tetandris:

    def __init__(self) :


        self.FPS = 25
        self.WINDOWWIDTH = 800
        self.WINDOWHEIGHT = 600
        self.BOXSIZE = 23
        self.BOARDWIDTH = 10
        self.BOARDHEIGHT = 20
        self.BLANK = '.'
        self.score = 0

        self.MOVESIDEWAYSFREQ = 0.15
        self.MOVEDOWNFREQ = 0.1

        self.XMARGIN = int((self.WINDOWWIDTH - self.BOARDWIDTH * self.BOXSIZE) / 2)
        self.TOPMARGIN = self.WINDOWHEIGHT - (self.BOARDHEIGHT * self.BOXSIZE) - 5

        #               R    G    B
        self.WHITE       = (255, 255, 255)
        self.GRAY        = (185, 185, 185)
        self.BLACK       = (  0,   0,   0)
        self.RED         = (155,   0,   0)
        self.LIGHTRED    = (175,  20,  20)
        self.GREEN       = (  0, 155,   0)
        self.LIGHTGREEN  = ( 20, 175,  20)
        self.BLUE        = (  0,   0, 155)
        self.LIGHTBLUE   = ( 20,  20, 175)
        self.YELLOW      = (155, 155,   0)
        self.LIGHTYELLOW = (175, 175,  20)

        self.BORDERCOLOR = self.WHITE
        self.BGCOLOR = (00,22,33)
        self.TEXTCOLOR = self.WHITE
        self.TEXTSHADOWCOLOR = self.GRAY
        self.COLORS      = (     self.BLUE,      self.GREEN,      self.RED,      self.YELLOW)
        self.LIGHTCOLORS = (self.LIGHTBLUE, self.LIGHTGREEN, self.LIGHTRED, self.LIGHTYELLOW)
        assert len(self.COLORS) == len(self.LIGHTCOLORS) # each color must have light color

        self.TEMPLATEWIDTH = 5
        self.TEMPLATEHEIGHT = 5

        self.S_SHAPE_TEMPLATE = [['.....',
                             '.....',
                             '..OO.',
                             '.OO..',
                             '.....'],
                            ['.....',
                             '..O..',
                             '..OO.',
                             '...O.',
                             '.....']]

        self.Z_SHAPE_TEMPLATE = [['.....',
                             '.....',
                             '.OO..',
                             '..OO.',
                             '.....'],
                            ['.....',
                             '..O..',
                             '.OO..',
                             '.O...',
                             '.....']]

        self.I_SHAPE_TEMPLATE = [['..O..',
                             '..O..',
                             '..O..',
                             '..O..',
                             '.....'],
                            ['.....',
                             '.....',
                             'OOOO.',
                             '.....',
                             '.....']]

        self.O_SHAPE_TEMPLATE = [['.....',
                             '.....',
                             '.OO..',
                             '.OO..',
                             '.....']]

        self.J_SHAPE_TEMPLATE = [['.....',
                             '.O...',
                             '.OOO.',
                             '.....',
                             '.....'],
                            ['.....',
                             '..OO.',
                             '..O..',
                             '..O..',
                             '.....'],
                            ['.....',
                             '.....',
                             '.OOO.',
                             '...O.',
                             '.....'],
                            ['.....',
                             '..O..',
                             '..O..',
                             '.OO..',
                             '.....']]

        self.L_SHAPE_TEMPLATE = [['.....',
                             '...O.',
                             '.OOO.',
                             '.....',
                             '.....'],
                            ['.....',
                             '..O..',
                             '..O..',
                             '..OO.',
                             '.....'],
                            ['.....',
                             '.....',
                             '.OOO.',
                             '.O...',
                             '.....'],
                            ['.....',
                             '.OO..',
                             '..O..',
                             '..O..',
                             '.....']]

        self.T_SHAPE_TEMPLATE = [['.....',
                             '..O..',
                             '.OOO.',
                             '.....',
                             '.....'],
                            ['.....',
                             '..O..',
                             '..OO.',
                             '..O..',
                             '.....'],
                            ['.....',
                             '.....',
                             '.OOO.',
                             '..O..',
                             '.....'],
                            ['.....',
                             '..O..',
                             '.OO..',
                             '..O..',
                             '.....']]

        self.PIECES = {'S': self.S_SHAPE_TEMPLATE,
                  'Z': self.Z_SHAPE_TEMPLATE,
                  'J': self.J_SHAPE_TEMPLATE,
                  'L': self.L_SHAPE_TEMPLATE,
                  'I': self.I_SHAPE_TEMPLATE,
                  'O': self.O_SHAPE_TEMPLATE,
                  'T': self.T_SHAPE_TEMPLATE}


    def main(self):
        global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT, ulti, noob, DIFFICULTY
        pygame.init()
        FPSCLOCK = pygame.time.Clock()
        DISPLAYSURF = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHEIGHT))
        BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
        BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
        pygame.display.set_caption('TETRIS --> START')
        ulti = BASICFONT.render(
            "PRESS \'R\' to USE Ultimate Skill",
            1,
            (255,255,255))
        noob = False

        pygame.mixer.music.load("music01.ogg")
        pygame.mixer.music.play()
        self.showTextScreen('Tet and Ris')
        while True: # game loop
            noob = False
            self.runGame()
            pygame.mixer.music.stop()
            noob = True
            self.showTextScreen('YOU\'RE NOOB')



    def runGame(self):
        # setup variables for the start of the game

        board = self.getBlankBoard()
        lastMoveDownTime = time.time()
        lastMoveSidewaysTime = time.time()
        lastFallTime = time.time()
        movingDown = False # note: there is no movingUp variable
        movingLeft = False
        movingRight = False
        isulti = False
        imgSURF2 = pygame.image.load('face_'+charNum+'.jpg').convert()
        level, fallFreq = self.calculateLevelAndFallFreq(self.score)

        # pygame.display.flip()

        fallingPiece = self.getNewPiece()
        nextPiece = self.getNewPiece()

        while True: # game loop
            if fallingPiece == None:
                # No falling piece in play, so start a new piece at the top
                fallingPiece = nextPiece
                nextPiece = self.getNewPiece()
                lastFallTime = time.time() # reset lastFallTime

                if not self.isValidPosition(board, fallingPiece):
                    return # can't fit a new piece on the board, so game over

            self.checkForQuit()
            for event in pygame.event.get(): # event handling loop
                if event.type == KEYUP:
                    if (event.key == K_p):
                        # Pausing the game
                        DISPLAYSURF.fill(self.BGCOLOR)
                        pygame.mixer.music.stop()
                        self.showTextScreen('Paused') # pause until a key press
                        pygame.mixer.music.play(-1, 0.0)
                        lastFallTime = time.time()
                        lastMoveDownTime = time.time()
                        lastMoveSidewaysTime = time.time()
                    elif (event.key == K_LEFT or event.key == K_a):
                        movingLeft = False
                    elif (event.key == K_RIGHT or event.key == K_d):
                        movingRight = False
                    elif (event.key == K_DOWN or event.key == K_s):
                        movingDown = False

                elif event.type == KEYDOWN:
                    # moving the piece sideways



                    if (event.key == K_LEFT or event.key == K_a) and self.isValidPosition(board, fallingPiece, adjX=-1):
                        fallingPiece['x'] -= 1
                        movingLeft = True
                        movingRight = False
                        lastMoveSidewaysTime = time.time()

                    elif (event.key == K_RIGHT or event.key == K_d) and self.isValidPosition(board, fallingPiece, adjX=1):
                        fallingPiece['x'] += 1
                        movingRight = True
                        movingLeft = False
                        lastMoveSidewaysTime = time.time()

                    # rotating the piece (if there is room to rotate)
                    elif (event.key == K_UP or event.key == K_w):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(self.PIECES[fallingPiece['shape']])
                        if not self.isValidPosition(board, fallingPiece):
                            fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(self.PIECES[fallingPiece['shape']])
                    elif (event.key == K_q): # rotate the other direction
                        fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(self.PIECES[fallingPiece['shape']])
                        if not self.isValidPosition(board, fallingPiece):
                            fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(self.PIECES[fallingPiece['shape']])

                    elif event.key == K_r:
                        if isulti == True:
                            self.score += self.ultimateSkill(board)
                            isulti = False
                            pygame.display.update()
                            pygame.time.delay(750)

                    # making the piece fall faster with the down key
                    elif (event.key == K_DOWN or event.key == K_s):
                        movingDown = True
                        if self.isValidPosition(board, fallingPiece, adjY=1):
                            fallingPiece['y'] += 1
                        lastMoveDownTime = time.time()

                    # move the current piece all the way down
                    elif event.key == K_SPACE:
                        movingDown = False
                        movingLeft = False
                        movingRight = False
                        for i in range(1, self.BOARDHEIGHT):
                            if not self.isValidPosition(board, fallingPiece, adjY=i):
                                break
                        fallingPiece['y'] += i - 1



            # handle moving the piece because of user input
            if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > self.MOVESIDEWAYSFREQ:
                if movingLeft and self.isValidPosition(board, fallingPiece, adjX=-1):
                    fallingPiece['x'] -= 1
                elif movingRight and self.isValidPosition(board, fallingPiece, adjX=1):
                    fallingPiece['x'] += 1
                lastMoveSidewaysTime = time.time()

            if movingDown and time.time() - lastMoveDownTime > self.MOVEDOWNFREQ and self.isValidPosition(board, fallingPiece, adjY=1):
                fallingPiece['y'] += 1
                lastMoveDownTime = time.time()

            # let the piece fall if it is time to fall
            if time.time() - lastFallTime > fallFreq:
                # see if the piece has landed
                if not self.isValidPosition(board, fallingPiece, adjY=1):
                    # falling piece has landed, set it on the board
                    self.addToBoard(board, fallingPiece)
                    self.score += self.removeCompleteLines(board)
                    level, fallFreq = self.calculateLevelAndFallFreq(self.score)
                    fallingPiece = None
                else:
                    # piece did not land, just move the piece down
                    fallingPiece['y'] += 1
                    lastFallTime = time.time()



            # drawing everything on the screen

            DISPLAYSURF.fill(self.BGCOLOR)
            if self.score %10 == 0 and isulti==False and self.score is not 0 and self.score is not 100:
                isulti=True
                DISPLAYSURF.blit(ulti,(0,0))
            elif isulti==True:
                DISPLAYSURF.blit(ulti,(0,0))
            DISPLAYSURF.blit(imgSURF2,(0,100))
            self.drawBoard(board)
            self.drawStatus(self.score, level)
            self.drawNextPiece(nextPiece)
            if fallingPiece != None:
                self.drawPiece(fallingPiece)

            pygame.display.update()
            FPSCLOCK.tick(self.FPS)


    def makeTextObjs(self,text, font, color):
        surf = font.render(text, True, color)
        return surf, surf.get_rect()


    def terminate(self):
        pygame.quit()
        sys.exit()


    def checkForKeyPress(self):
        # Go through event queue looking for a KEYUP event.
        # Grab KEYDOWN events to remove them from the event queue.
        self.checkForQuit()

        for event in pygame.event.get([KEYDOWN, KEYUP]):
            if event.type == KEYDOWN:
                continue
            return event.key
        return None


    def showTextScreen(self,text):
        # This function displays large text in the
        # center of the screen until a key is pressed.
        # Draw the text drop shadow
        titleSurf, titleRect = self.makeTextObjs(text, BIGFONT, self.TEXTSHADOWCOLOR)
        titleRect.center = (int(self.WINDOWWIDTH / 2), int(self.WINDOWHEIGHT / 2))
        DISPLAYSURF.blit(titleSurf, titleRect)

        # Draw the text
        titleSurf, titleRect = self.makeTextObjs(text, BIGFONT, self.TEXTCOLOR)
        titleRect.center = (int(self.WINDOWWIDTH / 2) - 3, int(self.WINDOWHEIGHT / 2) - 3)
        DISPLAYSURF.blit(titleSurf, titleRect)

        # Draw the additional "Press a key to play." text.
        pressKeySurf, pressKeyRect = self.makeTextObjs('Press a key to play.', BASICFONT, self.TEXTCOLOR)
        pressKeyRect.center = (int(self.WINDOWWIDTH / 2), int(self.WINDOWHEIGHT / 2) + 100)
        DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

        while self.checkForKeyPress() == None:
            pygame.display.update()
            FPSCLOCK.tick()
        if(noob == True):
            if DIFFICULTY == 0:
                self.score = 0
            elif DIFFICULTY == 1:
                self.score = 100
            elif DIFFICULTY == 2:
                self.score = 200
            elif DIFFICULTY == 3:
                self.score = 250




    def checkForQuit(self):
        for event in pygame.event.get(QUIT): # get all the QUIT events
            self.terminate() # terminate if any QUIT events are present
        for event in pygame.event.get(KEYUP): # get all the KEYUP events
            if event.key == K_ESCAPE:
                self.terminate() # terminate if the KEYUP event was for the Esc key
            pygame.event.post(event) # put the other KEYUP event objects back




    def calculateLevelAndFallFreq(self,score):
        # Based on the score, return the level the player is on and
        # how many seconds pass until a falling piece falls one space.
        level = int(score / 10) + 1
        fallFreq = 0.5 - (level * 0.02)
        return level, fallFreq

    def getNewPiece(self):
        # return a random new piece in a random rotation and color
        shape = random.choice(list(self.PIECES.keys()))
        newPiece = {'shape': shape,
                    'rotation': random.randint(0, len(self.PIECES[shape]) - 1),
                    'x': int(self.BOARDWIDTH / 2) - int(self.TEMPLATEWIDTH / 2),
                    'y': -2, # start it above the board (i.e. less than 0)
                    'color': random.randint(0, len(self.COLORS)-1)}
        return newPiece


    def addToBoard(self,board, piece):
        # fill in the board based on piece's location, shape, and rotation
        for x in range(self.TEMPLATEWIDTH):
            for y in range(self.TEMPLATEHEIGHT):
                if self.PIECES[piece['shape']][piece['rotation']][y][x] != self.BLANK:
                    board[x + piece['x']][y + piece['y']] = piece['color']


    def getBlankBoard(self):
        # create and return a new blank board data structure
        board = []
        for i in range(self.BOARDWIDTH):
            board.append([self.BLANK] * self.BOARDHEIGHT)
        return board


    def isOnBoard(self,x, y):
        return x >= 0 and x < self.BOARDWIDTH and y < self.BOARDHEIGHT


    def isValidPosition(self,board, piece, adjX=0, adjY=0):
        # Return True if the piece is within the board and not colliding
        for x in range(self.TEMPLATEWIDTH):
            for y in range(self.TEMPLATEHEIGHT):
                isAboveBoard = y + piece['y'] + adjY < 0
                if isAboveBoard or self.PIECES[piece['shape']][piece['rotation']][y][x] == self.BLANK:
                    continue
                if not self.isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                    return False
                if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != self.BLANK:
                    return False
        return True

    def isCompleteLine(self,board, y):
        # Return True if the line filled with boxes with no gaps.
        for x in range(self.BOARDWIDTH):
            if board[x][y] == self.BLANK:
                return False
        return True


    def removeCompleteLines(self,board):
        # Remove any completed lines on the board, move everything above them down, and return the number of complete lines.
        numLinesRemoved = 0
        y = self.BOARDHEIGHT - 1 # start y at the bottom of the board
        while y >= 0:
            if self.isCompleteLine(board, y):
                # Remove the line and pull boxes down by one line.
                for pullDownY in range(y, 0, -1):
                    for x in range(self.BOARDWIDTH):
                        board[x][pullDownY] = board[x][pullDownY-1]
                # Set very top line to blank.
                for x in range(self.BOARDWIDTH):
                    board[x][0] = self.BLANK
                numLinesRemoved += 1
                # Note on the next iteration of the loop, y is the same.
                # This is so that if the line that was pulled down is also
                # complete, it will be removed.
            else:
                y -= 1 # move on to check next row up
        return numLinesRemoved


    def convertToPixelCoords(self,boxx, boxy):
        # Convert the given xy coordinates of the board to xy
        # coordinates of the location on the screen.
        return (self.XMARGIN + (boxx * self.BOXSIZE)), (self.TOPMARGIN + (boxy * self.BOXSIZE))


    def drawBox(self,boxx, boxy, color, pixelx=None, pixely=None):
        # draw a single box (each tetromino piece has four boxes)
        # at xy coordinates on the board. Or, if pixelx & pixely
        # are specified, draw to the pixel coordinates stored in
        # pixelx & pixely (this is used for the "Next" piece).
        if color == self.BLANK:
            return
        if pixelx == None and pixely == None:
            pixelx, pixely = self.convertToPixelCoords(boxx, boxy)
        pygame.draw.rect(DISPLAYSURF, self.COLORS[color], (pixelx + 1, pixely + 1, self.BOXSIZE - 1, self.BOXSIZE - 1))
        pygame.draw.rect(DISPLAYSURF, self.LIGHTCOLORS[color], (pixelx + 1, pixely + 1, self.BOXSIZE - 4, self.BOXSIZE - 4))


    def drawBoard(self,board):
        # draw the border around the board
        pygame.draw.rect(DISPLAYSURF, self.BORDERCOLOR, (self.XMARGIN - 3, self.TOPMARGIN - 7, (self.BOARDWIDTH * self.BOXSIZE) + 8, (self.BOARDHEIGHT * self.BOXSIZE) + 8), 5)

        # fill the background of the board
        pygame.draw.rect(DISPLAYSURF, self.BGCOLOR, (self.XMARGIN, self.TOPMARGIN, self.BOXSIZE * self.BOARDWIDTH, self.BOXSIZE * self.BOARDHEIGHT))
        # draw the individual boxes on the board
        for x in range(self.BOARDWIDTH):
            for y in range(self.BOARDHEIGHT):
                self.drawBox(x, y, board[x][y])


    def drawStatus(self,score, level):
        # draw the score text
        scoreSurf = BASICFONT.render('Score: %s' % score, True, self.TEXTCOLOR)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (self.WINDOWWIDTH - 150, 20)
        DISPLAYSURF.blit(scoreSurf, scoreRect)

        # draw the level text
        levelSurf = BASICFONT.render('Level: %s' % level, True, self.TEXTCOLOR)
        levelRect = levelSurf.get_rect()
        levelRect.topleft = (self.WINDOWWIDTH - 150, 50)
        DISPLAYSURF.blit(levelSurf, levelRect)


    def drawPiece(self,piece, pixelx=None, pixely=None):
        shapeToDraw = self.PIECES[piece['shape']][piece['rotation']]
        if pixelx == None and pixely == None:
            # if pixelx & pixely hasn't been specified, use the location stored in the piece data structure
            pixelx, pixely = self.convertToPixelCoords(piece['x'], piece['y'])

        # draw each of the boxes that make up the piece
        for x in range(self.TEMPLATEWIDTH):
            for y in range(self.TEMPLATEHEIGHT):

                if shapeToDraw[y][x] != self.BLANK:
                    self.drawBox(None, None, piece['color'], pixelx + (x * self.BOXSIZE), pixely + (y * self.BOXSIZE))


    def drawNextPiece(self,piece):
        # draw the "next" text
        nextSurf = BASICFONT.render('Next:', True, self.TEXTCOLOR)
        nextRect = nextSurf.get_rect()
        nextRect.topleft = (self.WINDOWWIDTH - 120, 80)
        DISPLAYSURF.blit(nextSurf, nextRect)
        # draw the "next" piece
        self.drawPiece(piece, pixelx=self.WINDOWWIDTH-120, pixely=100)


    # if __name__ == '__main__':
    #     main()


    def ultimateSkill(self,board):
        usingUlti = BIGFONT.render(
            "BLOCK CRASH",
            1,

            (255,255,255))
        imgNum = 'char'+charNum+'.jpg'
        imgSURF = pygame.image.load(imgNum).convert()


        DISPLAYSURF.blit(imgSURF,(int(self.WINDOWWIDTH/2)-300,int(self.WINDOWHEIGHT/2)-40))
        effectSound = pygame.mixer.Sound('effect'+soundNum+'.wav')
        pygame.mixer.Sound.play(effectSound)


        if self.score is not 0 and self.score is not 100:
            DISPLAYSURF.blit(usingUlti,(int(self.WINDOWWIDTH/2)-380,int(self.WINDOWHEIGHT/2)-40))
            for y in range(self.BOARDHEIGHT):
                for x in range(self.BOARDWIDTH):
                    board[x][y] = self.BLANK
            return 1

        else:
            return 0




class Menu:
    global charNum,soundNum
    charNum='00'
    soundNum='00'
    lista = []
    pola = []
    rozmiar_fontu = 32
    font_path = 'data/coders_crux/coders_crux.ttf'
    font = pygame.font.Font
    dest_surface = pygame.Surface
    ilosc_pol = 0
    kolor_tla = (51,51,51)
    kolor_tekstu =  (255, 255, 153)
    kolor_zaznaczenia = (153,102,255)
    pozycja_zaznaczenia = 0
    pozycja_wklejenia = (0,0)
    menu_width = 0
    menu_height = 0

    class Pole:
        tekst = ''
        pole = pygame.Surface
        pole_rect = pygame.Rect
        zaznaczenie_rect = pygame.Rect

    def move_menu(self, top, left):
        self.pozycja_wklejenia = (top,left)

    def set_colors(self, text, selection, background):
        self.kolor_tla = background
        self.kolor_tekstu =  text
        self.kolor_zaznaczenia = selection

    def set_fontsize(self,font_size):
        self.rozmiar_fontu = font_size

    def set_font(self, path):
        self.font_path = path

    def get_position(self):
        return self.pozycja_zaznaczenia

    def init(self, lista, dest_surface):
        self.lista = lista
        self.dest_surface = dest_surface
        self.ilosc_pol = len(self.lista)
        self.stworz_strukture()

    def draw(self,przesun=0):
        if przesun:
            self.pozycja_zaznaczenia += przesun
            if self.pozycja_zaznaczenia == -1:
                self.pozycja_zaznaczenia = self.ilosc_pol - 1
            self.pozycja_zaznaczenia %= self.ilosc_pol
        menu = pygame.Surface((self.menu_width, self.menu_height))
        menu.fill(self.kolor_tla)
        zaznaczenie_rect = self.pola[self.pozycja_zaznaczenia].zaznaczenie_rect
        pygame.draw.rect(menu,self.kolor_zaznaczenia,zaznaczenie_rect)

        for i in range(self.ilosc_pol):
            menu.blit(self.pola[i].pole,self.pola[i].pole_rect)
        self.dest_surface.blit(menu,self.pozycja_wklejenia)
        return self.pozycja_zaznaczenia

    def stworz_strukture(self):
        przesuniecie = 0
        self.menu_height = 0
        self.font = pygame.font.Font(self.font_path, self.rozmiar_fontu)
        for i in range(self.ilosc_pol):
            self.pola.append(self.Pole())
            self.pola[i].tekst = self.lista[i]
            self.pola[i].pole = self.font.render(self.pola[i].tekst, 1, self.kolor_tekstu)

            self.pola[i].pole_rect = self.pola[i].pole.get_rect()
            przesuniecie = int(self.rozmiar_fontu * 0.2)

            height = self.pola[i].pole_rect.height
            self.pola[i].pole_rect.left = przesuniecie
            self.pola[i].pole_rect.top = przesuniecie+(przesuniecie*2+height)*i

            width = self.pola[i].pole_rect.width+przesuniecie*2
            height = self.pola[i].pole_rect.height+przesuniecie*2
            left = self.pola[i].pole_rect.left-przesuniecie
            top = self.pola[i].pole_rect.top-przesuniecie

            self.pola[i].zaznaczenie_rect = (left,top ,width, height)
            if width > self.menu_width:
                    self.menu_width = width
            self.menu_height += height
        x = self.dest_surface.get_rect().centerx - self.menu_width / 2
        y = self.dest_surface.get_rect().centery - self.menu_height / 2
        mx, my = self.pozycja_wklejenia
        self.pozycja_wklejenia = (x+mx, y+my)


if __name__ == '__main__':
    import sys
    surface = pygame.display.set_mode((854,480)) #0,6671875 and 0,(6) of HD resoultion
    surface.fill((51,51,51))
    '''First you have to make an object of a *Menu class.
    *init take 2 arguments. List of fields and destination surface.
    Then you have a 4 configuration options:
    *set_colors will set colors of menu (text, selection, background)
    *set_fontsize will set size of font.
    *set_font take a path to font you choose.
    *move_menu is quite interseting. It is only option which you can use before
    and after *init statement. When you use it before you will move menu from
    center of your surface. When you use it after it will set constant coordinates.
    Uncomment every one and check what is result!
    *draw will blit menu on the surface. Be carefull better set only -1 and 1
    arguments to move selection or nothing. This function will return actual
    position of selection.
    *get_postion will return actual position of seletion. '''
    menu = Menu()#necessary
    #menu.set_colors((255,255,255), (0,0,255), (0,0,0))#optional
    #menu.set_fontsize(64)#optional
    #menu.set_font('data/couree.fon')#optional
    #menu.move_menu(100, 99)#optional

    menu.init(['Game Start','Difficulty','Character','Quit'], surface)#necessary
    pygame.display.set_caption('TetandRis MENU')

    #menu.move_menu(0, 0)#optional
    menu.draw()#necessary
    tmp=0
    tmp2=0
    pygame.key.set_repeat(199,69)#(delay,interval)
    pygame.display.update()
    tet = Tetandris()
    while 1:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    menu.draw(-1) #here is the Menu class function
                if event.key == K_DOWN:
                    menu.draw(1) #here is the Menu class function
                if event.key == K_RETURN:



                    if menu.get_position() == 3:#here is the Menu class function
                        pygame.display.quit()
                        sys.exit()
                    if menu.get_position() == 0:
                        tet.main()
                    if menu.get_position() == 1:

                        # surface = pygame.display.set_mode((854,480))
                        surface.fill((51,51,51))
                        menu.init(['Easy','Normal','Hard','Hell'],surface)
                        menu.move_menu(395,200)
                        menu.draw()

                        pygame.display.update()
                        # tmp =0
                        while 1:

                            for event in pygame.event.get():
                                if event.type == KEYDOWN:
                                    if event.key == K_UP:
                                        menu.draw(-1) #here is the Menu class function
                                    if event.key == K_DOWN:
                                        menu.draw(1) #here is the Menu class function
                                    if event.key == K_RETURN:
                                        if menu.get_position() == 3:
                                            tet.score = 250
                                            DIFFICULTY = 3
                                        if menu.get_position() == 0:
                                            tet.score = 0
                                            DIFFICULTY = 0

                                            # pygame.display.quit()

                                        if menu.get_position() == 1:
                                            tet.score= 100
                                            DIFFICULTY = 1

                                            # pygame.display.update()


                                        if menu.get_position() == 2:
                                            tet.score = 200
                                            DIFFICULTY = 2



                                            # pygame.display.update()

                                        tmp=1
                                        surface.fill((51,51,51))
                                        menu.move_menu(0,0)
                                        menu.init(['Game Start','Difficulty','Character','Quit'], surface)
                                        menu.draw()
                                        pygame.display.update()




                                    if event.key == K_ESCAPE:
                                        pygame.display.quit()
                                        sys.exit()

                                    pygame.display.update()
                                elif event.type == QUIT:
                                    pygame.display.quit()
                                    sys.exit()
                                if tmp==1:
                                    break


                            pygame.time.wait(8)
                            if tmp==1:
                                break
                    if menu.get_position() == 2:
                        surface.fill((51,51,51))
                        menu.init(['Genzi','Naruto'],surface)
                        menu.move_menu(395,200)
                        menu.draw()
                        global effectSound
                        pygame.display.update()
                        # tmp2 =0
                        while 1:

                            for event in pygame.event.get():
                                if event.type == KEYDOWN:
                                    if event.key == K_UP:
                                        menu.draw(-1) #here is the Menu class function
                                    if event.key == K_DOWN:
                                        menu.draw(1) #here is the Menu class function
                                    if event.key == K_RETURN:
                                        if menu.get_position() == 0:
                                            charNum = '00'
                                            soundNum = '00'


                                            # pygame.display.quit()

                                        if menu.get_position() == 1:
                                            charNum = '01'
                                            soundNum = '01'

                                        # if menu.get_position() == 2:
                                        #     charNum = '01'
                                        # if menu.get_position() == 3:
                                        #     charNum = '01'

                                            # pygame.display.update()


                                            # pygame.display.update()

                                        tmp2=1
                                        surface.fill((51,51,51))
                                        menu.move_menu(0,0)
                                        menu.init(['Game Start','Difficulty','Character','Quit'], surface)
                                        menu.draw()
                                        pygame.display.update()




                                    if event.key == K_ESCAPE:
                                        pygame.display.quit()
                                        sys.exit()

                                    pygame.display.update()

                                if tmp2==1:
                                    break


                            pygame.time.wait(8)
                            if tmp2==1:
                                break


                if event.key == K_ESCAPE:
                    pygame.display.quit()
                    sys.exit()

                pygame.display.update()
            elif event.type == QUIT:
                pygame.display.quit()
                sys.exit()


        pygame.time.wait(8)
