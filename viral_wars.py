import pygame, sys
from pygame.locals import *
import math

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

#constants representing the different tiles
STD  = 0
#GRASS = 1
#WATER = 2
#COAL  = 3

# temp constans
EMPTY = 0
PLAYER1 = 1
PLAYER2 = 2

#a dictionary linking resources to textures
textures =   {
                STD  : pygame.image.load('1x1.png')
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


#set up the display
pygame.init()
DISPLAYSURF = pygame.display.set_mode( (MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE +100)  )



#add a font for our inventory
INVFONT = pygame.font.Font('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', 18)

#the player image
player1 = Player(1)
currentPlayer = player1

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
        # if a key is pressed
        elif event.type == KEYDOWN:
            # if the right arrow is pressed
            if (event.key == K_RIGHT) and currentPlayer.playerPos[0] < MAPWIDTH - 1:
                # change the player's x position
                currentPlayer.playerPos[0] += 1
            # if the right arrow is pressed
            elif (event.key == K_LEFT) and currentPlayer.playerPos[0] > 0:
                # change the player's x position
                currentPlayer.playerPos[0] -= 1
            # if the right arrow is pressed
            elif (event.key == K_DOWN) and currentPlayer.playerPos[1] < MAPHEIGHT - 1:
                # change the player's x position
                currentPlayer.playerPos[1] += 1
            # if the right arrow is pressed
            elif (event.key == K_UP) and currentPlayer.playerPos[1] > 0:
                # change the player's x position
                currentPlayer.playerPos[1] -= 1
        elif event.type == MOUSEBUTTONUP:
            (x_pos,y_pos) = pygame.mouse.get_pos()
            x = int(math.floor(x_pos/TILESIZE))
            y = int(math.floor(y_pos/TILESIZE))
            #print (x_pos, y_pos), (x,y)

            # contain player
            if ( currBoard[x][y] == PLAYER1 ):

                # is it the currenly selected piece
                if ( currentPlayer.isSelected == True and currentPlayer.selectedPos == (x,y) ):
                    currentPlayer.setSelected(False, (x,y))
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
                    print 'empth'
                elif ( dist == 1.0 ):
                    pass #currBoard[a][b] = EMPTY

            print "CB:",currBoard



    #loop through each row
    for row in range(MAPHEIGHT):                # !!! = Y
        #loop through each column in the row
        for column in range(MAPWIDTH):          # !!! = X
            #draw the resource at that position in the tilemap, using the correct image
            DISPLAYSURF.blit(textures[tilemap[column][row]], (column*TILESIZE,row*TILESIZE))


            # display the player
            if ( currBoard[column][row] == PLAYER1 ):

                if ( currentPlayer.selectedPos == (column,row) and temp_pieceSelected ):
                    DISPLAYSURF.blit(currentPlayer.selected, (column * TILESIZE, row * TILESIZE))
                else:
                    DISPLAYSURF.blit(currentPlayer.normal, (column * TILESIZE, row * TILESIZE))


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
