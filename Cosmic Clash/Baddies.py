# Baddie and BaddieMgr classes

import pygame
import pygwidgets
import random
from Constants import *
from Laser import EnemyLaser

# Baddie class represents an enemy character
class Baddie():
    MIN_SIZE = 20
    MAX_SIZE = 40
    MIN_SPEED = 1
    MAX_SPEED = 8
    # Load the image of the baddie once to avoid reloading it repeatedly
    BADDIE_IMAGE = pygame.image.load('images/alien.png')

    def __init__(self, window):
        self.window = window
        # Random size for the baddie
        size = random.randrange(Baddie.MIN_SIZE, Baddie.MAX_SIZE + 1)
        # Random initial position for the baddie
        self.x = random.randrange(0, WINDOW_WIDTH - size)
        self.y = 0 - size  # Start the baddie offscreen (above the window)
        # Load and scale the baddie's image
        self.image = pygwidgets.Image(self.window, (self.x, self.y), Baddie.BADDIE_IMAGE)

        percent = (size * 100) / Baddie.MAX_SIZE
        self.image.scale(percent, False)
        
        # Random speed and horizontal movement direction
        self.speed = random.randrange(Baddie.MIN_SPEED, Baddie.MAX_SPEED + 1)
        self.xSpeed = random.choice([-1, 1]) * random.randint(2, 5)
        
        # Baddies that are larger and slower can shoot
        self.can_shoot = size >= 30 and self.speed <= 3
        # Random cooldown period for shooting
        self.shoot_cooldown = random.randint(60, 120)

    def update(self):
        # Update the baddie's position (move diagonally)
        self.x += self.xSpeed
        self.y += self.speed

        # Bounce off the left and right walls
        if self.x <= 0 or self.x + self.image.getRect().width >= WINDOW_WIDTH:
            self.xSpeed *= -1  # Reverse direction

        self.image.setLoc((self.x, self.y))

        # Check if the baddie has moved off the screen (bottom)
        if self.y > GAME_HEIGHT:
            return True  # Mark for deletion
        else:
            return False

    def draw(self):
        # Draw the baddie image
        self.image.draw()

    def collide(self, playerRect):
        # Check if the baddie has collided with the player
        return self.image.overlaps(playerRect)

# BaddieMgr class manages multiple baddies
class BaddieMgr():
    def __init__(self, window):
        self.window = window
        self.enemy_lasers = []  # List to store lasers fired by baddies
        self.base_spawn_rate = 14  # Base spawn rate for baddies
        self.min_spawn_rate = 2   # Minimum spawn rate
        self.current_spawn_rate = self.base_spawn_rate
        self.nFramesTilNextBaddie = self.current_spawn_rate
        self.previous_spawn_rate = self.base_spawn_rate
        self.previous_spawn_rate = self.base_spawn_rate
        self.spawn_rate_changed = False
        self.message_timer = 0
        self.reset()

    def reset(self):
        # Reset the baddie manager for a new game
        self.baddiesList = []  # List to store active baddies
        self.current_spawn_rate = self.base_spawn_rate
        self.nFramesTilNextBaddie = self.current_spawn_rate
        self.enemy_lasers = []
        self.previous_spawn_rate = self.base_spawn_rate
        self.spawn_rate_changed = False
        self.message_timer = 0

    def update(self, score):
        # Update baddies and their behavior based on score
        new_spawn_rate = max(self.min_spawn_rate, self.base_spawn_rate - (score // 750))

        # Check if the spawn rate has changed
        if new_spawn_rate != self.current_spawn_rate:
            self.current_spawn_rate = new_spawn_rate
            self.previous_spawn_rate = new_spawn_rate
            self.spawn_rate_changed = True
            self.message_timer = 60  # Show message for 60 frames (1.5 seconds)

        # Count down to spawn the next baddie
        self.nFramesTilNextBaddie -= 1
        if self.nFramesTilNextBaddie <= 0:
            # Add a new baddie to the list
            self.baddiesList.append(Baddie(self.window))
            self.nFramesTilNextBaddie = self.current_spawn_rate

        # Handle baddie updates (moving them and checking for removal)
        nBaddiesRemoved = 0
        baddiesListCopy = self.baddiesList.copy()
        for oBaddie in baddiesListCopy:
            deleteMe = oBaddie.update()
            if deleteMe:
                self.baddiesList.remove(oBaddie)
                nBaddiesRemoved += 1

            # Handle baddie shooting
            if oBaddie.can_shoot:
                oBaddie.shoot_cooldown -= 1
                if oBaddie.shoot_cooldown <= 0:
                    # Fire a laser from the baddie
                    laserX = oBaddie.x + oBaddie.image.getRect().width // 2
                    laserY = oBaddie.y + oBaddie.image.getRect().height
                    self.enemy_lasers.append(EnemyLaser(laserX, laserY))
                    oBaddie.shoot_cooldown = random.randint(60, 120)

        # Update enemy lasers
        for laser in self.enemy_lasers[:]:
            laser.update()
            if laser.is_off_screen():
                self.enemy_lasers.remove(laser)

        # Handle spawn rate message display
        if self.spawn_rate_changed:
            self.message_timer -= 1
            if self.message_timer <= 0:
                self.spawn_rate_changed = False

        # Return the count of baddies that were removed
        return nBaddiesRemoved

    def draw(self):
        # Draw all baddies and their lasers
        for oBaddie in self.baddiesList:
            oBaddie.draw()
        for laser in self.enemy_lasers:
            laser.draw(self.window)

    def hasPlayerHitBaddie(self, playerRect):
        # Check if any baddie has collided with the player
        for oBaddie in self.baddiesList:
            if oBaddie.collide(playerRect):
                return True
        return False
