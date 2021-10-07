import pygame
import random
from enum import auto, Enum


class States(Enum):
    READY = auto()
    MOVING = auto()


class Player:
    def __init__(self):
        self.image = pygame.image.load("assets/player.png")
        self.playerX = 370
        self.playerY = 480
        self.velocity_x = 0
        self.collider = pygame.Rect(self.playerX, self.playerY, 32, 32)

    def get_X(self):
        return self.playerX

    def get_Y(self):
        return self.playerY

    def move_hori(self, screenWidth, delta_time):
        new_playerX = self.playerX + self.velocity_x * delta_time

        # Checks if the new player x is inside the boundary
        # x > 30 and x < screenwidth - (30 + player image pixel)
        if new_playerX > 30 and new_playerX < screenWidth - 94:
            self.playerX = new_playerX
            self.collider.x = new_playerX

    def move_vert(self):
        self.playerY += self.velocity_x

    def in_collision(self):
        pass


class Enemy:
    def __init__(self, x, y) -> None:
        self.image = pygame.image.load("assets/meteor.png")
        self.enemyX = x
        self.enemyY = y
        self.velocity = random.uniform(0.1, 0.5)
        self.collider = pygame.Rect(self.enemyX, self.enemyY, 32, 32)
        self.state = States.READY

    def move_vert(self, delta_time):
        self.enemyY += self.velocity * delta_time
        self.collider.y = self.enemyY

    def get_X(self):
        return self.enemyX

    def get_Y(self):
        return self.enemyY

    def in_collision(self):
        pass


class Bullet:
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/bullet.png")
        self.velocity = 0.5
        self.bulletX = x
        self.bulletY = y
        self.collider = pygame.Rect(0, 0, 8, 8)
        self.state = States.READY

    def move_vert(self, delta_time):
        self.bulletY -= self.velocity * delta_time
        self.collider.y = self.bulletY

    def get_velocity(self):
        return self.velocity

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def set_X(self, x):
        self.bulletX = x

    def set_Y(self, y):
        self.bulletY = y

    def get_X(self):
        return self.bulletX

    def get_Y(self):
        return self.bulletY
