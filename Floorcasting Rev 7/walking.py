import pygame
import numpy
from math import pi
from settings import *


def movement(posx, posy, rot, keys, timer, gun_bob, map1, sens, vertical_angle):
    if keys[ord('e')]:
        vertical_angle += 5
    elif keys[ord('q')]:
        vertical_angle -= 5

    if keys[pygame.K_LEFT] or keys[ord('a')]:  # Detects if the 'a' or left arrow is pressed
        tempx = posx - numpy.cos(rot+pi/2) * PLAYER_SPEED * timer  # For collision avoidance
        tempy = posy - numpy.sin(rot+pi/2) * PLAYER_SPEED * timer  # For collision avoidance

        if map1[round(tempx - 0.5)][round(tempy - 0.5)] == 0:  # For collision avoidance
            posx = tempx
            posy = tempy
    elif keys[pygame.K_RIGHT] or keys[ord('d')]:
        tempx = posx + numpy.cos(rot+pi/2) * PLAYER_SPEED * timer  # For collision avoidance
        tempy = posy + numpy.sin(rot+pi/2) * PLAYER_SPEED * timer  # For collision avoidance

        if map1[round(tempx - 0.5)][round(tempy - 0.5)] == 0:  # For collision avoidance
            posx = tempx
            posy = tempy

    if keys[pygame.K_UP] or keys[ord('w')]:
        tempx = posx + numpy.cos(rot) * PLAYER_SPEED * 2 * timer  # For collision avoidance
        tempy = posy + numpy.sin(rot) * PLAYER_SPEED * 2 * timer  # For collision avoidance

        if map1[round(tempx-0.5)][round(tempy-0.5)] == 0:  # For collision avoidance
            if keys[pygame.K_LSHIFT]:
                posx = posx + numpy.cos(rot) * PLAYER_SPEED * 2 * timer  # Increments player position (sprint)
                posy = posy + numpy.sin(rot) * PLAYER_SPEED * 2 * timer  # Uses sin and cos because the player may be moving in a diagonal direction
                if not pygame.mixer.Channel(11).get_busy():
                    pygame.mixer.Channel(10).fadeout(250)
                    pygame.mixer.Channel(11).play(pygame.mixer.Sound('sounds/run.mp3'))
            else:
                posx = posx + numpy.cos(rot) * PLAYER_SPEED * timer  # Increments player position (walk)
                posy = posy + numpy.sin(rot) * PLAYER_SPEED * timer  # Uses sin and cos because the player may be moving in a diagonal direction
                if not pygame.mixer.Channel(10).get_busy():
                    pygame.mixer.Channel(11).fadeout(250)
                    pygame.mixer.Channel(10).play(pygame.mixer.Sound('sounds/walk.mp3'))

    elif keys[pygame.K_DOWN] or keys[ord('s')]:
        tempx = posx - numpy.cos(rot) * PLAYER_SPEED * timer  # For collision avoidance
        tempy = posy - numpy.sin(rot) * PLAYER_SPEED * timer  # For collision avoidance

        if map1[round(tempx-0.5)][round(tempy-0.5)] == 0:
            posx = tempx  # Increments player position
            posy = tempy
            if not pygame.mixer.Channel(10).get_busy():
                pygame.mixer.Channel(11).fadeout(250)
                pygame.mixer.Channel(10).play(pygame.mixer.Sound('sounds/walk.mp3'))
    
    else:
        pygame.mixer.Channel(10).fadeout(250)
        pygame.mixer.Channel(11).fadeout(250)

    return posx, posy, rot, gun_bob, vertical_angle  # Outputs the player's position and rotation
