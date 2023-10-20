import pygame
import numpy


def movement(posx, posy, rot, keys, timer, gunBob, map1, sens):
    if keys[pygame.K_LEFT] or keys[ord('a')]:  # Detects if the 'a' or left arrow is pressed
        rot = rot - sens*timer  # Rotates the player
        if gunBob > 0:
            gunBob = gunBob-14        
        elif gunBob > -80:
            gunBob = gunBob-4
        elif gunBob > -120:
            gunBob = gunBob-3
    elif keys[pygame.K_RIGHT] or keys[ord('d')]:
        rot = rot + sens*timer  # Rotates the player
        if gunBob < 0:
            gunBob = gunBob+14        
        elif gunBob < 80:
            gunBob = gunBob+4
        elif gunBob < 120:
            gunBob = gunBob+3
    else:  # Returns the pistol to the center
        if gunBob <= 12:
            gunBob = gunBob+12
        if gunBob >= 12:
            gunBob = gunBob-12
        if gunBob <= 12 and gunBob >= -12:
            gunBob = 0

    if keys[pygame.K_UP] or keys[ord('w')]:
        tempx = posx + numpy.cos(rot) * 0.006*timer  # For collision avoidance
        tempy = posy + numpy.sin(rot) * 0.006*timer  # For collision avoidance
        
        if map1[round(tempx-0.5)][round(tempy-0.5)] == 0:  # For collision avoidance
            if keys[pygame.K_LSHIFT]:
                posx = posx + numpy.cos(rot) * 0.006*timer  # Increments player position (sprint)
                posy = posy + numpy.sin(rot) * 0.006*timer  # Uses sin and cos because the player may be moving in a diagonal direction
                if pygame.mixer.Channel(11).get_busy() == False:
                    pygame.mixer.Channel(10).fadeout(250)
                    pygame.mixer.Channel(11).play(pygame.mixer.Sound('sounds/run.mp3'))
            else:
                posx = posx + numpy.cos(rot) * 0.004*timer  # Increments player position (walk)
                posy = posy + numpy.sin(rot) * 0.004*timer  # Uses sin and cos because the player may be moving in a diagonal direction
                if pygame.mixer.Channel(10).get_busy() == False:
                    pygame.mixer.Channel(11).fadeout(250)
                    pygame.mixer.Channel(10).play(pygame.mixer.Sound('sounds/walk.mp3'))

    elif keys[pygame.K_DOWN] or keys[ord('s')]:
        tempx = posx - numpy.cos(rot) * 0.004*timer  # For collision avoidance
        tempy = posy - numpy.sin(rot) * 0.004*timer  # For collision avoidance
        
        if map1[round(tempx-0.5)][round(tempy-0.5)] == 0:
            posx = posx - numpy.cos(rot) * 0.004*timer  # Increments player position
            posy = posy - numpy.sin(rot) * 0.004*timer
            if pygame.mixer.Channel(10).get_busy() == False:
                pygame.mixer.Channel(11).fadeout(250)
                pygame.mixer.Channel(10).play(pygame.mixer.Sound('sounds/walk.mp3'))
    
    else:
        pygame.mixer.Channel(10).fadeout(250)
        pygame.mixer.Channel(11).fadeout(250)

    return posx, posy, rot, gunBob  # Outputs the player's position and rotation
