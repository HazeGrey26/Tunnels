from maps import *
from mainProgram import *
from settings import *

BUY_AREA_SIZE = 1.5


def door_prompt(posx, posy, surface, prompt_text, keys, points, map1, areas_open, mag_ammo, total_ammo):
    for door in door_locations:
        if ((posx - BUY_AREA_SIZE) <= door[0] <= (posx + BUY_AREA_SIZE)) and ((posy - BUY_AREA_SIZE) <= door[1] <= (posy + BUY_AREA_SIZE - 0.25)) and (door[2] == True):
            surface.blit(prompt_text.render(f'Press F to Unlock Door | {areas_open**2 * 1250} Points', False, (255, 255, 255)), (SCREEN_RES[0] / 2 - 200, SCREEN_RES[1] / 2 + 100))
            if keys[ord('f')] and points >= areas_open**2 * 1250:
                points = points - areas_open**2 * 1250
                areas_open += 1
                door[2] = False
                pygame.mixer.Channel(13).play(pygame.mixer.Sound('sounds/purchase.mp3'))
                map1[door[1]][door[0]] = 0
                print(posx, posy)
    if 38 < posx < 39 and 11 < posy < 12:
        surface.blit(prompt_text.render(f'Press F to Buy .45 ACP Ammo | {AMMO_PISTOL_PRICE} Points', False, (255, 255, 255)),
                     (SCREEN_RES[0] / 2 - 200, SCREEN_RES[1] / 2 + 100))
        if keys[ord('f')] and points >= AMMO_PISTOL_PRICE:
            points = points - AMMO_PISTOL_PRICE
            pygame.mixer.Channel(13).play(pygame.mixer.Sound('sounds/purchase.mp3'))
            mag_ammo = 7
            total_ammo = PISTOL_MAX_AMMO
    if keys[ord('v')]:
        print(f"x: {posx} | y: {posy}")
    return points, map1, areas_open, mag_ammo, total_ammo