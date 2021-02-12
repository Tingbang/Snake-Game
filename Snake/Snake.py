#Darren Lally Advanced Higher Computing Science Project

import pygame #Importing pygame module
import time   #Importing time function
import random #Importing random function
import sys

pygame.init() #Initialising the module
pygame.mixer.init() #Initialises pygames sound function
pygame.mixer.music.set_volume(0.2)

#Assigning colors to variables using RBG
white = (255,255,255)
black = (0,0,0)
red= (255,0,0)
green = (0,155,0)

#Variables to assign the game window dimensions
display_width=800
display_height=600

#Creates the game window and sets the title
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Rat Eater")

#Icon for game window
icon=pygame.image.load('logo.png')      #Imports the logo
pygame.display.set_icon(icon)           #Sets the icon

#Imports the sprites images
img = pygame.image.load('snakehead.png')              #Snakehead
ratimg = pygame.image.load('rat.png')                 #Rat

#Initalising FPS
clock = pygame.time.Clock()

FPS = 15                                    #Set FPS
block_size= 20                              #Snake Size
Ratthickness = 30                           #Rat Thickness(Hitbox)
direction = "right"                         #Global variable to set direction of the snake

#Font options
smallfont = pygame.font.SysFont("comicsansms", 25)      #Sets small font
medfont = pygame.font.SysFont("comicsansms", 50)        #Sets medium font 
largefont = pygame.font.SysFont("comicsansms", 80)      #Sets large font

#Pause Screen
def pause():
    paused = True
    while paused:                                           #Loops until user selects their choice                        
        for event in pygame.event.get():            
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:                 #If the 'c' key is pressed unpause the game
                    paused = False
                elif event.key == pygame.K_q:               #Else if the "q" key is pressed quit the game
                    pygame.quit()
                    quit()
                
        gameDisplay.fill(white)                                             #Creates a white background for the pause menu
        message_to_screen("Paused.", black, -100, size = "large")           #Displays Message to the screen
        message_to_screen("Press C to continue or Q to quit", black, 25)    
        message_to_screen("Rat Eater™ By Darren Lally 2016", black, 70)
        
        pygame.display.update()                                             #Updates the screen with the current gamestate                             
        clock.tick(5)                                                       #Sets the FPS to 5 when it is on the menu screen

#Sending score to display function
def score(score):
    text = smallfont.render("Score: " + str(score), True, black)            #Sets up the Score with colour and font size (default font is "small")
    gameDisplay.blit(text, [0,0])                                           #Blits the score counter to the screen (2D array)


#Rat random spawn Function
def randRatGen():
    randRatX = round(random.randrange(0, display_width-Ratthickness))               #Calculates a random horizontal (y) co-ordinate
    randRatY = round(random.randrange(0, display_height-Ratthickness))              #Calculates a random vertical (x) co-ordinate
    return randRatX, randRatY                                                       #Returns the values


#Snake Function
def snake(block_size, snakeList):
    #Rotates the snakes head to face direction travelling
    if direction == "right":
        head = pygame.transform.rotate(img, 270)                                    #Rotates the snakes head so that it faces right

    if direction == "left":
        head = pygame.transform.rotate(img, 90)                                     #Rotates the snakes head so that it faces left

    if direction == "up":                                                           #The snakehead's image is naturally faceing up so it is set to default image
        head = img
        
    if direction == "down":
        head = pygame.transform.rotate(img, 180)                                    #Rotates the snakes head so that it faces down
        
    #Sends it to display
    gameDisplay.blit(head, (snakeList[-1][0], snakeList [-1] [1]))                  #Sends the the snake to display (2D Arrays)
    for XnY in snakeList[:-1]:
        pygame.draw.rect(gameDisplay, green, [XnY[0],XnY[1],block_size,block_size])

#Sets up different text sizes
def text_objects(text,color,size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)

    return textSurface, textSurface.get_rect()

#Start Menu
def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                    
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()


        #Introduction screen messages
        gameDisplay.fill(white)
        message_to_screen("Welcome to Rat Eater", green, -100, size="large")
        message_to_screen("The objective of the game is to eat the rats.", black, -30)
        message_to_screen("The more rats you eat, the longer the snakes body gets.", black, 10)
        message_to_screen("For each rat collected you earn 1 point!", black, 50)
        message_to_screen("If you run into yourself, or the edges, you die!", black, 90)
        message_to_screen("Press C to play or q to quit, also press P to pause the game. ", black, 180)
        
        pygame.display.update()
        clock.tick(15)              #Sets fps of the main menu      
        
    
#Sets the attributes for sending messages to screen.
def message_to_screen(msg,color, y_displace=0, size = "small"):
    textSurf, textRect = text_objects(msg,color, size)
    textRect.center = (display_width/2), (display_height/2)+ y_displace
    gameDisplay.blit(textSurf, textRect)
    

#Main Game Loop Function
def gameLoop():
    global direction        #Direction made global to refrence in this loop 
    direction = "right"
    gameExit = False        #On start the game, exit is set to false(so it can be triggered later)
    gameOver = False

    #Lead blocks of Sprite(head of the snake)
    lead_x = display_width/2
    lead_y = display_height/2

    lead_x_change = 10
    lead_y_change = 0

    snakeList = []
    snakeLength = 1
    
    randRatX,randRatY = randRatGen()

    while not gameExit:
        #Loop Exit screen and takes input from user to see if they want to continue playing or exit the game
        while gameOver == True:
            gameDisplay.fill(white)
            message_to_screen("Game over", red, y_displace=-50, size = "large")                            #Writes message to screen at game over and displaces the text -50 pixels and sets the text to large font
            message_to_screen("Press C to play again or Q to quit", black,y_displace = 50, size ="medium") #Writes message to screen at game over and displaces the text 50 pixels and sets the text to medium font
            
            pygame.display.update()

            for event in pygame.event.get():        
                if event.type==pygame.QUIT:
                    gameExit = True
                    gameOver = False
                    
                if event.type == pygame.KEYDOWN:                    #Binds keys for the user to either start the game by pressing "c" or if "q" is pressed then the game exits
                    
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()

        #Controls of the snake
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                           #Exiting the game via the X
                gameExit = True
            if event.type == pygame.KEYDOWN:                        #Event handling - USER CONTROLS - 
                if event.key == pygame.K_LEFT:
                    direction = "left"                              #When the event its triggered it moves in the direction of what key is pressed.
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:                   #Moves the snake in the direction right.
                    direction = "right"
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP:                      #Moves the snake UP.
                    direction = "up"
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:                    #Moves the snake down.
                    direction = "down"
                    lead_y_change = block_size
                    lead_x_change = 0

                elif event.key == pygame.K_p:                       #If the "p" key is pressed it activates the pause function.
                    pause()
                    
        #Boundaries/Collision detection with walls           
        if lead_x >= display_width or lead_x<0 or lead_y>=display_height or lead_y <0:
            gameOver=True
                
        lead_x += lead_x_change
        lead_y += lead_y_change

        gameDisplay.fill(white)             #Fills the back ground of the game screen
        gameDisplay.blit(ratimg, (randRatX, randRatY)) #Displays sprites on screen

        
        snakeHead = []                              #Snake List(builds the body)
        snakeHead.append(lead_x)                    #Sorts the snakehead into an the snakeHead array by x
        snakeHead.append(lead_y)                    #Sorts the snakehead into an snakeHead array by y
        snakeList.append(snakeHead)                 #Appends the snakeHead list to the front of the snakeList

        if len(snakeList) > snakeLength:
            del snakeList[0]

        for eachSegment in snakeList[:-1]:          #Analise everything up to the last element
            if eachSegment == snakeHead:            #Ends Game if Snake eats/collides with its body
                gameOver = True
        
        snake(block_size, snakeList)
        score(snakeLength-1)                        #Calling function score - Also everytime the snake eats a rat and gains length user gains a point
        
        pygame.display.update()

        #Collision Detection with Rat.
        #Collison if the snake makes contact horizontally
        if lead_x > randRatX and lead_x < randRatX + Ratthickness or lead_x + block_size > randRatX and lead_x + block_size < randRatX + Ratthickness:
            if lead_y > randRatY and lead_y < randRatY + Ratthickness:
                randRatX,randRatY = randRatGen()                            #Re-Spawns the rat in random positions around the screen
                snakeLength += 1                                            #Gives the snake length when he eats a rat
                s= pygame.mixer.Sound("nom.wav")                            #Importing sound effect for when the snake eats a rat
                s.play()                                                    
                
            #Collision if the snake makes contact with the rat vertically
            elif lead_y + block_size > randRatY and lead_y + block_size < randRatY + Ratthickness:
                randRatX,randRatY = randRatGen()                            #Re-spawns the rat in random positions around the screen
                snakeLength += 1                                            #Gives the snake length when he eats a rat
                s= pygame.mixer.Sound("nom.wav")                            #Importing sound effect for when the snake eats a rat
                s.play()
            
        clock.tick(FPS) #Calling/Setting the FPS
    
    pygame.quit()
    quit()
game_intro()    
gameLoop()

