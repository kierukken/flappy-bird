import pygame as pg, sys, random

class CreateSurface():
    '''
    CreateSurface class creates objects that can be blitted onto the screen with ease

    The purpose of this class is to create objects that can be blitted onto the screen with ease
    This leads to less lines of coded being needed as it will create a rectangle for each object to place to object easier
    Each function in this class is a different type of object that can be created for example text/image/obstacle

    Parameters
    ----------
    parameter1 : None
        this class does not take any parameters as it is a class that creates different objects that does not have a __init__ method
      Returns
        CreateSurface object
      type
        object
      '''
    def text(self, position, text, colour, size, font = None, rectPos = None, **kwargs):
        '''
    text method creates a text object that can be blitted onto the screen

    The purpose of this method is to create a text object that can be blitted onto the screen
    The parameters allow this object to be changed to different dimensions, colours, position and type of font used

    Parameters
    ----------
    position : tuple/list
        takes in a tuple or list that contains the x and y position of the text
    text : string
        a string passed in the be used as the text of the object
    colour : string
        a string that contains the colour of the text
    size : int
        an integer that contains the size of the text
    font : string, optional
        a string that contains the font of the text, defaults to None
    rectPos : string, optional
        a string that contains the position of the text, defaults to None

      Returns
        updated CreateSurface object
      type
        object
      '''
        if font is not None:
            self.surface = pg.font.SysFont(font, size).render(text, False, colour)
        else:
            self.surface = pg.font.Font(font, size).render(text, False, colour)
        if rectPos is not None:
            self.rect = self.surface.get_rect(**{rectPos: position})
        else:
            self.rect = self.surface.get_rect(topleft = position)
    def image(self, position, image,dimensions = None, rectPos = None, flip = False, **kwargs):
        '''
        image method creates a text object that can be blitted onto the screen

        The purpose of this method is to create a image object that can be blitted onto the screen
        The parameters allow this object to be changed to different dimensions, colours, position and type of font used

        Parameters
        ----------
        position : tuple/list
            takes in a tuple or list that contains the x and y position of the text
        image : string
            a string with the location of the image in the foldor
        dimensions : tuple/list, optional
            a tuple or list that contains the dimensions of the image, defaults to None
        rectPos : string, optional
            a string that contains the position of the text, defaults to None
        flip : bool, optional
            a boolean that contains if the image should be flipped, defaults to False

          Returns
            updated CreateSurface object
          type
            object
      '''
        self.surface = pg.image.load(image).convert_alpha()
        if dimensions is not None:
            self.surface = pg.transform.scale(self.surface, dimensions)
        if flip:
            self.surface = pg.transform.flip(self.surface, True, False)
        if rectPos is not None:
            self.rect = self.surface.get_rect(**{rectPos: position})
        else:
            self.rect = self.surface.get_rect(topleft = position)
    def obstacle(self, xPosition, obstacleGap):
        '''
            obstacle method creates a obstacle object that can be blitted onto the screen

            The purpose of this method is to create a obstacle object that can be blitted onto the screen
            The parameters set the xposiiton and the gap between the obstacles

            Parameters
            ----------
            xPosition : int
                an integer that contains the x position of the obstacle
            obstacleGap : int
                an integer that contains the gap between the top and bottom obstacle

              Returns
                updated CreateSurface object
              type
                object
        '''
        self.surfaceBottom = pg.image.load("Assets/obstacle.png").convert_alpha()
        self.surfaceTop = pg.transform.flip(self.surfaceBottom, False, True)
        self.surfaceBottom = pg.transform.scale(self.surfaceBottom, (200, 450))
        self.surfaceTop = pg.transform.scale(self.surfaceTop, (200, 450))
        self.rectBottom = self.surfaceBottom.get_rect(midbottom = (xPosition, 330-obstacleGap))
        self.rectTop = self.surfaceTop.get_rect(midtop = (xPosition, 330+obstacleGap))
        self.topHitbox = pg.Rect(0, 0, 135, 440)
        self.bottomHitbox = pg.Rect(0, 0, 135, 440)
    def obstacleSpawn(self, obstacleFrequency, obstacleGap):
        '''
            obstacleSpawn method moves the previously created obstacle to a new position to 'respawn' it

            The purpose of this method is to move the obstacle to a new position and make sure that obstacles coming in is uniform

            Parameters
            ----------
            obstacleFrequency : int
                an integer that contains the frequency of the obstacles
            obstacleGap : int
                an integer that contains the gap between the top and bottom obstacle

            Returns
                updated CreateSurface object
            type
                object
        '''
        self.rectBottom.bottom = 330-obstacleGap
        self.rectTop.top = 330+obstacleGap
        randomY = random.randint(-140, 125)
        self.rectBottom.move_ip(1480 + abs(500-obstacleFrequency)*3, randomY)
        self.rectTop.move_ip(1480 + abs(500-obstacleFrequency)*3, randomY)
    def obstacleBlit(self):
        '''
            obstacleBlit method blits the obstacle onto the screen

            Parameters
            ----------
            None

              Returns
                None
              type
                None
              '''
        screen.blit(self.surfaceBottom, self.rectBottom)
        screen.blit(self.surfaceTop, self.rectTop)
    def screenBlit(self):
        '''
            obstacleBlit method blits the obstacle onto the screen

            Parameters
            ----------
            None

            Returns
                None
            type
                None
        '''
        screen.blit(self.surface,self.rect)

def checkCollision(player, surface):
    '''
            Checks for collision between the player and the object

            Parameters
            ----------
            player : object
                object that contains the player
            surface : object
                object that contains the object that the player is colliding with

            Returns
                True or False
            type
                boolean
            '''
    if player.colliderect(surface):
        return True
    return False


# pg setup
pg.init()
pg.font.init()
pg.mixer.init()
screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()

#Start screen variables
gamestate = "startmenu"
highScore = 0
groundSelected = 1
backgroundSelected = 1
playerSelected = 1
arrowAnimationTimer = 0
arrowMoveDistance = 1
ground = [None,1,2,3,4]
background = [None,1,2,3,4]
player = [None,1,2,3,4]

#creating the ground, background and player using class
for i in range(1,5):
    background[i], ground[i], player[i] = CreateSurface(), CreateSurface(), CreateSurface()
    background[i].image((0, 0), f"Assets/background{i}.png", dimensions = (1280, 720))
    ground[i].image((0, 720), f"Assets/ground{i}.png", dimensions = (1280, 125), rectPos = 'bottomleft')
    player[i].image((590, 370), f"Assets/player{i}.png", dimensions = (90, 70))
player[0] = player[playerSelected].rect
playerHitbox = pg.Rect(0, 0, 70, 55)

#Create start screen text and buttons using class
startScreen = [CreateSurface() for i in range(8)]
startScreen[0].image((player[0].centerx, 200), "Assets/title.png", dimensions = (550, 200), rectPos = 'center')
startScreen[2].image((player[0].centerx-100, player[playerSelected].rect.centery), "Assets/arrow.png", dimensions = (75, 50), rectPos = 'center')
startScreen[3].image((player[0].centerx+100, player[playerSelected].rect.centery), "Assets/arrow.png", dimensions = (75, 50), rectPos = 'center', flip = True)
startScreen[4].image((player[0].centerx, 500), "Assets/jumpbutton.png", dimensions = (400, 60), rectPos = 'center')
startScreen[5].text((player[0].centerx, 500), "Click to start!", 'white', 40, font='Bahnschrift', rectPos='center')
startScreen[6].text((1080,50), "Choose Skin", 'black', 30, font='ComicSansMS', rectPos='midtop')
startScreen[7].text((1080,130), "Difficulty", 'black', 30, font='ComicSansMS', rectPos='midtop')

#Score object
score = 0
scoreDisplay = CreateSurface()

#Skin Selection Menu using class
skinSelectionMenu = [CreateSurface() for i in range(3)]
skinSelectionMenu[0].image((640, 300), "Assets/signBackground.png", dimensions = (800, 420), rectPos = 'center')
skinSelectionMenu[1].text((640, 100), "Choose Skin", 'black', 50, font='Comic Sans MS', rectPos='center')
skinSelectionMenu[2].image((990,80), "Assets/closebutton.png", dimensions = (50, 50), rectPos = 'center')

#Skins using class
skins = [CreateSurface() for i in range(0,12)]
for i in range(1, 5):
    skins[i-1].image((220 + i*150, 150), f"Assets/player{i}.png", dimensions = (100, 70), rectPos = 'topleft')
    skins[i+3].image((220 + i*150, 250), f"Assets/background{i}.png", dimensions = (100, 70), rectPos = 'topleft')
    skins[i+7].image((220 + i*150, 350), f"Assets/ground{i}.png", dimensions = (100, 70), rectPos = 'topleft')

#Death screen using class
deathScreen, restartButton, mainMenuButton = CreateSurface(), CreateSurface(), CreateSurface()
restartButton.text((640,270), "Restart", 'black', 40, font='Comic Sans MS', rectPos='center')
mainMenuButton.text((640,370), "Main Menu", 'black', 40, font='Comic Sans MS', rectPos='center')

#Pause button and mute button using class
pauseButton, muteButton, resumeButton, settingsButton, returnButton = CreateSurface(), CreateSurface(), CreateSurface(), CreateSurface(), CreateSurface()
pauseButton.image((10, 10), "Assets/pausebutton.png", dimensions = (85, 85))
muteButton.image((100, 10), "Assets/mutebutton.png", dimensions = (85, 85))
resumeButton.image((10, 10), "Assets/resumebutton.png", dimensions = (85, 85))
settingsButton.image((10, 100), "Assets/settingsbutton.png", dimensions = (85, 85))
returnButton.image((10, 190), "Assets/backbutton.png", dimensions = (85, 85))

#settings menu using class
menuBackGround, close, rebindJump, rebindJumpText = CreateSurface(), CreateSurface(), CreateSurface(), CreateSurface()
menuBackGround.image((640, 300), "Assets/signBackground.png", dimensions = (800, 420), rectPos = 'center')
close.image((menuBackGround.rect.right-130, menuBackGround.rect.top+70), "Assets/closebutton.png", dimensions = (50, 50), rectPos = 'center')
rebindJump.text((menuBackGround.rect.right-200, menuBackGround.rect.top+200), "Rebind Jump", '#C1F376', 30, font='Comic Sans MS', rectPos='center')
rebindJumpText.text((640, 300), "Press new rebinded jump key", '#C1F376', 50, font='Comic Sans MS', rectPos='center')

#Sound Sliders and text using class
soundLevel, musicLevel, sfxLevel = 100, 100, 100
soundText, musicText, sfxText = CreateSurface(), CreateSurface(), CreateSurface()
#Sound Text
soundText.text((350, 150), f"Sound {soundLevel}%", '#C1F376', 30, font='Comic Sans MS')
musicText.text((350, 250), f"Music {musicLevel}%", '#C1F376', 30, font='Comic Sans MS')
sfxText.text((350, 350), f"Sfx {sfxLevel}%", '#C1F376', 30, font='Comic Sans MS')
sliderText = [soundText, musicText, sfxText]
#Sound Sliders
soundSlider = pg.Rect(350, 200, 350, 27)
musicSlider = pg.Rect(350, 300, 350, 27)
sfxSlider = pg.Rect(350, 400, 350, 27)
sliders = [soundSlider, musicSlider, sfxSlider]
#Mini Sliders
soundMiniSlider, soundMiniSlider.centerx, soundMiniSlider.centery = pg.Rect(0, 0, 10, 40), 525, 213
musicMiniSlider, musicMiniSlider.centerx, musicMiniSlider.centery = pg.Rect(0, 0, 10, 40), 525, 313
sfxMiniSlider, sfxMiniSlider.centerx, sfxMiniSlider.centery = pg.Rect(0, 0, 10, 40), 525, 413
miniSliders = [soundMiniSlider, musicMiniSlider, sfxMiniSlider]

#Difficulty Menu using class
difficultyMenu = [CreateSurface() for i in range(3)]
difficultyMenu[0].image((640, 300), "Assets/signBackground.png", dimensions = (800, 420), rectPos = 'center')
difficultyMenu[1].text((640, 100), "Choose Difficulty", 'black', 50, font='Comic Sans MS', rectPos='center')
difficultyMenu[2].image((990,80), "Assets/closebutton.png", dimensions = (50, 50), rectPos = 'center')

#Difficulty Sliders
obstacleFrequency, obstacleGap = 500, 105
obstacleFrequencyText, obstacleGapText = CreateSurface(), CreateSurface()
#Difficulty Text
obstacleFrequencyText.text((350, 150), f"Obstacle Frequency {obstacleFrequency}", '#C1F376', 30, font='Comic Sans MS')
obstacleGapText.text((350, 250), f"Obstacle Gap {obstacleGap}", '#C1F376', 30, font='Comic Sans MS')
difficultyText = [obstacleFrequencyText, obstacleGapText]
#Difficulty Sliders
difficultySlider = pg.Rect(350, 200, 350, 27)
gapSlider = pg.Rect(350, 300, 350, 27)
difficultySliders = [difficultySlider, gapSlider]
#Mini Sliders
difficultyMiniSlider, difficultyMiniSlider.centerx, difficultyMiniSlider.centery = pg.Rect(0, 0, 10, 40), 525, 213
gapMiniSlider, gapMiniSlider.centerx, gapMiniSlider.centery = pg.Rect(0, 0, 10, 40), 525, 313
difficultyMiniSliders = [difficultyMiniSlider, gapMiniSlider]


#Create Obstacles
obstacles = None
def CreateObstacles(obstacleFrequency):
    '''
        CreateObstacle functions generates 3 obstacles that are placed on the screen evenly

        Parameters
        ----------
        obstacleFrequency : int
            an integer that contains the frequency of the obstacles

        Returns
            Nothing
        type
            Nothing
                '''
    global obstacles
    if obstacles is not None:
        del obstacles
    obstacles = [CreateSurface() for i in range(3)]
    for i in range(3):
        obstacles[i].obstacle(1280 + i*obstacleFrequency, obstacleGap)
#Create obstacles
CreateObstacles(obstacleFrequency)


#Music and sfx loading it and setting volumne
pg.mixer.music.load("Assets/backgroundmusic.mp3")
pg.mixer.music.play(-1)
pg.mixer.music.set_volume(0.1)
flapSound = pg.mixer.Sound("Assets/flapsound.mp3")
flapSound.set_volume(1)
deathSound = pg.mixer.Sound("Assets/deathsound.mp3")
deathSound.set_volume(1)
soundEffects = [flapSound, deathSound]
soundSliderValue = 1
musicSliderValue = 1
sfxSliderValue = 1


#game variables
previousGamestate = None
pauseAndResumeBoolean = False
jumpKeyBind = pg.K_SPACE
selectingKeyBind = False
mute = False

#game loop
while True:
    #event loop checking for all events
    for event in pg.event.get():
        #if the event is a quit event then quit the game
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        #if the event is a keydown event then check for the key pressed
        if event.type == pg.KEYDOWN:
            #if the key pressed is escape then check the gamestate and change it accordingly
            if event.key == pg.K_ESCAPE and gamestate != 'settings' and gamestate != 'skins' and gamestate != 'difficulty':
                if gamestate == 'pause':
                    gamestate = previousGamestate
                else:
                    previousGamestate = gamestate
                    gamestate = 'pause'

            #if the key pressed is the jump key and the gamestate is playgame then make the player jump
            if event.key == jumpKeyBind and gamestate == 'playgame'and player[0].top > -20:
                playerVelocity = -15
                flapSound.play()

            #if the key pressed is not escape and the gamestate is settings then change the jump key to the key pressed
            if selectingKeyBind and event.key != pg.K_ESCAPE and gamestate == 'settings':
                jumpKeyBind = event.key
                selectingKeyBind = False


        #if the event is a mousebuttondown event then check for the position of the mouse and change the gamestate accordingly
        if event.type == pg.MOUSEBUTTONDOWN:
            #Check for start menu events
            if gamestate == 'startmenu':
                #Check for the position of the mouse and change the gamestate accordingly
                if startScreen[6].rect.collidepoint(event.pos):
                    gamestate = 'skins'

                elif startScreen[7].rect.collidepoint(event.pos):
                    gamestate = 'difficulty'

                #if the mouse is not on the buttons then change the gamestate to playgame and start game
                if not (muteButton.rect.collidepoint(event.pos) or pauseButton.rect.collidepoint(event.pos) or startScreen[6].rect.collidepoint(event.pos) or startScreen[7].rect.collidepoint(event.pos)):
                    score = 0
                    gamestate = 'playgame'
                    playerVelocity = -15

            #Check for jumps while game is playing to make player jump but only if the player is not at the top of the screen
            if gamestate == 'playgame' and player[0].top > -20:
                playerVelocity = -15
                flapSound.play()

            #Check for deathscreen events
            if gamestate == 'deathscreen':
                #Check if restart button is pressed and restart the game if so
                if restartButton.rect.collidepoint(event.pos):
                    score = 0
                    gamestate = 'playgame'
                    player[0] = player[playerSelected].rect
                    playerVelocity = -25
                    CreateObstacles(obstacleFrequency)

                #Check if main menu button is pressed and change the gamestate to startmenu ressetting the player and obstacles
                if mainMenuButton.rect.collidepoint(event.pos):
                    gamestate = 'startmenu'
                    player[0] = player[playerSelected].rect
                    playerVelocity = 0
                    CreateObstacles(obstacleFrequency)

            #Check if the pause button is pressed and change the gamestate to pause
            if pauseButton.rect.collidepoint(event.pos) and gamestate != 'pause' and gamestate != 'settings' and gamestate != 'skins' and gamestate != 'difficulty':
                previousGamestate = gamestate
                pauseAndResumeBoolean = True
                gamestate = 'pause'

            #Check for pause gamestate events
            if gamestate == 'pause':
                #Check if resume button is pressed and change the gamestate to the previous gamestate
                if resumeButton.rect.collidepoint(event.pos) and not pauseAndResumeBoolean:
                    gamestate = previousGamestate

                #Check if settings button is pressed and change the gamestate to settings
                if settingsButton.rect.collidepoint(event.pos):
                    previousGamestate = gamestate
                    gamestate = 'settings'

                #Check if return button is pressed and change the gamestate to startmenu
                if returnButton.rect.collidepoint(event.pos):
                    gamestate = 'startmenu'
                    player[0] = player[playerSelected].rect
                    playerVelocity = 0
                    CreateObstacles(obstacleFrequency)

            #Check for settings gamestate events
            if gamestate == 'settings':
                #Check if close button is pressed and change the gamestate to startmenu
                if close.rect.collidepoint(event.pos) and not selectingKeyBind:
                    previousGamestate = 'startmenu'
                    player[0] = player[playerSelected].rect
                    CreateObstacles(obstacleFrequency)
                    gamestate = previousGamestate

                #Check of the user pressed rebind jump button and change the selectingKeyBind to True to allow the user to rebind the jump key on the next
                #iteration of the game loop
                if rebindJump.rect.collidepoint(event.pos):
                    selectingKeyBind = True

                #Check if the user pressed the sliders and change the value of the sliders accordingly
                if soundSlider.collidepoint(event.pos):
                    soundMiniSlider.centerx = event.pos[0]
                    soundSliderValue = (soundMiniSlider.centerx-350)/175
                    soundText.text((350, 150), f"Sound {int(100*soundSliderValue)}%", '#C1F376', 30, font='Comic Sans MS')

                if musicSlider.collidepoint(event.pos):
                    musicMiniSlider.centerx = event.pos[0]
                    musicSliderValue = (musicMiniSlider.centerx-350)/175
                    musicText.text((350, 250), f"Music {int(100*musicSliderValue)}%", '#C1F376', 30, font='Comic Sans MS')

                if sfxSlider.collidepoint(event.pos):
                    sfxMiniSlider.centerx = event.pos[0]
                    sfxSliderValue = (sfxMiniSlider.centerx-350)/175
                    sfxText.text((350, 350), f"Sfx {int(100*sfxSliderValue)}%", '#C1F376', 30, font='Comic Sans MS')

                #Check if the mute button has been pressed if not change the volume of the music and sound effects according to values set by slider
                if not mute:
                    pg.mixer.music.set_volume(0.1 * musicSliderValue * soundSliderValue)
                    for sound in soundEffects:
                        sound.set_volume(1 * soundSliderValue * sfxSliderValue)

            #Check for difficulty gamestate events
            if gamestate == 'difficulty':
                #Check if close button is pressed and change the gamestate to startmenu
                if difficultyMenu[2].rect.collidepoint(event.pos):
                    gamestate = 'startmenu'

                #Check if the sliders are pressed and change the value of the sliders accordingly
                if difficultySlider.collidepoint(event.pos):
                    difficultyMiniSlider.centerx = event.pos[0]
                    obstacleFrequency = int((difficultyMiniSlider.centerx-200)*1.54)
                    obstacleFrequencyText.text((350, 150), f"Obstacle Frequency: {obstacleFrequency}", '#C1F376', 30, font='Comic Sans MS')

                if gapSlider.collidepoint(event.pos):
                    gapMiniSlider.centerx = event.pos[0]
                    obstacleGap = int((gapMiniSlider.centerx-100)//4)
                    obstacleGapText.text((350, 250), f"Obstacle Gap: {obstacleGap}", '#C1F376', 30, font='Comic Sans MS')

                #Regenerate obstacles with new values
                CreateObstacles(obstacleFrequency)

            #Check if mute button is pressed and toggle the mute variable turning the music and sound effects on and off
            if muteButton.rect.collidepoint(event.pos):
                #turning the music and sound effects on
                if pg.mixer.music.get_volume() == 0:
                    pg.mixer.music.set_volume(0.1*musicSliderValue*soundSliderValue)
                    for sound in soundEffects:
                        sound.set_volume(1*soundSliderValue*sfxSliderValue)
                    mute = False
                #turning the music and sound effects off
                else:
                    pg.mixer.music.set_volume(0)
                    for sound in soundEffects:
                        sound.set_volume(0)
                    mute = True

            #Check for skin selection menu events
            if gamestate == 'skins':
                #Check if close button is pressed and change the gamestate to startmenu
                if skinSelectionMenu[2].rect.collidepoint(event.pos):
                    gamestate = 'startmenu'
                #Check if the skins are pressed and change the player, background and ground accordingly
                for i, skin in enumerate(skins):
                    if skin.rect.collidepoint(event.pos):
                        #Changing the player
                        if i < 4:
                            playerSelected = i+1

                        #Changing the background
                        elif i < 8:
                            backgroundSelected = i-3

                        #Changing the ground
                        else:
                            groundSelected = i-7

                        #Moving the new selected player to the position of the old player
                        player[0] = player[playerSelected].rect

    #setting pause boolean to false, variable exists to prevent the game from pausing and resuming at the same time
    pauseAndResumeBoolean = False
    #blitting the background, ground and player first as they are used in every scene
    background[backgroundSelected].screenBlit()
    ground[groundSelected].screenBlit()
    screen.blit(player[playerSelected].surface, player[0])

    #Checking for startmenu to display the startmenu
    if gamestate == 'startmenu':
        #Rendering high score text to constantly update it to what ever the current one is
        startScreen[1].text((player[0].centerx, 265), f"Highscore: {highScore}", 'black', 40, font='Comic Sans MS', rectPos='center')

        #Blitting all the objects in the start menu
        for object in startScreen:
            object.screenBlit()

        #Drawing a rectangle around the 2 buttons in the start menu
        pg.draw.rect(screen, 'black', (startScreen[6].rect.left-10,startScreen[6].rect.top-10, startScreen[6].rect.width+20, startScreen[6].rect.height+20), 4)
        pg.draw.rect(screen, 'black', (startScreen[7].rect.left-10,startScreen[7].rect.top-10, startScreen[7].rect.width+20, startScreen[7].rect.height+20), 4)

        #Checking if the arrow animation timer is at 30 or 60 and changing the direction of the arrow creating a pointing animation
        if arrowAnimationTimer == 30:
            arrowMoveDistance *= -1
        if arrowAnimationTimer == 60:
            arrowMoveDistance *= -1
            arrowAnimationTimer = 0
        arrowAnimationTimer += 1
        #Moving the arrows to create the animation
        startScreen[2].rect.move_ip(-arrowMoveDistance, 0)
        startScreen[3].rect.move_ip(arrowMoveDistance, 0)

    #Checking for playgame to display the game
    if gamestate == 'playgame':
        #Moving the player
        player[0] = player[0].move(0, playerVelocity)
        playerVelocity += 1

        #Code to move the player to the left at the start of the game
        if player[0].left > 350:
            player[0] = player[0].move(-7, 0)

        #Checking for collision with the ground and changing the gamestate to deathscreen
        if checkCollision(player[0], ground[groundSelected].rect):
            player[0].bottom = ground[groundSelected].rect.top
            gamestate = 'deathscreen'
            deathSound.play()

        #Setting the previously defined player hitbox to the appropriate spot to get the most accurate collision detection
        playerHitbox.centerx, playerHitbox.centery = player[0].centerx+5, player[0].centery+5

    #Checking for the screens that need the obstacles to be displayed
    if gamestate == 'playgame' or gamestate == 'deathscreen' or gamestate == 'pause':
        #Looping through all the obstacles to display, update position, update score, check for collision and check if the obstacle is off the screen
        for i, obstacle in enumerate(obstacles):
            obstacle.obstacleBlit()
            #Moving the obstacles
            if gamestate == 'playgame':
                obstacle.rectBottom.move_ip(-7, 0)
                obstacle.rectTop = obstacle.rectTop.move(-7, 0)

            #Checking if the obstacle is off the screen and if so respawning it
            if obstacles[i].rectBottom.right < 0:
                obstacles[i].obstacleSpawn(obstacleFrequency, obstacleGap)

            #Checking for collision with the player and changing the gamestate to deathscreen
            if (checkCollision(playerHitbox, obstacle.bottomHitbox) or checkCollision(playerHitbox, obstacle.topHitbox)) and gamestate == 'playgame':
                gamestate = 'deathscreen'
                deathSound.play()

            # Code to show the hitboxes of the player and obstacles for marking purposes
            try:
                if checkHitBox:
                    pg.draw.rect(screen, 'blue', obstacles[i].topHitbox, 5)
                    pg.draw.rect(screen, 'blue', obstacles[i].bottomHitbox, 5)
                    pg.draw.rect(screen, 'blue', playerHitbox, 5)
            except:
                pass

            #updating the hitboxes of the obstacles
            obstacles[i].bottomHitbox.centerx, obstacles[i].bottomHitbox.centery = obstacles[i].rectBottom.centerx, obstacles[i].rectBottom.centery
            obstacles[i].topHitbox.centerx, obstacles[i].topHitbox.centery = obstacles[i].rectTop.centerx, obstacles[i].rectTop.centery

            #Checking if the player has passed the obstacle and updating the score
            if player[0].centerx-4 < obstacles[i].topHitbox.midbottom[0] < player[0].centerx+4 and gamestate == 'playgame':
                score += 1

            #Displaying the score
            scoreDisplay.text((640, 50), f"Score: {score}", 'black', 40, font='Comic Sans MS', rectPos='center')
            scoreDisplay.screenBlit()

    #Bliting pause and mute button
    pauseButton.screenBlit()
    muteButton.screenBlit()

    #Checking if the game is paused
    if gamestate == 'pause':
        #Blitting the resume, settings and return button
        resumeButton.screenBlit()
        settingsButton.screenBlit()
        returnButton.screenBlit()

    #Checking if the game is in settings
    if gamestate == 'settings':
        #Blitting the background, close button, and rebind jump
        menuBackGround.screenBlit()
        close.screenBlit()
        rebindJump.screenBlit()
        #drawing a rectangle around the rebind jump button
        pg.draw.rect(screen, '#C1F376', (rebindJump.rect.left-10, rebindJump.rect.top-10, rebindJump.rect.width+20, rebindJump.rect.height+20), 4)

        #Blitting the sliders and mini sliders
        for slider in sliders:
            pg.draw.rect(screen, '#C1F376', slider)
        for text in sliderText:
            text.screenBlit()
        for miniSlider in miniSliders:
            pg.draw.rect(screen, 'black', miniSlider)

    #Checking if the game is in skins gamestate
    if gamestate == 'skins':
        #Blitting the background, close button and the skins
        for surface in skinSelectionMenu:
            surface.screenBlit()
        for skin in skins:
            skin.screenBlit()

    #Checking if the game is in difficulty gamestate
    if gamestate == 'difficulty':
        #Blitting the background, close button and the sliders
        for surface in difficultyMenu:
            surface.screenBlit()
        for slider in difficultySliders:
            pg.draw.rect(screen, '#C1F376', slider)
        for miniSlider in difficultyMiniSliders:
            pg.draw.rect(screen, 'Black', miniSlider)
        for text in difficultyText:
            text.screenBlit()

    #Checking if the game is in the deathscreen gamestate
    if gamestate == 'deathscreen':
        #updating high score
        if score > highScore:
            highScore = score
        #Blitting the deathscreen, restart button and main menu button
        restartButton.screenBlit()
        mainMenuButton.screenBlit()
        pg.draw.rect(screen, 'black', (restartButton.rect.left - 10, restartButton.rect.top - 10, restartButton.rect.width + 20, restartButton.rect.height + 20), 4)
        pg.draw.rect(screen, 'black', (mainMenuButton.rect.left - 10, mainMenuButton.rect.top - 10, mainMenuButton.rect.width + 20, mainMenuButton.rect.height + 20), 4)

    #Checking if the game is in the settings gamestate
    if selectingKeyBind:
        #Blitting the text to rebind the jump key
        pg.draw.rect(screen, '#fff5be', (rebindJumpText.rect.left - 10, rebindJumpText.rect.top - 10, rebindJumpText.rect.width + 20, rebindJumpText.rect.height + 20))
        rebindJumpText.screenBlit()

    pg.display.flip()
    clock.tick(60)

pg.quit()
