from settings import *
from mainProgram import hud_text, point_text, prompt_text
from images import *


def hud(surface, gun_bob, crosshair, crosshair_size, keys, timer, mag_ammo, total_ammo, health_ring, posx, posy,
        points):
    # Draws crosshair
    surface.blit(crosshair, (0, 0), (
    gun_bob / 2 - SCREEN_RES[0] / 2 + crosshair_size / 2, -abs(gun_bob) / 4 - SCREEN_RES[1] / 2 + crosshair_size / 2,
    SCREEN_RES[0], SCREEN_RES[1]))

    # Draws ammo HUD in lower right part of the screen
    pygame.draw.polygon(surface, (10, 10, 10), (
    (SCREEN_RES[0] - 5, SCREEN_RES[1] - 105), (SCREEN_RES[0] - 5, SCREEN_RES[1] - 155),
    (SCREEN_RES[0] - 175, SCREEN_RES[1] - 155), (SCREEN_RES[0] - 155, SCREEN_RES[1] - 105)))  # Shadow
    pygame.draw.polygon(surface, (50, 50, 50), (
    (SCREEN_RES[0] - 10, SCREEN_RES[1] - 110), (SCREEN_RES[0] - 10, SCREEN_RES[1] - 160),
    (SCREEN_RES[0] - 180, SCREEN_RES[1] - 160), (SCREEN_RES[0] - 160, SCREEN_RES[1] - 110)))  # Draws the HUD rectangle
    surface.blit(hud_text.render(f'{mag_ammo} | {total_ammo}', False, (10, 10, 10)),
                 (SCREEN_RES[0] - 150, SCREEN_RES[1] - 160))  # Shadow
    surface.blit(hud_text.render(f'{mag_ammo} | {total_ammo}', False, (150, 25, 25)),
                 (SCREEN_RES[0] - 155, SCREEN_RES[1] - 165))  # Draws the mag_ammo text

    # Draws points HUD in lower right part of the screen
    pygame.draw.polygon(surface, (10, 10, 10), (
    (SCREEN_RES[0] - 5, SCREEN_RES[1] - 105 - 70), (SCREEN_RES[0] - 5, SCREEN_RES[1] - 155 - 50),
    (SCREEN_RES[0] - 125, SCREEN_RES[1] - 155 - 50), (SCREEN_RES[0] - 105, SCREEN_RES[1] - 105 - 70)))  # Shadow
    pygame.draw.polygon(surface, (50, 50, 50), (
    (SCREEN_RES[0] - 10, SCREEN_RES[1] - 105 - 75), (SCREEN_RES[0] - 10, SCREEN_RES[1] - 155 - 55),
    (SCREEN_RES[0] - 130, SCREEN_RES[1] - 155 - 55),
    (SCREEN_RES[0] - 110, SCREEN_RES[1] - 105 - 75)))  # Draws the HUD rectangle
    surface.blit(point_text.render(f'{points}', False, (10, 10, 10)), (SCREEN_RES[0] - 93, SCREEN_RES[1] - 208))
    surface.blit(point_text.render(f'{points}', False, (150, 25, 25)), (SCREEN_RES[0] - 95, SCREEN_RES[1] - 210))

    # Black bars at the top and bottom of the screen
    pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(0, 0, SCREEN_RES[0], 100))
    pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(0, SCREEN_RES[1] - 100, SCREEN_RES[0], 100))

    return points, total_ammo
