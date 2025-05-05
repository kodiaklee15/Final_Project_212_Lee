# Play scene - the main game play scene
from pygame.locals import *
import pygwidgets
import pyghelpers
from Player import *
from Baddies import *
from Goodies import *
from Laser import *

# Function to show a custom Yes/No dialog box
def showCustomYesNoDialog(theWindow, theText):
    oDialogBackground = pygwidgets.Image(theWindow, (40, 250), 'images/dialog.png')
    oPromptDisplayText = pygwidgets.DisplayText(theWindow, (0, 290), theText, width=WINDOW_WIDTH, justified='center', fontSize=36)

    oYesButton = pygwidgets.CustomButton(theWindow, (320, 370), 'images/gotoHighScoresNormal.png', over='images/gotoHighScoresOver.png', down='images/gotoHighScoresDown.png', disabled='images/gotoHighScoresDisabled.png')
    oNoButton = pygwidgets.CustomButton(theWindow, (62, 370), 'images/noThanksNormal.png', over='images/noThanksOver.png', down='images/noThanksDown.png', disabled='images/noThanksDisabled.png')

    # Display the Yes/No dialog and return the choice
    choiceAsBoolean = pyghelpers.customYesNoDialog(theWindow, oDialogBackground, oPromptDisplayText, oYesButton, oNoButton)
    return choiceAsBoolean

# Constants for the game states and invincibility duration
BOTTOM_RECT = (0, GAME_HEIGHT + 1, WINDOW_WIDTH, WINDOW_HEIGHT - GAME_HEIGHT)
STATE_WAITING = 'waiting'
STATE_PLAYING = 'playing'
STATE_GAME_OVER = 'game over'
INVINCIBILITY_DURATION = 80  # frames (e.g., 2 seconds if 60 FPS)

# ScenePlay class handles the main game logic
class ScenePlay(pyghelpers.Scene):

    def __init__(self, window):
        self.window = window

        # Background and button images for the controls and interface
        self.controlsBackground = pygwidgets.Image(self.window, (0, GAME_HEIGHT), 'images/controlsBackground.jpg')
        self.quitButton = pygwidgets.CustomButton(self.window, (30, GAME_HEIGHT + 90), up='images/quitNormal.png', down='images/quitDown.png', over='images/quitOver.png', disabled='images/quitDisabled.png')
        self.highScoresButton = pygwidgets.CustomButton(self.window, (190, GAME_HEIGHT + 90), up='images/gotoHighScoresNormal.png', down='images/gotoHighScoresDown.png', over='images/gotoHighScoresOver.png', disabled='images/gotoHighScoresDisabled.png')
        self.newGameButton = pygwidgets.CustomButton(self.window, (450, GAME_HEIGHT + 90), up='images/startNewNormal.png', down='images/startNewDown.png', over='images/startNewOver.png', disabled='images/startNewDisabled.png', enterToActivate=True)

        # Sound and display elements
        self.soundCheckBox = pygwidgets.TextCheckBox(self.window, (430, GAME_HEIGHT + 17), 'Background music', True, textColor=WHITE)
        self.gameOverImage = pygwidgets.Image(self.window, (140, 180), 'images/gameOver.png')
        self.titleText = pygwidgets.DisplayText(self.window, (15, GAME_HEIGHT + 17), 'Score:                                 High Score:', fontSize=24, textColor=WHITE)
        self.scoreText = pygwidgets.DisplayText(self.window, (80, GAME_HEIGHT + 13), '0', fontSize=36, textColor=WHITE, justified='right')
        self.highScoreText = pygwidgets.DisplayText(self.window, (300, GAME_HEIGHT + 13), '', fontSize=36, textColor=WHITE, justified='right')
        self.shieldImage = pygwidgets.Image(self.window, (0, 0), 'images/shield_powerup.png')
        self.goldText = pygwidgets.DisplayText(self.window, (15, GAME_HEIGHT + 47), 'Gold Collected: 0', fontSize=30, textColor=GOLD)

        # Sounds for the game
        pygame.mixer.music.load('sounds/background.mid')
        self.dingSound = pygame.mixer.Sound('sounds/ding.wav')
        self.gameOverSound = pygame.mixer.Sound('sounds/gameover.wav')

        # Instantiate game objects
        self.oPlayer = Player(self.window)
        self.oBaddieMgr = BaddieMgr(self.window)
        self.oGoodieMgr = GoodieMgr(self.window)

        # Initialize game state variables
        self.highestHighScore = 0
        self.lowestHighScore = 0
        self.backgroundMusic = True
        self.score = 0
        self.playingState = STATE_WAITING
        self.lasers = []

        self.lives = 3
        self.is_invincible = False
        self.invincibility_timer = 0

        self.goodies_collected = 0
        self.special_laser_active = False
        self.special_laser_timer = 0
        self.shield_active = False
        self.shield_timer = 0

        self.livesText = pygwidgets.DisplayText(self.window, (450, GAME_HEIGHT + 47), f'Lives: {self.lives}', fontSize=30, textColor=WHITE)

    def getSceneKey(self):
        return SCENE_PLAY

    def enter(self, data):
        self.getHiAndLowScores()

    def getHiAndLowScores(self):
        # Get high and low scores from the high scores scene
        infoDict = self.request(SCENE_HIGH_SCORES, HIGH_SCORES_DATA)
        self.highestHighScore = infoDict['highest']
        self.highScoreText.setValue(self.highestHighScore)
        self.lowestHighScore = infoDict['lowest']

    def reset(self):
        # Reset the game state for a new game
        self.score = 0
        self.scoreText.setValue(self.score)
        self.getHiAndLowScores()

        # Reset all managers and game state variables
        self.oBaddieMgr.reset()
        self.oGoodieMgr.reset()
        self.shield_active = False
        self.shield_timer = 0
        self.lasers = []  # Reset lasers list
        self.goodies_collected = 0
        self.goldText.setValue(f'Gold Collected: {self.goodies_collected}')
        self.special_laser_active = False

        if self.backgroundMusic:
            pygame.mixer.music.play(-1, 0.0)  # Loop background music
        self.newGameButton.disable()
        self.highScoresButton.disable()
        self.soundCheckBox.disable()
        self.quitButton.disable()
        pygame.mouse.set_visible(False)

        self.lives = 3
        self.is_invincible = False
        self.invincibility_timer = 0
        self.livesText.setValue(f'Lives: {self.lives}')

    def handleInputs(self, eventsList, keyPressedList):
        # Handle key and mouse inputs for the game
        if self.playingState == STATE_PLAYING:
            for event in eventsList:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if not self.is_invincible:
                        playerRect = self.oPlayer.image.getRect()
                        laserX = playerRect.centerx
                        laserY = playerRect.top
                        if self.special_laser_active:
                            self.lasers.append(SpecialLaser(laserX, laserY, 90))
                            self.lasers.append(SpecialLaser(laserX, laserY, 110))
                            self.lasers.append(SpecialLaser(laserX, laserY, 70))
                        else:
                            self.lasers.append(Laser(laserX, laserY))
            return  # Ignore button events while playing

        # Handle events for UI buttons
        for event in eventsList:
            if self.newGameButton.handleEvent(event):
                self.reset()
                self.playingState = STATE_PLAYING

            if self.highScoresButton.handleEvent(event):
                self.goToScene(SCENE_HIGH_SCORES)

            if self.soundCheckBox.handleEvent(event):
                self.backgroundMusic = self.soundCheckBox.getValue()

            if self.quitButton.handleEvent(event):
                self.quit()

    def update(self):
        # Update the game state during play
        if self.playingState != STATE_PLAYING:
            return  # Only update when playing
        self.livesText.setValue(f'Lives: {self.lives}')

        # Move the Player to the mouse position
        mouseX, mouseY = pygame.mouse.get_pos()
        playerRect = self.oPlayer.update(mouseX, mouseY)

        # Handle invincibility state
        if self.is_invincible:
            self.invincibility_timer -= 1
            if self.invincibility_timer <= 0:
                self.is_invincible = False

        # Update the GoodieMgr (collect goodies)
        nGoodiesHit, shieldPickedUp = self.oGoodieMgr.update(playerRect)

        if nGoodiesHit > 0:
            self.dingSound.play()
            self.score += (nGoodiesHit * POINTS_FOR_GOODIE)
            self.goodies_collected += nGoodiesHit
            self.goldText.setValue(f'Gold Collected: {self.goodies_collected}')

            # Activate special laser after collecting 10 gold
            if self.goodies_collected >= 10:
                self.special_laser_active = True
                self.special_laser_timer = 400
                self.goodies_collected = 0

        # Activate shield if picked up
        if shieldPickedUp:
            self.shield_active = True
            self.shield_timer = 240  # 6 seconds at 40 FPS
            print("Shield activated!")

        if self.shield_active:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.shield_active = False

        # Update the BaddieMgr (enemy behavior)
        nBaddiesEvaded = self.oBaddieMgr.update(self.score)
        self.score += (nBaddiesEvaded * POINTS_FOR_BADDIE_EVADED)
        self.scoreText.setValue(self.score)

        # Handle laser updates
        for laser in self.lasers[:]:
            laser.update()
            for baddie in self.oBaddieMgr.baddiesList[:]:
                laser_rect = pygame.Rect(laser.x - 2, laser.y - 2, 4, 4)
                if baddie.image.getRect().colliderect(laser_rect):
                    self.oBaddieMgr.baddiesList.remove(baddie)
                    self.lasers.remove(laser)
                    self.score += 10
                    break

            if laser in self.lasers and laser.is_dead():
                self.lasers.remove(laser)

        # Handle enemy laser collision
        for laser in self.oBaddieMgr.enemy_lasers[:]:
            if playerRect.collidepoint(laser.x, laser.y) and not self.is_invincible and not self.shield_active:
                self.lives -= 1
                self.livesText.setValue(f'Lives: {self.lives}')
                self.is_invincible = True
                self.invincibility_timer = INVINCIBILITY_DURATION
                self.oBaddieMgr.enemy_lasers.remove(laser)

                if self.lives <= 0:
                    self.handleGameOver()

        # Handle special laser deactivation
        if self.special_laser_active:
            self.special_laser_timer -= 1
            if self.special_laser_timer <= 0:
                self.special_laser_active = False

        # Check if the Player has hit any Baddie
        if not self.is_invincible and not self.shield_active and self.oBaddieMgr.hasPlayerHitBaddie(playerRect):
            self.lives -= 1
            self.livesText.setValue(f'Lives: {self.lives}')
            self.is_invincible = True
            self.invincibility_timer = INVINCIBILITY_DURATION

            if self.lives <= 0:
                self.handleGameOver()

    def handleGameOver(self):
        # Handle the game over state
        pygame.mouse.set_visible(True)
        pygame.mixer.music.stop()
        self.gameOverSound.play()
        self.playingState = STATE_GAME_OVER
        self.draw()

        if self.score > self.lowestHighScore:
            scoreString = 'Your score: ' + str(self.score) + '\n'
            if self.score > self.highestHighScore:
                dialogText = (scoreString + 'is a new high score, CONGRATULATIONS!')
            else:
                dialogText = (scoreString + 'gets you on the high scores list.')

            result = showCustomYesNoDialog(self.window, dialogText)
            if result: 
                self.goToScene(SCENE_HIGH_SCORES, self.score)

        # Enable UI buttons after game over
        self.newGameButton.enable()
        self.highScoresButton.enable()
        self.soundCheckBox.enable()
        self.quitButton.enable()

    def draw(self):
        # Draw the game elements on the screen
        self.window.fill(BLACK)

        # Draw the managers (baddies, goodies, lasers)
        self.oBaddieMgr.draw()
        self.oGoodieMgr.draw()
        for laser in self.lasers:
            laser.draw(self.window)

        # Draw the Player
        if not self.is_invincible:
            self.oPlayer.draw()
        else:
            # Blink effect: Only draw on certain frames
            if (self.invincibility_timer // 5) % 2 == 0:
                self.oPlayer.draw()

        # Draw the shield if active
        if self.shield_active:
            playerRect = self.oPlayer.image.getRect()
            center_x = playerRect.centerx
            center_y = playerRect.centery
            shield_width, shield_height = self.shieldImage.getSize()
            shield_x = center_x - shield_width // 2
            shield_y = center_y - shield_height // 2
            self.shieldImage.setLoc((shield_x, shield_y))
            if self.shield_timer > 80:
                self.shieldImage.draw()  # Draw normally if more than 2 seconds left
            else:
                # Blink when 2 seconds left
                if (self.shield_timer // 5) % 2 == 0:
                    self.shieldImage.draw()

        # Display level-up message if spawn rate changed
        if self.oBaddieMgr.spawn_rate_changed:
            level_up_text = pygwidgets.DisplayText(self.window, (200, 50), "Level Up", fontSize=48, textColor=(255, 0, 0))
            level_up_text.draw()

        # Draw the UI elements (score, high score, buttons)
        self.controlsBackground.draw()
        self.titleText.draw()
        self.scoreText.draw()
        self.highScoreText.draw()
        self.soundCheckBox.draw()
        self.quitButton.draw()
        self.highScoresButton.draw()
        self.newGameButton.draw()
        self.livesText.draw()
        self.goldText.draw()

        if self.playingState == STATE_GAME_OVER:
            self.gameOverImage.draw()

    def leave(self):
        # Stop music when leaving the scene
        pygame.mixer.music.stop()
