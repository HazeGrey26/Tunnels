from math import pi, atan
import pygame
from numpy import deg2rad
from settings import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, spawn_pos, health):
        super().__init__()
        self.SOURCE_IMAGE = pygame.image.load("images/enemy_default.png").convert()
        self.SOURCE_IMAGE_RESOLUTION = (100, 100)
        self.image_scale = 1
        self.sprite_size = (int(self.SOURCE_IMAGE_RESOLUTION[0] * self.image_scale), int(self.SOURCE_IMAGE_RESOLUTION[1] * self.image_scale))
        self.SOURCE_IMAGE.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.SOURCE_IMAGE, self.sprite_size)
        self.position = spawn_pos
        self.health = 100
        self.enemy_screen_pos = [SCREEN_RES[0]/2, SCREEN_RES[1]/2]
        self.rect = (200, (SCREEN_RES[1]/2)-(self.image.get_height()/2))
        print('initialized')

    def move(self, position, speed, player_pos):
        # Some code to move the enemy
        return position

    def take_damage(self, health, damage_value):
        self.health -= damage_value
        if self.health <= 0:
            return True  # Dead
        else:
            return False  # Not Dead

    def draw_enemy(self, surface, hres, rot, player_pos_y, player_pos_x, halfvres):
        player_rot = 2*pi - (rot % (2 * pi))  # Caps player rot to 2pi and makes it increase towards counterclockwise
        fov = deg2rad(FIELD_OF_VIEW/2)  # Converts the player's field of view to radians and divides it by 2
        delta_x = player_pos_x - self.position[0]
        delta_y = player_pos_y - self.position[1]
        distance_to_player = (delta_x**2 + delta_y**2)**(1/2)  # Pythagorean Theorem
        angle_to_player = atan(delta_y / delta_x) + pi/2
        delta_angle = player_rot - angle_to_player  # Negative when enemy is to the left of where the player is looking

        print(f"Dist: {distance_to_player}, Angle: {angle_to_player}, Rot: {player_rot}, Coord: {delta_x},{delta_y}")

        self.image_scale = abs(1 / (distance_to_player**(1/2)))  # This is a test
        self.sprite_size = (int(self.SOURCE_IMAGE_RESOLUTION[0] * self.image_scale),
                            int(self.SOURCE_IMAGE_RESOLUTION[1] * self.image_scale))
        self.image = pygame.transform.scale(self.SOURCE_IMAGE, self.sprite_size)
        screen_pos = (self.enemy_screen_pos[0] - self.image.get_height() / 2, self.enemy_screen_pos[1] - self.image.get_width() / 2)

        angle_to_screen = delta_angle/fov  # Where the enemy will be drawn on screen (negative = left, positive = right)
        # Shifts the enemies y-position on screen according to angle_to_screen
        screen_pos = (screen_pos[0] + angle_to_screen * (SCREEN_RES[0]/2), screen_pos[1])

        if -1 < angle_to_screen < 1:  # Ensures the enemy is drawn only when the player can see it
            surface.blit(self.image, screen_pos)  # Draws the enemy on screen



enemies = pygame.sprite.Group()
