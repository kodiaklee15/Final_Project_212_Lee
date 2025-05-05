# Laser.py
import pygame
from Constants import *
import math

# Constants for the player's laser
LASER_SPEED = 20
LASER_COLOR = (173, 216, 230)   # Blue color
LASER_WIDTH = 4
LASER_HEIGHT = 15

# Laser class for the player
class Laser:
    def __init__(self, x, y):
        # Initialize laser's position
        self.x = x
        self.y = y

    def update(self):
        # Update the laser's position (move it upwards)
        self.y -= LASER_SPEED

    def draw(self, window):
        # Draw the laser as a rectangle
        laser_rect = pygame.Rect(int(self.x - LASER_WIDTH // 2), int(self.y), LASER_WIDTH, LASER_HEIGHT)
        pygame.draw.rect(window, LASER_COLOR, laser_rect)

    def is_dead(self):
        # Check if the laser has gone off screen (past the top)
        return self.y + LASER_HEIGHT < 0


# Constants for the enemy's laser
ENEMY_LASER_SPEED = 7
ENEMY_LASER_COLOR = (255, 102, 102)  # Red color
ENEMY_LASER_RADIUS = 4

# EnemyLaser class for the lasers fired by the enemies
class EnemyLaser:
    def __init__(self, x, y):
        # Initialize enemy laser's position
        self.x = x
        self.y = y

    def update(self):
        # Update the enemy laser's position (move it downwards)
        self.y += ENEMY_LASER_SPEED

    def draw(self, window):
        # Draw the enemy laser as a circle
        pygame.draw.circle(window, ENEMY_LASER_COLOR, (int(self.x), int(self.y)), ENEMY_LASER_RADIUS)

    def is_off_screen(self):
        # Check if the enemy laser has gone off screen (past the bottom)
        return self.y > GAME_HEIGHT
    

# Constants for the special laser (when the player collects 10 gold)
SPECIAL_LASER_SPEED = 10

# SpecialLaser class for the laser fired when the player has 10 gold
class SpecialLaser:
    def __init__(self, x, y, angle_degrees):
        # Initialize special laser with angle and position
        self.x = x
        self.y = y
        # Convert angle to radians for movement calculations
        self.angle = math.radians(angle_degrees)

    def update(self):
        # Update the special laser's position based on its angle
        self.x += SPECIAL_LASER_SPEED * math.cos(self.angle)
        self.y -= SPECIAL_LASER_SPEED * math.sin(self.angle)

    def draw(self, window):
        # Draw the special laser as a small rectangle
        laser_rect = pygame.Rect(int(self.x - 2), int(self.y), 4, 15)
        pygame.draw.rect(window, (173, 216, 230), laser_rect)

    def is_dead(self):
        # Check if the special laser has gone off screen
        return (self.y + 15 < 0 or self.x < 0 or self.x > WINDOW_WIDTH)
