import random
import pygame
import sys
import math

from pygame.time import get_ticks
from Entity import Player, Bullet, Enemy


class Game:
    def __init__(self, screenWidth, screenHeight):
        # Initialize pygame modules
        pygame.init()

        self.running = True
        self.game_clock = pygame.time.Clock()
        self.game_start_ticks = pygame.time.get_ticks()
        self.game_score = 0
        self.game_level = 1
        self.spawn_speed = 1
        self.spawn_enemy_total = 1
        self.game_fps = 60

        # Set window and assets
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.set_window(screenWidth, screenHeight)
        self.set_assets()

    def set_assets(self):
        self.player = Player()
        self.enemies = []
        self.bullets = []
        self.game_font = pygame.font.Font("assets/cmd_font.ttf", 24)
        self.score_text = self.game_font.render(
            str(self.game_score), True, (255, 255, 255), (0, 0, 0))
        self.game_fps = self.game_font.render(
            str(self.game_clock.get_fps()), True, (255, 255, 255), (0, 0, 0))

    def on_run(self):
        # Game Loop
        while self.running:
            # Checks for events
            self.on_event()
            # Render assets
            self.on_render()
            # Update the display
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
                    self.player.velocity_x = 0.4

                # LEFT MOVEMENT
                if event.key == pygame.K_LEFT:
                    self.player.velocity_x = -0.4

                # FIRE
                if event.key == pygame.K_SPACE:
                    self.fire_bullet()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.player.velocity_x = 0

    def on_render(self):
        self.screen.fill((0, 0, 0))

        for bullet in self.bullets:
            if bullet.state == "fired":
                # remove bullet if out of bounds
                if bullet.get_y() < 0:
                    self.bullets.remove(bullet)

                bullet.move_vert(self.game_clock.get_time())
                self.draw_bullet(bullet)

        # Render all spawned enemy
        for enemy in self.enemies:
            if enemy.state == "falling":

                # remove enemy if out of bounds
                if enemy.get_EnemyY() > self.screenHeight:
                    pass
                    self.enemies.remove(enemy)

                enemy.move_vert(self.game_clock.get_time())
                self.draw_enemy(enemy)
            elif enemy == "hit":
                pass
                # Game over

        self.spawn_enemy()
        self.player.move_hori(self.screenWidth, self.game_clock.get_time())
        self.draw_player()

        # self.collision_detection()

        self.screen.blit(self.score_text, (30, 30))
        self.show_fps()

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
        spawn_timer = (pygame.time.get_ticks() - self.game_start_ticks)/1000
        increase_level_timer = int(pygame.time.get_ticks() / 1000)

        # if increase_level_timer % 10 == 0 and increase_level_timer > 0 and increase_level_timer > 0:
        #     print("in")
        #     self.spawn_speed = self.spawn_speed - 0.1

        if spawn_timer > 0.1:
            for i in range(self.spawn_enemy_total):
                random_loc_x = random.randint(30, self.screenWidth-30)
                enemy = Enemy(random_loc_x, 0)
                enemy.state = "falling"
                self.enemies.append(enemy)
            # resets the timer
            self.game_start_ticks = pygame.time.get_ticks()

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
                self.reset_game()

            for bullet in self.bullets:
                if bullet.collider.colliderect(enemy_collider):
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.update_score(1)

    def update_score(self, val):
        if val != 0:
            self.game_score += val
        else:
            self.game_score = val

        self.score_text = self.game_font.render(
            str(self.game_score), True, (255, 255, 255), (0, 0, 0))

    def reset_game(self):
        self.game_score = 0
        self.game_level = 1
        self.enemies.clear()
        self.bullets.clear()
        self.player.playerX = 370
        self.player.playerY = 480
        self.update_score(0)

    def set_window(self, width, height):
        title = "Space Game"
        icon = pygame.image.load('assets/spaceship.png')

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        pygame.display.set_icon(icon)

    def increase_level(self):
        pass

    def show_fps(self):
        self.game_clock.tick(120)
        self.game_fps = self.game_font.render(
            f"FPS: {math.ceil(self.game_clock.get_fps())}", True, (255, 255, 255), (0, 0, 0))
        self.screen.blit(self.game_fps,
                         (self.screenWidth - 90, 30))


if __name__ == "__main__":
    Space = Game(800, 600)
    Space.on_run()
