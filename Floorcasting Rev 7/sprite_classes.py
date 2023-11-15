from math import pi, asin, atan, acos, cos, sin
import pygame
from numpy import deg2rad, dot
import numpy
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
        rot = rot - pi/2  # Sets rot to 0 when player is facing along the positive y-axis
        player_rot = 2*pi - (rot % (2 * pi))  # Caps player rot to 2pi and makes it increase towards counterclockwise
        fov = deg2rad(FIELD_OF_VIEW/2)  # Converts the player's field of view to radians and divides it by 2
        delta_x = player_pos_x - self.position[0]
        delta_y = player_pos_y - self.position[1]
        magnitude = 1/((delta_x**2 + delta_y**2)**(1/2))  # Magnitude of a vector formula
        distance_to_player = (delta_x ** 2 + delta_y ** 2) ** (1 / 2)  # Pythagorean Theorem
        player_vector = [cos(player_rot), sin(player_rot)]
        rotation_vector = [cos(2*pi - ((rot - pi/2) % (2 * pi))), sin(2*pi - ((rot - pi/2) % (2 * pi)))]
        enemy_vector = [-delta_x * magnitude, -delta_y * magnitude]
        angle_between_vectors = numpy.dot(player_vector, enemy_vector)

        if enemy_vector[0] < 0:
            angle_to_player = asin(delta_y / distance_to_player)
            print("asin")
        else:
            angle_to_player = pi - asin(delta_y / distance_to_player)
            print("alt asin")
        delta_angle = player_rot - angle_to_player  # This is where my sprite problem is

        self.image_scale = abs(1 / (((delta_x**2 + delta_y**2)**(1/2)) ** (1 / 2)))   # This is a test
        self.sprite_size = (int(self.SOURCE_IMAGE_RESOLUTION[0] * self.image_scale),
                            int(self.SOURCE_IMAGE_RESOLUTION[1] * self.image_scale))
        self.image = pygame.transform.scale(self.SOURCE_IMAGE, self.sprite_size)
        screen_pos = (self.enemy_screen_pos[0] - self.image.get_height() / 2, self.enemy_screen_pos[1] - self.image.get_width() / 2)

        screen_shift = (delta_angle - pi)/fov  # Where the enemy will be drawn on screen (negative = left, positive = right)

        # Shifts the enemies y-position on screen according to angle_to_screen
        screen_pos = (screen_pos[0] + screen_shift * (SCREEN_RES[0]/2), screen_pos[1])
        print(f"P_Rot: {int(player_rot)} dlta {delta_angle}\nplrAng {angle_to_player}\nEVec {enemy_vector}")

        if angle_between_vectors > 5/6:  # Ensures the enemy is drawn only when the player can see it
            surface.blit(self.image, screen_pos)  # Draws the enemy on screen
            print("True")


enemies = pygame.sprite.Group()
