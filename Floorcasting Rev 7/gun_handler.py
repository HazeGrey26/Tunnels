from settings import *
from images import *


def gun_draw(timer, current_gun, surface, gun_bob, keys, idle_anim, shooting, mag_ammo, total_ammo, reloading,
             channel_num, mouse_down, idle_dir):
    # Applies an idle animation to the gun
    if gun_bob == 0:
        if abs(idle_anim) <= 14:
            if abs(idle_anim) > 8:
                idle_anim = idle_anim + idle_dir / 4
            else:
                idle_anim = idle_anim + idle_dir / 2
        else:
            idle_dir = -idle_dir
            idle_anim = idle_anim + idle_dir / 3
    else:
        if idle_anim > 0:
            idle_anim = idle_anim - 1

    # Plays the gunfire animation
    if keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[
        0] and mag_ammo > 0 and shooting == 0 and reloading == 0 and mouse_down:
        print(mouse_down)
        shooting = 1
        if channel_num < 9:
            channel_num += 1
        else:
            channel_num = 0
        pygame.mixer.Channel(channel_num).play(pygame.mixer.Sound('sounds/pistol.mp3'))
        pygame.mixer.Channel(20 + channel_num).play(pygame.mixer.Sound('sounds/brass.mp3'))

    elif keys[pygame.K_SPACE] and mag_ammo == 0 and shooting == 0 and reloading == 0 and mouse_down:
        if not pygame.mixer.Channel(14).get_busy():
            pygame.mixer.Channel(14).play(pygame.mixer.Sound('sounds/empty.mp3'))

    if shooting == 1:
        if current_gun < 4:
            current_gun = current_gun + 1
        else:
            current_gun = 0
            shooting = 0
            mag_ammo = mag_ammo - 1

    # Steps through the reload animation
    if reloading == 1:
        current_gun = current_gun + 1

    # Initiates the reloading process if the player wants to reload or the gun is out of ammo
    if mag_ammo == 0 and reloading == 0 or keys[ord('r')] and reloading == 0:
        if mag_ammo < 7 and total_ammo > 0:
            reloading = 1
            current_gun = 5
            pygame.mixer.Channel(12).play(pygame.mixer.Sound('sounds/pistolReload.mp3'))

    # Draws the gun on the screen (0-4 is the shooting animation) (5-13 is the reload animation)
    if mag_ammo == 0 and total_ammo == 0 and shooting == 0:
        gun = pygame.transform.rotate(reloadEmpty, gun_bob / 16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob - 50, -abs(gun_bob) / 4 - 150 + idle_anim / 2, SCREEN_RES[0], SCREEN_RES[1]))

        # Pistol fire animation
    elif current_gun == 0:
        gun = pygame.transform.rotate(pistol, gun_bob / 16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob - 50, -abs(gun_bob) / 4 - 150 + idle_anim / 2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 1:
        gun = pygame.transform.rotate(pistol1, gun_bob / 16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob - 50, -abs(gun_bob) / 4 - 150 + idle_anim / 2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 2:
        gun = pygame.transform.rotate(pistol2, gun_bob / 16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob - 50, -abs(gun_bob) / 4 - 150 + idle_anim / 2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 3:
        gun = pygame.transform.rotate(pistol3, gun_bob / 16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob - 50, -abs(gun_bob) / 4 - 150 + idle_anim / 2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 4:
        gun = pygame.transform.rotate(pistol4, gun_bob / 16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob - 50, -abs(gun_bob) / 4 - 150 + idle_anim / 2, SCREEN_RES[0], SCREEN_RES[1]))
    # Pistol reload animation
    elif current_gun == 5:
        gun = pygame.transform.rotate(reload13, gun_bob / 16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob - 50, -abs(gun_bob) / 4 - 150 + idle_anim / 2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 6:
        gun = pygame.transform.rotate(reload12, gun_bob / 16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob - 50, -abs(gun_bob) / 4 - 150 + idle_anim / 2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 7:
        gun = pygame.transform.rotate(reload12, gun_bob / 16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob - 50, -abs(gun_bob) / 4 - 150 + idle_anim / 2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 8:
        gun = pygame.transform.rotate(reload11, gun_bob / 16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob - 50, -abs(gun_bob) / 4 - 150 + idle_anim / 2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 9:
        gun = pygame.transform.rotate(reload11, gun_bob / 16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob - 50, -abs(gun_bob) / 4 - 150 + idle_anim / 2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 10:
        gun = pygame.transform.rotate(reload10, gun_bob / 16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob - 50, -abs(gun_bob) / 4 - 150 + idle_anim / 2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 11:
        gun = pygame.transform.rotate(reload10, gun_bob / 16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob - 50, -abs(gun_bob) / 4 - 150 + idle_anim / 2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 12:
        gun = pygame.transform.rotate(reload9, gun_bob / 16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob - 50, -abs(gun_bob) / 4 - 150 + idle_anim / 2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 13:
        gun = pygame.transform.rotate(reload9, gun_bob / 16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob - 50, -abs(gun_bob) / 4 - 150 + idle_anim / 2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 14:
        gun = pygame.transform.rotate(reload8, gun_bob / 16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob - 50, -abs(gun_bob) / 4 - 150 + idle_anim / 2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 15:
        gun = pygame.transform.rotate(reload8, gun_bob / 16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob - 50, -abs(gun_bob) / 4 - 150 + idle_anim / 2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 16:
        gun = pygame.transform.rotate(reload7, gun_bob / 16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob - 50, -abs(gun_bob) / 4 - 150 + idle_anim / 2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 17:
        gun = pygame.transform.rotate(reload7, gun_bob / 16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob - 50, -abs(gun_bob) / 4 - 150 + idle_anim / 2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 18:
        gun = pygame.transform.rotate(reload6, gun_bob / 16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob - 50, -abs(gun_bob) / 4 - 150 + idle_anim / 2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 19:
        gun = pygame.transform.rotate(reload6, gun_bob / 16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob - 50, -abs(gun_bob) / 4 - 150 + idle_anim / 2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 20:
        gun = pygame.transform.rotate(reload5, gun_bob / 16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob - 50, -abs(gun_bob) / 4 - 150 + idle_anim / 2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 21:
        gun = pygame.transform.rotate(reload5, gun_bob / 16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob - 50, -abs(gun_bob) / 4 - 150 + idle_anim / 2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 22:
        gun = pygame.transform.rotate(reload4, gun_bob / 16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob - 50, -abs(gun_bob) / 4 - 150 + idle_anim / 2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 23:
        gun = pygame.transform.rotate(reload4, gun_bob / 16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob - 50, -abs(gun_bob) / 4 - 150 + idle_anim / 2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 24:
        gun = pygame.transform.rotate(reload3, gun_bob / 16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob - 50, -abs(gun_bob) / 4 - 150 + idle_anim / 2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 25:
        gun = pygame.transform.rotate(reload3, gun_bob / 16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob - 50, -abs(gun_bob) / 4 - 150 + idle_anim / 2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 26:
        gun = pygame.transform.rotate(reload2, gun_bob / 16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob - 50, -abs(gun_bob) / 4 - 150 + idle_anim / 2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 27:
        gun = pygame.transform.rotate(reload2, gun_bob / 16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob - 50, -abs(gun_bob) / 4 - 150 + idle_anim / 2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 28:
        gun = pygame.transform.rotate(reload1, gun_bob / 16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob - 50, -abs(gun_bob) / 4 - 150 + idle_anim / 2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 29:
        gun = pygame.transform.rotate(reload1, gun_bob / 16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob - 50, -abs(gun_bob) / 4 - 150 + idle_anim / 2, SCREEN_RES[0], SCREEN_RES[1]))
        reloading = 0
        current_gun = 0

        # Replenishes the ammo in the magazine and subtracts from the player's total ammo
        if total_ammo < 7:
            mag_ammo = total_ammo
            total_ammo = 0
        else:
            total_ammo = total_ammo + (mag_ammo - 7)
            mag_ammo = 7

    return current_gun, shooting, mag_ammo, total_ammo, reloading, channel_num, idle_anim, idle_dir
