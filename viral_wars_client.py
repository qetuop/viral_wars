import pygame, sys
from pygame.locals import *
import math
import zmq
import viral_pb2

class Game():
    def __init__(self):
        self.numPlayers = 1
        self.currPlayer = PLAYER1

class Board():
    def __init__(self, rows, cols):
        self.currBoard = []   # row major
        self.rows = rows
        self.cols = cols

        for row in range(self.rows):
            self.currBoard.append([])
            for col in range(self.cols):
                self.currBoard[row].append(STD)

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

#useful game dimensions
TILESIZE  = 80
MAPWIDTH  = 3
MAPHEIGHT = 3

def writeBoard(gameBoard, currBoard):
    for row in range(MAPHEIGHT):
        for col in range(MAPWIDTH):
            gameBoard.data.append(currBoard[col][row])

def readBoard(gameBoard, currBoard):
    for row in range(gameBoard.rows):
        for col in range(gameBoard.cols):
            currBoard[col][row] = gameBoard.data[row*gameBoard.cols+col]

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


#set up the display
pygame.init()
DISPLAYSURF = pygame.display.set_mode( (MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE +100)  )



#add a font for our inventory
INVFONT = pygame.font.Font('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', 18)

#the player image
player1 = Player(1)
currentPlayer = player1

board = Board(3,3)

temp_pieceSelected = False

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
            x = int(math.floor(x_pos/TILESIZE))
            y = int(math.floor(y_pos/TILESIZE))
            #print (x_pos, y_pos), (x,y)

            # contain player
            if ( currBoard[x][y] == PLAYER1 ):

                # is it the currenly selected piece
                if ( currentPlayer.isSelected == True and currentPlayer.selectedPos == (x,y) ):
                    currentPlayer.setSelected(False, (x,y))
                    temp_pieceSelected = False
                    print "unsel:", (x, y)
                else:
                    currentPlayer.setSelected(True, (x, y))
                    temp_pieceSelected = True
                    print "sel:",(x,y)

            # if empty, move piece
            elif (temp_pieceSelected == True and currBoard[x][y] == EMPTY ):
                print "MOVE TO", x,y
                # get the coords of the selected piece
                a= currentPlayer.selectedPos[0]
                b=currentPlayer.selectedPos[1]
                currBoard[x][y] = PLAYER1
                currentPlayer.setSelected(False, (a, b)) # unselect the original/new piece
                temp_pieceSelected = False

                dist = math.sqrt( math.pow(x-a, 2) + math.pow(y-b, 2) )
                print 'dist', dist
                # if jump
                if ( dist > math.sqrt(2) ):
                    currBoard[a][b] = EMPTY
                    print 'empty'
                elif ( dist == 1.0 ):
                    pass #currBoard[a][b] = EMPTY


            print "CB Req:  ", currBoard

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

            print "CB Resp: ",currBoard



    #loop through each row
    for row in range(MAPHEIGHT):                # row/height == Y
        #loop through each column in the row
        for column in range(MAPWIDTH):          # column/width == X
            #draw the resource at that position in the tilemap, using the correct image
            DISPLAYSURF.blit(textures[tilemap[column][row]], (column*TILESIZE,row*TILESIZE))


            # display the player
            if ( currBoard[column][row] == PLAYER1 ):

                if ( currentPlayer.selectedPos == (column,row) and temp_pieceSelected ):
                    DISPLAYSURF.blit(currentPlayer.selected, (column * TILESIZE, row * TILESIZE))
                else:
                    DISPLAYSURF.blit(currentPlayer.normal, (column * TILESIZE, row * TILESIZE))

            # print cell coords
            if (1):
                textObj = INVFONT.render('(%d,%d)'%(column,row), True, WHITE, GREEN)
                DISPLAYSURF.blit(textObj, (column * TILESIZE + 20, row*TILESIZE+20))


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
