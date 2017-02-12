import pygame, sys
from pygame.locals import *
import math

#constants representing colours
BLACK = (0,   0,   0  )
WHITE = (255, 255, 255)
BROWN = (153, 76,  0  )
GREEN = (0,   255, 0  )
BLUE  = (0,   0,   255)

#constants representing the different tiles
STD  = 0
GRASS = 1
WATER = 2
COAL  = 3

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
PLAYER = pygame.image.load('player1.png').convert_alpha()

#the position of the player [x,y]
playerPos = [0,0]

pygame.display.set_caption('ATTAX')
pygame.display.set_icon(PLAYER)

while True:

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
            if (event.key == K_RIGHT) and playerPos[0] < MAPWIDTH - 1:
                # change the player's x position
                playerPos[0] += 1
            # if the right arrow is pressed
            elif (event.key == K_LEFT) and playerPos[0] > 0:
                # change the player's x position
                playerPos[0] -= 1
            # if the right arrow is pressed
            elif (event.key == K_DOWN) and playerPos[1] < MAPHEIGHT - 1:
                # change the player's x position
                playerPos[1] += 1
            # if the right arrow is pressed
            elif (event.key == K_UP) and playerPos[1] > 0:
                # change the player's x position
                playerPos[1] -= 1
        elif event.type == MOUSEBUTTONUP:
            (x_pos,y_pos) = pygame.mouse.get_pos()
            x = math.floor(x_pos/TILESIZE)
            y = math.floor(y_pos/TILESIZE)
            print (x_pos, y_pos), (x,y)
            playerPos[0] = x
            playerPos[1] = y


    #loop through each row
    for row in range(MAPHEIGHT):
        #loop through each column in the row
        for column in range(MAPWIDTH):
            #draw the resource at that position in the tilemap, using the correct image
            DISPLAYSURF.blit(textures[tilemap[row][column]], (column*TILESIZE,row*TILESIZE))

    # display the player at the correct position
    DISPLAYSURF.blit(PLAYER, (playerPos[0] * TILESIZE, playerPos[1] * TILESIZE))


    # Score, starting 10 pixels in
    placePosition = 10

    # add the image
    DISPLAYSURF.blit(PLAYER, (placePosition, MAPHEIGHT * TILESIZE + 20))
    placePosition += 30
    # add the text showing the amount in the inventory
    textObj = INVFONT.render(str(1), True, WHITE, GREEN)
    DISPLAYSURF.blit(textObj, (placePosition, MAPHEIGHT * TILESIZE + 20))
    placePosition += 50


    #update the display
    pygame.display.update()