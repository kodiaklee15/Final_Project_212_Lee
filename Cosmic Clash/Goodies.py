# Goodie and GoodieMgr classes
import pygame
import pygwidgets
import random
from Constants import *

# Goodie class represents an item that the player can collect (e.g., gold or shield)
class Goodie():
    MIN_SIZE = 10
    MAX_SIZE = 40
    MIN_SPEED = 1
    MAX_SPEED = 8
    GOODIE_IMAGE = pygame.image.load('images/gold.png')  # Image for normal goodie
    SHIELD_IMAGE = pygame.image.load('images/shield_powerup.png')  # Image for shield power-up
    RIGHT = 'right'
    LEFT = 'left'

    def __init__(self, window, goodie_type='normal'):
        self.window = window
        self.goodie_type = goodie_type

        # Random size for the goodie
        size = random.randrange(Goodie.MIN_SIZE, Goodie.MAX_SIZE + 1)
        # Random y-position for the goodie
        self.y = random.randrange(0, GAME_HEIGHT - size)

        # Random horizontal direction for the goodie (left or right)
        self.direction = random.choice([Goodie.LEFT, Goodie.RIGHT])
        if self.direction == Goodie.LEFT:
            self.x = WINDOW_WIDTH  # Start from the right side of the screen
            self.speed = -random.randrange(Goodie.MIN_SPEED, Goodie.MAX_SPEED + 1)
            self.minLeft = -size  # Minimum position for the goodie to move
        else:
            self.x = 0 - size  # Start from the left side of the screen
            self.speed = random.randrange(Goodie.MIN_SPEED, Goodie.MAX_SPEED + 1)

        # Choose correct image based on goodie type
        if self.goodie_type == 'shield':
            self.image = pygwidgets.Image(self.window, (self.x, self.y), Goodie.SHIELD_IMAGE)
        else:
            self.image = pygwidgets.Image(self.window, (self.x, self.y), Goodie.GOODIE_IMAGE)

        # Scale the image based on size
        percent = int((size * 100) / Goodie.MAX_SIZE)
        self.image.scale(percent, False)

    def update(self):
        # Update the goodie's position
        self.x += self.speed
        self.image.setLoc((self.x, self.y))

        # If the goodie has moved off-screen, it needs to be deleted
        if self.direction == Goodie.LEFT:
            if self.x < self.minLeft:
                return True  # Mark for deletion
            else:
                return False
        else:
            if self.x > WINDOW_WIDTH:
                return True  # Mark for deletion
            else:
                return False

    def draw(self):
        # Draw the goodie image
        self.image.draw()

    def collide(self, playerRect):
        # Check if the goodie has collided with the player
        return self.image.overlaps(playerRect)

# GoodieMgr class manages multiple goodies in the game
class GoodieMgr():
    GOODIE_RATE_LO = 90  # Lower bound for goodie spawn rate
    GOODIE_RATE_HI = 111  # Upper bound for goodie spawn rate

    def __init__(self, window):
        self.window = window
        self.reset()

    def reset(self):
        # Reset the goodie manager for a new game
        self.goodiesList = []  # List to store active goodies
        self.nFramesTilNextGoodie = GoodieMgr.GOODIE_RATE_HI  # Timer for next goodie spawn

    def update(self, thePlayerRect):
        nGoodiesHit = 0  # Number of goodies collected
        shieldPickedUp = False  # Flag to check if shield was picked up
        goodiesListCopy = self.goodiesList.copy()

        # Update each goodie in the list
        for oGoodie in goodiesListCopy:
            deleteMe = oGoodie.update()
            if deleteMe:
                self.goodiesList.remove(oGoodie)

            elif oGoodie.collide(thePlayerRect):
                # If the player collects a goodie
                if oGoodie.goodie_type == 'shield':
                    shieldPickedUp = True  # If shield is collected
                else:
                    nGoodiesHit += 1  # Count normal goodies collected
                self.goodiesList.remove(oGoodie)

        # Decrease the timer until the next goodie spawns
        self.nFramesTilNextGoodie -= 1
        if self.nFramesTilNextGoodie <= 0:
            # 5% chance to spawn a Shield Power-Up
            if random.random() < 0.05:
                oGoodie = Goodie(self.window, goodie_type='shield')
            else:
                oGoodie = Goodie(self.window, goodie_type='normal')

            self.goodiesList.append(oGoodie)
            # Reset spawn timer with random value
            self.nFramesTilNextGoodie = random.randrange(GoodieMgr.GOODIE_RATE_LO,
                                                          GoodieMgr.GOODIE_RATE_HI)

        return nGoodiesHit, shieldPickedUp  # Return goodies collected and shield status

    def draw(self):
        # Draw all active goodies
        for oGoodie in self.goodiesList:
            oGoodie.draw()
