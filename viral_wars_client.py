import pygame, sys
from pygame.locals import *
import math
import zmq
import viral_pb2

class Game():
    def __init__(self):
        self.numPlayers = 0
        self.currPlayer = PLAYER_NONE
        self.playerSelected = False  # is a player piece selected, can i remove this
        self.playerDict = {}

    def addPlayer(self,playerNum):
        self.playerDict[playerNum] =  Player(playerNum)
        self.numPlayers += 1

    def removePlayer(self,playerNum):
        try:
            self.playerDict.pop(playerNum,None)
            self.numPlayers -= 1
        except:
            pass

    def setCurrPlayer(self,playerNum):
        self.currPlayer = playerNum

    def getCurrPlayer(self):
        return self.playerDict[self.currPlayer]

    def getPlayer(self,playerNum):
        player = None
        try:
            player =  self.playerDict[playerNum]
        except:
            pass
        return player

    # what if more players
    def nextPlayerTurn(self):
        if self.currPlayer == 1:
            self.setCurrPlayer(2)
        elif self.currPlayer == 2:
            self.setCurrPlayer(1)

class Board():
    def __init__(self, rows, cols):
        #self.currBoard = []   # row major
        self.tiles = []
        self.players = []
        self.rows = rows
        self.cols = cols

        for row in range(self.rows):
            #self.currBoard.append([])
            self.tiles.append([])
            self.players.append([])
            for col in range(self.cols):
                #self.currBoard[row].append(TILE_STD)
                self.tiles[row].append(TILE_STD)
                self.players[row].append(PLAYER_NONE)

    # rox, col = last move
    def updateBoard(self, row, col):

        for drow in range(-1,2):
            for dcol in range(-1,2):
                if ( (row+drow < self.rows and row+drow >= 0) and (col+dcol < self.cols and col+dcol >= 0)):
                    if self.players[row+drow][col+dcol] != PLAYER_NONE:
                        self.players[row + drow][col + dcol] = self.players[row][col]

    '''
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
    '''
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

# moar constants
PLAYER_NONE = 0
PLAYER_1    = 1
PLAYER_2    = 2


# temp constants
TILE_EMPTY   = 0 # no tile
TILE_STD     = 1 # standard tile
TILE_PLAYER1 = 2
TILE_PLAYER2 = 3
TILE_BLOCK   = 4 # TILE_BLOCKed tile

#a dictionary linking resources to textures
textures =   {
                TILE_STD    : pygame.image.load('std.png'),
                TILE_BLOCK  : pygame.image.load('block.png')
            }

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

# The Board
rowCnt = 5
colCnt = 5
board = Board(rowCnt,colCnt)
board.tiles[1][2] = TILE_BLOCK
board.players[0][0] = PLAYER_1
board.players[rowCnt-1][colCnt-1] = PLAYER_2

# set up the display
pygame.init()

# Main display
DISPLAYSURF = pygame.display.set_mode( (board.rows*TILESIZE, board.cols*TILESIZE +100)  )
DISPLAYSURF.fill(GREEN)

###  !! can't do anything with Player class until the main display is set !!

# The Game
game = Game()
game.addPlayer(PLAYER_1)
game.addPlayer(PLAYER_2)
game.setCurrPlayer(PLAYER_1)

# add a font for our inventory
INVFONT = pygame.font.Font('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', 18)

pygame.display.set_caption('ATTAX')
#pygame.display.set_icon(TILE_PLAYER1.image)


#print board.currBoard
print 'Players', board.players
print 'Tiles', board.tiles

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

            currentPlayer = game.getCurrPlayer()

            # TODO: make function
            (x_pos,y_pos) = pygame.mouse.get_pos()
            col = int(math.floor(x_pos/TILESIZE))   # column is along the X plane
            row = int(math.floor(y_pos/TILESIZE))   # row is along the y plane
            #print (x_pos, y_pos), (x,y)


            # if empty/block ?

            # contain player (or opponent?)
            if ( board.players[row][col] == game.currPlayer ):

                # is it the currently selected piece
                if ( currentPlayer.isSelected == True and currentPlayer.selectedPos == (row, col) ):
                    currentPlayer.setSelected(False, (row,col))
                    game.playerSelected = False
                    print "unsel:", (row,col)
                else:
                    currentPlayer.setSelected(True, (row,col))
                    game.playerSelected = True
                    print "sel:",(row,col)

            # if TILE_EMPTY, move piece - a piece will only be selected if the above if first triggered
            elif (game.playerSelected == True and board.tiles[row][col] == TILE_STD):
                print "MOVE TO", row,col
                # get the coords of the selected piece
                row_orig = currentPlayer.selectedPos[0]
                col_orig = currentPlayer.selectedPos[1]
                board.players[row][col] = game.currPlayer
                currentPlayer.setSelected(False, (row, col)) # unselect the original/new piece

                dist = math.sqrt( math.pow(row-row_orig, 2) + math.pow(col-col_orig, 2) )
                print 'dist', dist
                # if jump
                if ( dist > math.sqrt(2) ):
                    board.tiles[row][col] = game.currPlayer
                    board.tiles[row_orig][col_orig] = TILE_STD
                    board.players[row_orig][col_orig] = PLAYER_NONE
                    print 'TILE_EMPTY'
                elif ( dist == 1.0 ):
                    pass #currBoard[a][b] = TILE_STD

                # update board
                board.updateBoard(row,col)

                game.playerSelected = False
                game.nextPlayerTurn()

            print "CB Req:  ", board.players

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

            print "CB Resp: ",board.players



    # loop through each row
    for row in range(board.rows):                # row/height == Y
        #loop through each column in the row
        for col in range(board.cols):             # column/width == X

            # !! col = X coord, row = Y coord --> draw at (col,row) !!

            # move out of loop
            currentPlayer = game.getCurrPlayer()

            # Draw the Tile
            if (board.tiles[row][col] == TILE_EMPTY):
                pass
            else:
                DISPLAYSURF.blit(textures[TILE_STD], (col * TILESIZE, row * TILESIZE))

            #if ( board.currBoard[row][col] == TILE_BLOCK ):
            if (board.tiles[row][col] == TILE_BLOCK):
                DISPLAYSURF.blit(textures[TILE_BLOCK], (col * TILESIZE, row * TILESIZE))

            # Draw the Player
            try:
                player = game.getPlayer(board.players[row][col])

                if ( currentPlayer.selectedPos == (row,col) and game.playerSelected == True ):
                    DISPLAYSURF.blit(player.selected, (col * TILESIZE, row * TILESIZE))
                else:
                    DISPLAYSURF.blit(player.normal, (col * TILESIZE, row * TILESIZE))
            except:
                pass

            # print cell coords
            if (1):
                textObj = INVFONT.render('(%d,%d)'%(row,col), True, WHITE, GREEN)
                DISPLAYSURF.blit(textObj, (col * TILESIZE + 20, row*TILESIZE+20))

    # Score, starting 10 pixels in
    placePosition = 10

    # add the image
    player = game.getCurrPlayer()
    DISPLAYSURF.blit(player.normal, (placePosition, board.rows * TILESIZE + 20))
    #placePosition += 30
    # add the text showing the amount in the inventory
    #textObj = INVFONT.render(, True, WHITE, GREEN)
    #DISPLAYSURF.blit(textObj, (placePosition, MAPHEIGHT * TILESIZE + 20))
    #placePosition += 50


    #update the display
    pygame.display.update()

    #QUIT = True
