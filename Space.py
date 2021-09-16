import random
import pygame
import sys


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


class Enemy:
    def __init__(self, x, y) -> None:
        self.image = pygame.image.load("assets/meteor.png")
        self.enemyX = x
        self.enemyY = y
        self.velocity = 0.5

        # States: ready,falling, hit
        self.state = "ready"

    def move_vert(self):
        self.enemyY += self.velocity

    # Getters and setters

    def get_EnemyX(self):
        return self.enemyX

    def get_EnemyY(self):
        return self.enemyY

    def set_pos_change_x(self, val):
        self.set_pos_change_x = val


class Bullet:
    def __init__(self):
        self.image = pygame.image.load("assets/bullet.png")
        self.velocity = random.randrange(0, 1, 0.2)
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
        self.running = True
        self.clock = pygame.time.Clock()
        self.start_ticks = pygame.time.get_ticks()
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.set_window(screenWidth, screenHeight)
        self.set_assets()

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
                sys.exit()

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
                # remove out of bounds bullet
                if bullet.get_y() < 0:
                    self.bullets.remove(bullet)

                bullet.move_vert()
                self.draw_bullet(bullet)

            elif bullet.state == "hit":
                # The bullet and the enemy should be removed from the screen
                pass

        for enemy in self.enemies:
            if enemy.state == "falling":
                enemy.move_vert()
                self.draw_enemy(enemy)
            elif enemy == "hit":
                pass
                # Game over

        self.spawn_enemy()
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

    def draw_enemy(self, enemy):
        x = enemy.get_EnemyX()
        y = enemy.get_EnemyY()
        self.screen.blit(enemy.image, (x, y))

    def spawn_enemy(self):
        spawn_interval = (pygame.time.get_ticks() - self.start_ticks)/1000
        if spawn_interval > 2:
            random_loc_x = random.randint(30, self.screenWidth-30)
            enemy = Enemy(random_loc_x, 0)
            enemy.state = "falling"
            self.enemies.append(enemy)

            # resets the timer
            self.start_ticks = pygame.time.get_ticks()

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
        self.enemies = []
        # Array of bullets
        self.bullets = []
        self.bulletCount = 0


if __name__ == "__main__":
    Space = Game(800, 600)
    Space.on_run()
