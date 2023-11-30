from math import pi, asin, cos, sin
import pygame
from numpy import deg2rad, dot
import numpy
from settings import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, spawn_pos, health):
        super().__init__()
        self.SOURCE_IMAGE = pygame.image.load("images/spider_sprite.png")#.convert()
        self.SOURCE_IMAGE_RESOLUTION = (400, 800)
        self.scale = 1.5
        self.sprite_size = ()
        #self.SOURCE_IMAGE.set_colorkey((0, 0, 0))
        self.image = self.SOURCE_IMAGE
        self.position = list(spawn_pos)
        self.health = 100
        self.speed = 0.0
        self.enemy_screen_pos = [SCREEN_RES[0]/2, SCREEN_RES[1]/2]
        self.hitbox_width = self.SOURCE_IMAGE_RESOLUTION[0]
        self.screen_pos = [0, 0]
        print('Enemy class initialized')

# Points directly towards the player and moves forward. Does not reference waypoints.
    def move_to_player(self, player_x, player_y):
        enemy_x = self.position[0]
        enemy_y = self.position[1]
        delta_x = player_x - enemy_x
        delta_y = player_y - enemy_y
        vector_magnitude = (delta_x ** 2 + delta_y ** 2) ** (1 / 2)  # Pythagorean Theorem
        vector_to_player = [delta_x / vector_magnitude, delta_y / vector_magnitude]  # A unit vector

        distance_moving = [self.speed * vector_to_player[0], self.speed * vector_to_player[1]]
        self.position[0] += distance_moving[0]
        self.position[1] += distance_moving[1]


    def take_damage(self, damage_value):
        if self.screen_pos[0] < (SCREEN_RES[0]/2):
            if (self.screen_pos[0]+self.hitbox_width) > (SCREEN_RES[0]/2):
                self.health -= damage_value
                print(self.health)
        if self.health <= 0:
            self.kill()
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
        enemy_vector = [-delta_x * magnitude, -delta_y * magnitude]
        angle_between_vectors = numpy.dot(player_vector, enemy_vector)

        if enemy_vector[0] < 0:
            angle_to_player = asin(delta_y / distance_to_player)
        else:
            angle_to_player = pi - asin(delta_y / distance_to_player)
        delta_angle = player_rot - angle_to_player  # This is where my sprite problem was

        y_adjust = self.SOURCE_IMAGE_RESOLUTION[0] * 0.8 / distance_to_player * (1/self.scale)

        self.image_scale = abs(self.scale / (((delta_x**2 + delta_y**2)**(1/2))))   # This is a test
        self.sprite_size = (int(self.SOURCE_IMAGE_RESOLUTION[0] * self.image_scale),
                            int(self.SOURCE_IMAGE_RESOLUTION[1] * self.image_scale))
        self.hitbox_width = self.sprite_size[0]
        if self.sprite_size[1] > 1800:
            self.sprite_size = (900,1800)
        self.image = pygame.transform.scale(self.SOURCE_IMAGE, self.sprite_size)
        self.screen_pos = (self.enemy_screen_pos[0] - self.image.get_width() / 2, self.enemy_screen_pos[1] - self.image.get_height() / 2 + y_adjust)

        if delta_angle < 0:
            screen_shift = -(-delta_angle - pi)/fov  # Where the enemy will be drawn on screen (negative = left, positive = right)
        else:
            screen_shift = (delta_angle - pi) / fov
        # Shifts the enemies y-position on screen according to angle_to_screen
        self.screen_pos = (self.screen_pos[0] + screen_shift * (SCREEN_RES[0]/2), self.screen_pos[1])

        if angle_between_vectors > 5/6:  # Ensures the enemy is drawn only when the player can see it
            surface.blit(self.image, self.screen_pos)  # Draws the enemy on screen


enemies = pygame.sprite.Group()
