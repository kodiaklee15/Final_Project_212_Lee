# Splash scene - first scene the user sees
import pygwidgets
import pyghelpers
from Constants import *

class SceneSplash(pyghelpers.Scene):
    def __init__(self, window):
        self.window = window
        #self.backgroundImage = window.fill(BLACK)  # Fill the window with black color
        #self.backgroundImage = pygwidgets.Image(self.window,
                                                #(0, 0), 'images/splashBackground.png')
        '''self.dodgerImage = pygwidgets.Image(self.window,
                                                (150, 30), 'images/dodger.png')'''
        
        self.startButton = pygwidgets.CustomButton(self.window, (450, 650),
                                                up='images/startNormal.png',
                                                down='images/startDown.png',
                                                over='images/startOver.png',
                                                disabled='images/startDisabled.png',
                                                enterToActivate=True)

        self.quitButton = pygwidgets.CustomButton(self.window, (30, 650),
                                                up='images/quitNormal.png',
                                                down='images/quitDown.png',
                                                over='images/quitOver.png',
                                                disabled='images/quitDisabled.png')

        self.highScoresButton = pygwidgets.CustomButton(self.window, (190, GAME_HEIGHT + 90),
                                                up='images/gotoHighScoresNormal.png',
                                                down='images/gotoHighScoresDown.png',
                                                over='images/gotoHighScoresOver.png',
                                                disabled='images/gotoHighScoresDisabled.png')
        
        self.playerText = pygwidgets.DisplayText(self.window, (140, 40),'This is you. Drag the icon around by \n'  
                                                                        'moving the mouse. Press the space \n'
                                                                        'bar to shoot lasers \n'
                                                                        'at the aliens. \n',
                                                                        fontSize=36, textColor=WHITE,)
        
        self.alienText = pygwidgets.DisplayText(self.window, (140, 170), 'Dodge the Aliens. Every Alien that \n' 
                                                                        'you dodge earns you a point. Every \n' 
                                                                        'Alien you shoot earns you 10 points.', 
                                                                        fontSize=36, textColor=WHITE)
                                                
        self.goldText = pygwidgets.DisplayText(self.window, (140, 295), 'Catch the Gold. Every Gold you catch \n' 
                                                                        'earns you 50 points. \n', 
                                                                        fontSize=36, textColor=WHITE)

        self.shieldText = pygwidgets.DisplayText(self.window, (140, 400),'Catch the shield to protect yourself \n' 
                                                                         'for 6 seconds. \n', 
                                                                         fontSize=36, textColor=WHITE)
        
        self.info = pygwidgets.DisplayText(self.window, (140, 500),'Press the spacebar to shoot! \n', 
                                                                         fontSize=36, textColor=WHITE)
        
        self.player = pygwidgets.Image(self.window, (40, 50), 'images/spaceship.png')
        self.player.scale(150, False)
        self.alien = pygwidgets.Image(self.window, (40, 190), 'images/alien.png')
        self.alien.scale(150, False)
        self.gold = pygwidgets.Image(self.window, (40, 295), 'images/gold.png')
        self.gold.scale(150, False)
        self.shield = pygwidgets.Image(self.window, (40, 390), 'images/shield_powerup.png')
        self.shield.scale(120, False)


    def getSceneKey(self):
        return SCENE_SPLASH

    def handleInputs(self, events, keyPressedList):
        for event in events:
            if self.startButton.handleEvent(event):
                self.goToScene(SCENE_PLAY)
            elif self.quitButton.handleEvent(event):
                self.quit()
            elif self.highScoresButton.handleEvent(event):
                self.goToScene(SCENE_HIGH_SCORES)

    def draw(self):
        self.window.fill(PURPLE)
        #self.backgroundImage.draw()
        #self.dodgerImage.draw()
        self.startButton.draw()
        self.quitButton.draw()
        self.highScoresButton.draw()
        self.playerText.draw()
        self.alienText.draw()
        self.goldText.draw()
        self.shieldText.draw()
        self.player.draw()
        self.alien.draw() 
        self.gold.draw()
        self.shield.draw()
        self.info.draw()
