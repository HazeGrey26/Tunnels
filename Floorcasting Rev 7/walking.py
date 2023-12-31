import pygame
import numpy
from math import pi
from settings import *


def movement(posx, posy, rot, keys, timer, gun_bob, map1, vertical_angle):
    if keys[pygame.K_LEFT] or keys[ord('a')]:  # Detects if the 'a' or left arrow is pressed
        tempx = posx - numpy.cos(rot+pi/2) * PLAYER_SPEED * timer  # For collision avoidance
        tempy = posy - numpy.sin(rot+pi/2) * PLAYER_SPEED * timer  # For collision avoidance
        if map1[round(tempx - 0.5)][round(posy - 0.5)] == 0:
            posx = tempx
            if not pygame.mixer.Channel(10).get_busy():
                pygame.mixer.Channel(11).fadeout(250)
                pygame.mixer.Channel(10).play(pygame.mixer.Sound('sounds/walk.mp3'))
        if map1[round(posx - 0.5)][round(tempy - 0.5)] == 0:
            posy = tempy
            if not pygame.mixer.Channel(10).get_busy():
                pygame.mixer.Channel(11).fadeout(250)
                pygame.mixer.Channel(10).play(pygame.mixer.Sound('sounds/walk.mp3'))

    elif keys[pygame.K_RIGHT] or keys[ord('d')]:
        tempx = posx + numpy.cos(rot+pi/2) * PLAYER_SPEED * timer  # For collision avoidance
        tempy = posy + numpy.sin(rot+pi/2) * PLAYER_SPEED * timer  # For collision avoidance
        if map1[round(tempx - 0.5)][round(posy - 0.5)] == 0:
            posx = tempx
            if not pygame.mixer.Channel(10).get_busy():
                pygame.mixer.Channel(11).fadeout(250)
                pygame.mixer.Channel(10).play(pygame.mixer.Sound('sounds/walk.mp3'))
        if map1[round(posx - 0.5)][round(tempy - 0.5)] == 0:
            posy = tempy
            if not pygame.mixer.Channel(10).get_busy():
                pygame.mixer.Channel(11).fadeout(250)
                pygame.mixer.Channel(10).play(pygame.mixer.Sound('sounds/walk.mp3'))

    if keys[pygame.K_UP] or keys[ord('w')]:
        tempx = posx + numpy.cos(rot) * PLAYER_SPEED * 2 * timer  # For collision avoidance
        tempy = posy + numpy.sin(rot) * PLAYER_SPEED * 2 * timer  # For collision avoidance

        if map1[round(tempx-0.5)][round(posy-0.5)] == 0:  # For collision avoidance
            if keys[pygame.K_LSHIFT]:
                posx = posx + numpy.cos(rot) * PLAYER_SPEED * 2 * timer  # Increments player position (sprint)
                if not pygame.mixer.Channel(11).get_busy():
                    pygame.mixer.Channel(10).fadeout(250)
                    pygame.mixer.Channel(11).play(pygame.mixer.Sound('sounds/run.mp3'))
            else:
                posx = posx + numpy.cos(rot) * PLAYER_SPEED * timer  # Uses sin and cos for diagonal walking
                if not pygame.mixer.Channel(10).get_busy():
                    pygame.mixer.Channel(11).fadeout(250)
                    pygame.mixer.Channel(10).play(pygame.mixer.Sound('sounds/walk.mp3'))

        if map1[round(posx-0.5)][round(tempy-0.5)] == 0:  # For collision avoidance
            if keys[pygame.K_LSHIFT]:
                posy = posy + numpy.sin(rot) * PLAYER_SPEED * 2 * timer
                if not pygame.mixer.Channel(11).get_busy():
                    pygame.mixer.Channel(10).fadeout(250)
                    pygame.mixer.Channel(11).play(pygame.mixer.Sound('sounds/run.mp3'))
            else:
                posy = posy + numpy.sin(rot) * PLAYER_SPEED * timer
                if not pygame.mixer.Channel(10).get_busy():
                    pygame.mixer.Channel(11).fadeout(250)
                    pygame.mixer.Channel(10).play(pygame.mixer.Sound('sounds/walk.mp3'))

    elif keys[pygame.K_DOWN] or keys[ord('s')]:
        tempx = posx - numpy.cos(rot) * PLAYER_SPEED * timer  # For collision avoidance
        tempy = posy - numpy.sin(rot) * PLAYER_SPEED * timer  # For collision avoidance
        if map1[round(tempx - 0.5)][round(posy - 0.5)] == 0:
            posx = tempx
            if not pygame.mixer.Channel(10).get_busy():
                pygame.mixer.Channel(11).fadeout(250)
                pygame.mixer.Channel(10).play(pygame.mixer.Sound('sounds/walk.mp3'))
        if map1[round(posx-0.5)][round(tempy-0.5)] == 0:  # For collision avoidance
            posy = tempy
            if not pygame.mixer.Channel(10).get_busy():
                pygame.mixer.Channel(11).fadeout(250)
                pygame.mixer.Channel(10).play(pygame.mixer.Sound('sounds/walk.mp3'))
    
    else:
        pygame.mixer.Channel(10).fadeout(250)
        pygame.mixer.Channel(11).fadeout(250)

    return posx, posy, rot, gun_bob, vertical_angle  # Outputs the player's position and rotation
