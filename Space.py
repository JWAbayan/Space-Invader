import random
import pygame
import sys


class Player:
    def __init__(self):
        self.image = pygame.image.load("assets/player.png")
        self.playerX = 370
        self.playerY = 480
        self.pos_change_x = 0
        self.collider = pygame.Rect(self.playerX, self.playerY, 32, 32)

    def get_PlayerX(self):
        return self.playerX

    def get_PlayerY(self):
        return self.playerY

    def move_hori(self, screenWidth):
        new_playerX = self.playerX + self.pos_change_x

        # Checks if the new player x is inside the boundary
        # x > 30 and x < screenwidth - (30 + player image pixel)
        if new_playerX > 30 and new_playerX < screenWidth - 94:
            self.playerX = new_playerX
            self.collider.x = new_playerX

    def move_vert(self):
        self.playerY += self.pos_change_x

    def in_collision(self):
        pass


class Enemy:
    def __init__(self, x, y) -> None:
        self.image = pygame.image.load("assets/meteor.png")
        self.enemyX = x
        self.enemyY = y
        self.velocity = random.uniform(0.1, 0.5)
        self.collider = pygame.Rect(self.enemyX, self.enemyY, 32, 32)
        # States: ready,falling, hit
        self.state = "ready"

    def move_vert(self):
        self.enemyY += self.velocity
        self.collider.y = self.enemyY
    # Getters and setters

    def get_EnemyX(self):
        return self.enemyX

    def get_EnemyY(self):
        return self.enemyY

    def set_pos_change_x(self, val):
        self.set_pos_change_x = val

    def in_collision(self):
        pass


class Bullet:
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/bullet.png")
        self.velocity = 0.5
        self.bulletX = x
        self.bulletY = y
        self.collider = pygame.Rect(0, 0, 8, 8)
        # States: ready, fired, hit
        self.state = "ready"

    def move_vert(self):
        self.bulletY -= self.velocity
        self.collider.y = self.bulletY

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

        # Set window and assets
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

                # RIGHT MOVEMENT
                if event.key == pygame.K_RIGHT:
                    self.player.pos_change_x = 0.2

                # LEFT MOVEMENT
                if event.key == pygame.K_LEFT:
                    self.player.pos_change_x = -0.2

                # FIRE
                if event.key == pygame.K_SPACE:
                    self.fire_bullet()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.player.pos_change_x = 0

    def on_render(self):
        self.screen.fill((0, 0, 0))

        for bullet in self.bullets:
            if bullet.state == "fired":
                # remove bullet if out of bound
                if bullet.get_y() < 0:
                    self.bullets.remove(bullet)

                bullet.move_vert()
                self.draw_bullet(bullet)

            elif bullet.state == "hit":
                # The bullet and the enemy should be removed from the screen
                pass

        for enemy in self.enemies:
            if enemy.state == "falling":

                # remove enemy if out of bound
                if enemy.get_EnemyY() > self.screenHeight:
                    self.enemies.remove(enemy)

                enemy.move_vert()
                self.draw_enemy(enemy)
            elif enemy == "hit":
                pass
                # Game over

        self.spawn_enemy()
        self.player.move_hori(self.screenWidth)
        self.collision_detection()
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

    # Spawns enemy between time intervals
    def spawn_enemy(self):

        spawn_timer = (pygame.time.get_ticks() - self.start_ticks)/1000

        if spawn_timer > 1:
            random_loc_x = random.randint(30, self.screenWidth-30)
            enemy = Enemy(random_loc_x, 0)
            enemy.state = "falling"
            self.enemies.append(enemy)
            # resets the timer
            self.start_ticks = pygame.time.get_ticks()

    # Spawn bullet relative to the player's position
    def fire_bullet(self):
        x = self.player.get_PlayerX() + 25
        y = self.player.get_PlayerY() - 10
        bullet = Bullet(x, y)
        bullet.set_state("fired")
        bullet.collider.x = x
        self.bullets.append(bullet)

    def collision_detection(self):
        for enemy in self.enemies:
            enemy_collider = enemy.collider
            if self.player.collider.colliderect(enemy_collider):
                self.running = False
            for bullet in self.bullets:
                if bullet.collider.colliderect(enemy_collider):
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)

    def set_window(self, width, height):
        title = "Space Game"
        icon = pygame.image.load('assets/spaceship.png')

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        pygame.display.set_icon(icon)

    def set_assets(self):
        self.player = Player()
        self.enemies = []
        self.bullets = []


if __name__ == "__main__":
    Space = Game(800, 600)
    Space.on_run()
