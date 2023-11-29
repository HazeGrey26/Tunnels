from maps import *
from mainProgram import *
from settings import *

BUY_AREA_SIZE = 1.5


def door_prompt(posx, posy, surface, prompt_text, keys, points, map1):
    for door in door_locations:
        if ((posx - BUY_AREA_SIZE) <= door[0] <= (posx + BUY_AREA_SIZE)) and ((posy - BUY_AREA_SIZE) <= door[1] <= (posy + BUY_AREA_SIZE - 0.25)) and (door[2] == True):
            surface.blit(prompt_text.render(f'Press F to Unlock Door | 100 Points', False, (255, 255, 255)), (SCREEN_RES[0] / 2 - 200, SCREEN_RES[1] / 2 + 100))
            if keys[ord('f')] and points >= 100:
                points = points - 100
                door[2] = False
                pygame.mixer.Channel(13).play(pygame.mixer.Sound('sounds/purchase.mp3'))
                map1[door[1]][door[0]] = 0
                print(posx, posy)
    if keys[ord('v')]:
        print(f"x: {posx} | y: {posy}")
    return points, map1