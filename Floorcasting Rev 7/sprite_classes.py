import random
from math import pi, asin, cos, sin
import pygame
from numpy import deg2rad, dot
import numpy
from settings import *
from maps import locate_zone, generate_spawns
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, areas_open, wave):
        super().__init__()
        self.SOURCE_IMAGE = pygame.image.load("images/spider_sprite.png")#.convert()
        self.SOURCE_IMAGE_RESOLUTION = (400, 800)
        self.scale = 1.5
        self.spawn_list = generate_spawns()
        if areas_open == 4:
            number = random.randint(0, 4)
        elif areas_open == 3:
            number = random.randint(0, 4)
        elif areas_open == 2:
            number = random.randint(0, 2)
        else:
            number = 0
        self.position = self.spawn_list[number]
        self.sprite_size = ()
        self.hit_frequency = 50
        self.hit_counter = self.hit_frequency + 1
        self.damage = 25
        self.image = self.SOURCE_IMAGE
        self.health = wave * damage_value + random.randint(0, 3) * damage_value
        self.default_speed = 0.02 + 0.005 * random.randint(0, 3)
        self.current_speed = self.default_speed
        self.enemy_screen_pos = [SCREEN_RES[0]/2, SCREEN_RES[1]/2]
        self.hitbox_width = self.SOURCE_IMAGE_RESOLUTION[0]
        self.screen_pos = [0, 0]
        self.zone = 0
        self.destination = False

    # Points directly towards the player and moves forward. Does not reference waypoints.
    def point_and_seek(self):
        enemy_x = self.position[0]
        enemy_y = self.position[1]
        delta_x = self.destination[0] - enemy_x
        delta_y = self.destination[1] - enemy_y
        vector_magnitude = (delta_x ** 2 + delta_y ** 2) ** (1 / 2)  # Pythagorean Theorem
        vector_to_player = [delta_x / vector_magnitude, delta_y / vector_magnitude]  # A unit vector
        distance_moving = [self.current_speed * vector_to_player[0], self.current_speed * vector_to_player[1]]
        self.position[0] += distance_moving[0]
        self.position[1] += distance_moving[1]

    def generate_destination(self, player_zone, player_x, player_y):
        self.destination = False
        if player_zone == self.zone:
            self.destination = (player_x, player_y)
        elif 13.3 < self.position[1] < 13.8:
            if player_zone == self.zone:
                self.point_and_seek(player_x, player_y)
                return
            elif player_zone < self.zone:
                self.destination = (99, 13.5)  # Goes to the right as far as possible
                return
            elif player_zone > self.zone:
                self.destination = (0, 13.5)  # Goes to the left as far as possible
                return
            else:
                self.destination = (player_x, player_y)
                return
        else:
            self.destination = (self.position[0], 13.5)

        kill_radius = 0.8
        if (player_x - kill_radius) < self.position[0] < (player_x + kill_radius) and (player_y - kill_radius) < self.position[1] < (player_y + kill_radius):
            if self.hit_counter > self.hit_frequency:
                print("Hitting player")
                player_damage = self.damage
                self.hit_counter = 0
            else:
                self.hit_counter += 1
                player_damage = 0
        else:
            player_damage = 0
        return player_damage

    def get_distance(self, enemy_x, enemy_y):
        delta_x = self.position[0] - enemy_x
        delta_y = self.position[1] - enemy_y
        vector_magnitude = (delta_x ** 2 + delta_y ** 2) ** (1 / 2)
        return vector_magnitude

    def move_to_player(self, player_x, player_y, player_zone, zone_map):
        self.zone = locate_zone(self.position, zone_map)
        player_damage = self.generate_destination(player_zone, player_x, player_y)
        self.point_and_seek()
        return player_damage

    def take_damage(self, damage_value, points, number_killed, number_of_enemies):
        if self.screen_pos[0] < (SCREEN_RES[0]/2):
            if (self.screen_pos[0]+self.hitbox_width) > (SCREEN_RES[0]/2):
                self.health -= damage_value
                points += 10
        if self.health <= 0:
            self.kill()
            points += 50
            number_killed += 1
            number_of_enemies -= 1
        return points, number_killed, number_of_enemies


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
            self.sprite_size = (900, 1800)
            self.current_speed = 0
        else:
            self.current_speed = self.default_speed
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
