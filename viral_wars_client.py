import pygame, sys
from pygame.locals import *
import math
import zmq
import viral_pb2

class Game():
    def __init__(self):
        self.numPlayers = 1
        self.currPlayer = PLAYER1
        self.playerSelected = False

class Board():
    def __init__(self, rows, cols):
        self.currBoard = []   # row major
        self.rows = rows
        self.cols = cols

        for row in range(self.rows):
            self.currBoard.append([])
            for col in range(self.cols):
                self.currBoard[row].append(STD)

    def writeBoardToBuf(self, gameBoard):
        for row in range(self.rows):
            for col in range(self.cols):
                gameBoard.data.append(self.board[row][col])

    def readBoardFromBuf(self, gameBoard):
        for row in range(gameBoard.rows):
            self.currBoard.append([])
            for col in range(gameBoard.cols):
                self.currBoard[row].append(gameBoard.data[row * gameBoard.cols + col])
                #self.board[row][col] = gameBoard.data[row * gameBoard.cols + col]

class Player():
    def __init__(self, playerNum):
        self.normal = pygame.image.load('player%d.png' % playerNum).convert_alpha()
        self.selected = pygame.image.load('player%d_selected.png' % playerNum).convert_alpha()
        self.image = self.normal
        self.selectedPos = (0,0) # selected position (if selected)
        self.isSelected = False # is a piece selected

    def setSelected(self, value, coords):
        if ( value == True ):
            self.isSelected = True
            self.image = self.selected
        elif ( value == False ):
            self.isSelected = False
            self.image = self.normal

        self.selectedPos = coords



#constants representing colours
BLACK = (0,   0,   0  )
WHITE = (255, 255, 255)
BROWN = (153, 76,  0  )
GREEN = (0,   255, 0  )
BLUE  = (0,   0,   255)

# temp constants
EMPTY   = 0 # no tile
STD     = 1 # standard tile
PLAYER1 = 2
PLAYER2 = 3
BLOCK   = 4 # blocked tile

#a dictionary linking resources to textures
textures =   {
                STD    : pygame.image.load('std.png'),
                BLOCK  : pygame.image.load('block.png')
            }
'''
#a list representing our tilemap
tilemap = [
            [STD, STD, STD, ],
            [STD, STD, STD  ],
            [STD, STD, STD  ]
          ]

# can this be merged with the tile map?
currBoard = [
    [PLAYER1, EMPTY, EMPTY, ],
    [EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY]
]
'''
#useful game dimensions
TILESIZE  = 80
#MAPWIDTH  = 3
#MAPHEIGHT = 3



################################
##
##      MAIN
##
################################
# ZeroMQ Context
context = zmq.Context()

# Define the socket using the "Context"
sock = context.socket(zmq.REQ)
sock.connect("tcp://127.0.0.1:5678")



# The Game
game = Game()

# The Board
board = Board(3,3)
board.currBoard[0][0] = PLAYER1
board.currBoard[1][2] = BLOCK


# set up the display
pygame.init()

# Main display
DISPLAYSURF = pygame.display.set_mode( (board.rows*TILESIZE, board.cols*TILESIZE +100)  )
DISPLAYSURF.fill(GREEN)

# add a font for our inventory
INVFONT = pygame.font.Font('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', 18)

# The Players
player1 = Player(1)
currentPlayer = player1




# temp_pieceSelected = False

#the position of the player [x,y]
#playerPos = [0,0]

pygame.display.set_caption('ATTAX')
pygame.display.set_icon(player1.image)


#isPlayerSelected = False
#QUIT = False
while (True):

    # get all the user events
    for event in pygame.event.get():
        #print(event)

        # if the user wants to quit
        if event.type == QUIT:
            # and the game and close the window
            pygame.quit()
            sys.exit()

        # if mouse
        elif event.type == MOUSEBUTTONUP:

            # TODO: make function
            (x_pos,y_pos) = pygame.mouse.get_pos()
            col = int(math.floor(x_pos/TILESIZE))   # column is along the X plane
            row = int(math.floor(y_pos/TILESIZE))   # row is along the y plane
            #print (x_pos, y_pos), (x,y)

            # contain player (or opponent?)
            if ( board.currBoard[row][col] == PLAYER1 ):

                # is it the currently selected piece
                if ( currentPlayer.isSelected == True and currentPlayer.selectedPos == (row, col) ):
                    currentPlayer.setSelected(False, (row,col))
                    game.playerSelected = False
                    print "unsel:", (row,col)
                else:
                    currentPlayer.setSelected(True, (row,col))
                    game.playerSelected = True
                    print "sel:",(row,col)

            # if empty, move piece
            elif (game.playerSelected == True and board.currBoard[row][col] == STD ):
                print "MOVE TO", row,col
                # get the coords of the selected piece
                row_orig = currentPlayer.selectedPos[0]
                col_orig = currentPlayer.selectedPos[1]
                board.currBoard[row][col] = game.currPlayer
                currentPlayer.setSelected(False, (row, col)) # unselect the original/new piece
                game.playerSelected = False

                dist = math.sqrt( math.pow(row-row_orig, 2) + math.pow(col-col_orig, 2) )
                print 'dist', dist
                # if jump
                if ( dist > math.sqrt(2) ):
                    board.currBoard[row][col] = game.currPlayer
                    board.currBoard[row_orig][col_orig] = STD
                    print 'empty'
                elif ( dist == 1.0 ):
                    pass #currBoard[a][b] = STD


            print "CB Req:  ", board.currBoard

            '''  TODO: Bring back in talking to server later
            # Send a "message" using the socket
            gameBoard = viral_pb2.GameBoard()
            gameBoard.rows = 3
            gameBoard.cols = 3
            #gameBoard.datadata[i*cols+j] = 0
            #print viral_pb2.GameBoard
            #gameBoard.data.append(0)

            writeBoard(gameBoard, currBoard)

            sock.send(gameBoard.SerializeToString())
            message =  sock.recv()

            try:
                gameBoard.ParseFromString(message)
                print "GB:", gameBoard.data
                readBoard(gameBoard, currBoard)

            except:
                print sys.exc_info()
            '''

            print "CB Resp: ",board.currBoard



    #loop through each row
    for row in range(board.rows):                # row/height == Y
        #loop through each column in the row
        for col in range(board.cols):             # column/width == X

            # !! col = X coord, row = Y coord --> draw at (col,row) !!

            if ( board.currBoard[row][col] == EMPTY ):
                pass
            else:
                DISPLAYSURF.blit(textures[STD], (col * TILESIZE, row * TILESIZE))

            if ( board.currBoard[row][col] == BLOCK ):
                DISPLAYSURF.blit(textures[BLOCK], (col * TILESIZE, row * TILESIZE))

            # display the player
            if ( board.currBoard[row][col] == PLAYER1 ):

                if ( currentPlayer.selectedPos == (row,col) and game.playerSelected == True ):
                    DISPLAYSURF.blit(currentPlayer.selected, (col * TILESIZE, row * TILESIZE))
                else:
                    DISPLAYSURF.blit(currentPlayer.normal, (col * TILESIZE, row * TILESIZE))

            # print cell coords
            if (1):
                textObj = INVFONT.render('(%d,%d)'%(row,col), True, WHITE, GREEN)
                DISPLAYSURF.blit(textObj, (col * TILESIZE + 20, row*TILESIZE+20))


    '''
    # Score, starting 10 pixels in
    placePosition = 10

    # add the image
    DISPLAYSURF.blit(PLAYER, (placePosition, MAPHEIGHT * TILESIZE + 20))
    placePosition += 30
    # add the text showing the amount in the inventory
    textObj = INVFONT.render(str(1), True, WHITE, GREEN)
    DISPLAYSURF.blit(textObj, (placePosition, MAPHEIGHT * TILESIZE + 20))
    placePosition += 50
    '''

    #update the display
    pygame.display.update()

    #QUIT = True
