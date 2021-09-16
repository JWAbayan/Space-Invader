import pygame
import math


class Player:
    def __init__(self):
        self.image = pygame.image.load("assets/player.png")
        self.playerX = 370
        self.playerY = 480
        self.pos_change_x = 0

    def get_PlayerX(self):
        return self.playerX

    def get_PlayerY(self):
        return self.playerY

    def move_hori(self):
        self.playerX += self.pos_change_x

    def move_vert(self):
        self.playerY += self.pos_change_x


class Bullet:
    def __init__(self):
        self.image = pygame.image.load("assets/bullet.png")
        self.velocity = 0.5
        self.bulletX = 0
        self.bulletY = 0
        # States: ready, fired, hit
        self.state = "ready"

    def move_vert(self):
        self.bulletY -= self.velocity

    def get_velocity(self):
        return self.velocity

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def set_x(self, x):
        self.bulletX = x

    def set_y(self, y):
        self.bulletY = y

    def get_x(self):
        return self.bulletX

    def get_y(self):
        return self.bulletY


class Game:
    def __init__(self, screenWidth, screenHeight):
        # Initialize pygame modules
        pygame.init()

        self.set_window(screenWidth, screenHeight)
        self.set_assets()
        self.running = True

    def on_run(self):
        # Game Loop
        while self.running:
            self.on_event()
            self.on_render()
            pygame.display.update()

    def on_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Player move set
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.player.pos_change_x = 0.2

                if event.key == pygame.K_LEFT:
                    self.player.pos_change_x = -0.2

                if event.key == pygame.K_SPACE:
                    self.fire_bullet()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.player.pos_change_x = 0

    def on_render(self):
        self.screen.fill((0, 0, 0))

        for bullet in self.bullets:
            if bullet.state == "fired":
                if bullet.get_y() < 0:
                    self.bullets.remove(bullet)
                bullet.move_vert()
                self.draw_bullet(bullet)
               #print(f"Y-COOR: {bullet.get_y()}")
        self.player.move_hori()
        self.draw_player()

    def draw_player(self):
        player_image = self.player.image
        x = self.player.get_PlayerX()
        y = self.player.get_PlayerY()

        self.screen.blit(player_image, (x, y))

    def draw_bullet(self, bullet):
        x = bullet.get_x()
        y = bullet.get_y()

        self.screen.blit(bullet.image, (x, y))

    def fire_bullet(self):
        bullet = Bullet()
        bullet.set_state("fired")
        x = self.player.get_PlayerX() + 25
        y = self.player.get_PlayerY() - 10
        bullet.set_x(x)
        bullet.set_y(y)

        self.bullets.append(bullet)

    def set_window(self, width, height):
        title = "Space Game"
        icon = pygame.image.load('assets/spaceship.png')

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        pygame.display.set_icon(icon)

    def set_assets(self):
        self.player = Player()
        # Array of bullets
        self.bullets = []
        self.bulletCount = 0


if __name__ == "__main__":
    Space = Game(800, 600)
    Space.on_run()
