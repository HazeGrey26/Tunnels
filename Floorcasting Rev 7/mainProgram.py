import pygame
import numpy  # Helps with raycasting
from numba import njit  # Uses optimized math to increase performance
from time import time as timer
import time

# My imported functions:
from pause import pauseScreen
from raycaster import newFrame
from walking import movement
from settings import *
from images import *
from maps import *

# TODO
# Fix gun reload animation  DONE
# Use .convert() and blit to improve performance for all images without transparency
# Fix bug where hand motion is slower when turning  DONE
# Add a posz and another map for multiple floors
# Add more rays near the edge of the screen to avoid stair-stepping at the edges
# Add a sprite system
# Add an options menu w/ brightness slider, camera sensitivity (DONE), and render scale (BUGGED)
# Make an enemy logic system
# Add gun sounds  DONE
# Add multiple weapons
# Add a door-buying system
# Add points for shooting enemies
# Shadows???
# Thin walls???

pygame.init()
running = True

# Creates HUD text
hud_text = pygame.font.SysFont('agencyfb', 45)
point_text = pygame.font.SysFont('agencyfb', 25)
prompt_text = pygame.font.SysFont('couriernew', 18)


def main():
    # Where the game render will be stored before being sent to pygame
    frame = numpy.random.uniform(0, 0, (hres, halfvres * 2, 3))
    
    # Variable to set the player's movements to be independent from the framerate
    clock = pygame.time.Clock()

    mod = hres / 60  # Scales to a 60 degrees field of view
    posx, posy, rot = 1.2, 1.2, 0  # Sets player's starting position to avoid collisions and rotation to zero
    
    # Audio files
    pygame.mixer.set_num_channels(99)
    pygame.mixer.music.load('sounds/background.mp3')
    pygame.mixer.music.play(-1)
    ticker = False
    channel_num = 0

    # Variables to define various gun actions
    gun_bob = 0  # Movement animation for the gun
    current_gun = 0  # Current image of the gun animation that is rendered
    shooting = 0  # Is the player trying to shoot?
    mag_ammo = 7  # Amount of ammo in the magazine
    total_ammo = 21  # Total ammo the player has outside of the magazine
    reloading = 0  # Is the player trying to reload?

    # Defines an idle animation for the gun
    idle_anim = 0
    idle_dir = 1

    points = 500
    
    # Starts title screen
    start = False
    surface = pygame.surfarray.make_surface(frame * 255)
    surface = pygame.transform.scale(surface, (SCREEN_RES[0], SCREEN_RES[1]))
    
    pygame.display.set_caption("Aaron's Raycasting Demo")
    
    while not start:
        pygame.event.get()  # Prevents the game from going non-responsive
        start, running = title_screen(surface, health_ring_title, pygame.key.get_pressed(), start, title_gradient,
                                      title_background, text_box, ticker)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
    
    pygame.mixer.music.stop()  # Stops title screen music
    
    pygame.mixer.music.load('sounds/static.wav')
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)

    set_update = False
    frame_update = False
    while running:
        millisecondsStart = timer() * 1000
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if frame_update:
            new_mod = new_hres / 60  # Scales to a 60 degrees field of view
            frame = newFrame(frame, posx, posy, rot, new_mod, new_hres, map1, new_halfvres, WALL_RES, WALL_BRICK, WALL_WOOD, WALL_BARS, WALL_PPSH, WALL_SHOTGUN,
                             WALL_DOOR, WALL_PISTOL, WALL_GRAFFITI, WALL_BRICK_DAMAGE1, WALL_BRICK_DAMAGE2, floorScale, FLOOR_RES, floor, ceiling)
        else:
            frame = newFrame(frame, posx, posy, rot, mod, hres, map1, halfvres, WALL_RES, WALL_BRICK, WALL_WOOD, WALL_BARS, WALL_PPSH, WALL_SHOTGUN,
                             WALL_DOOR, WALL_PISTOL, WALL_GRAFFITI, WALL_BRICK_DAMAGE1, WALL_BRICK_DAMAGE2, floorScale, FLOOR_RES, floor, ceiling)

        # Converts the numpy frame into a surface displayable by pygame (with 256-bit color depth)
        surface = pygame.surfarray.make_surface(frame * 255)
        # Scales game up to the full resolution
        surface = pygame.transform.scale(surface, (SCREEN_RES[0], SCREEN_RES[1]))

        # Starts pause screen
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            pause = True
            while pause:
                if set_update:
                    running, pause, new_hres, new_halfvres, new_sens, new_scale = pauseScreen(
                        pause, title_background, title_gradient, health_ring_title, text_box, ticker, screen, hud_text, new_scale, new_sens, SCREEN_RES)
                else:
                    running, pause, new_hres, new_halfvres, new_sens, new_scale = pauseScreen(
                        pause, title_background, title_gradient, health_ring_title, text_box, ticker, screen, hud_text, render_scale, sens, SCREEN_RES)
                set_update = True
                frame_update = True

        # Displays the game HUD
        idle_anim, idle_dir, current_gun, shooting, mag_ammo, total_ammo, reloading, points, channel_num = hud(
            surface, gun_bob, crosshair, crosshair_size, current_gun, idle_anim, idle_dir, pygame.key.get_pressed(),
            clock.tick(), shooting, mag_ammo, total_ammo, reloading, health_ring, posx, posy, points, channel_num)

        screen.blit(surface, (0, 0))  # Passes the surface to the frame buffer
        pygame.display.update()

        # Fetches the player position and rotation from the movement function
        if set_update:
            posx, posy, rot, gun_bob = movement(posx, posy, rot, pygame.key.get_pressed(), clock.tick(), gun_bob, map1, new_sens)
        else:
            posx, posy, rot, gun_bob = movement(posx, posy, rot, pygame.key.get_pressed(), clock.tick(), gun_bob, map1, sens)
        
        # Displays frames per second
        fps = int(clock.get_fps()/2)
        pygame.display.set_caption("Aaron's Raycasting Demo    fps = " + str(fps))
        
        # Sets the frame timing for a capped fps
        fps_delay = (1000/TARGET_FPS - (timer() * 1000 - millisecondsStart))/1000
        print(int(1000/(33.34-(fps_delay*1000))))

        if fps_delay > 0:
            time.sleep(fps_delay)  # Caps the game fps


def title_screen(surface, titleImage, keys, start, titleGradient, title_background, textBox, ticker):       
    start = False
    running = True

    screen.blit(title_background, (0, 0), (200, 100, SCREEN_RES[0], SCREEN_RES[1]))
    screen.blit(titleGradient, (0, 0), (0, 0, SCREEN_RES[0], SCREEN_RES[1]))
    screen.blit(titleImage, (0, 0), (40, 65, SCREEN_RES[0], SCREEN_RES[1]))
    screen.blit(textBox, (0, 0), (90, 0, SCREEN_RES[0], SCREEN_RES[1]))
    
    mouse = pygame.mouse.get_pos()
    
    if 50 < mouse[0] < 360 and 430 < mouse[1] < 500:
        ticker = True
        # Draws title screen button lighter on mouse rollover
        pygame.draw.polygon(screen, (100, 100, 100), ((50, 500), (35, 430), (360, 430), (360, 500)))
        if pygame.mouse.get_pressed()[0]:  # Detects if you click the button
            start = True
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/click.mp3'))
    else:
        pygame.draw.polygon(screen, (50, 50, 50), ((50, 500), (35, 430), (360, 430), (360, 500)))  # Draws title screen button
    screen.blit(hud_text.render('Enter the Tunnels', False, (10, 10, 10)), (80, 435))
    
    if 50 < mouse[0] < 360 and 430+100 < mouse[1] < 500+100:
        ticker = True
        # Draws title screen button lighter on mouse rollover
        pygame.draw.polygon(screen, (100, 100, 100), ((50, 500+100), (35, 430+100), (360, 430+100), (360, 500+100)))
    else:
        pygame.draw.polygon(screen, (50, 50, 50), ((50, 500+100), (35, 430+100), (360, 430+100), (360, 500+100))) # Draws title screen button
    screen.blit(hud_text.render('Options', False, (10, 10, 10)), (80, 435+100))

    if 50 < mouse[0] < 360 and 430+200 < mouse[1] < 500+200:
        ticker = True
        # Draws title screen button lighter on mouse rollover
        pygame.draw.polygon(screen, (100, 100, 100), ((50, 500+200), (35, 430+200), (360, 430+200), (360, 500+200)))
        if pygame.mouse.get_pressed()[0]:  # Detects if you click the button       
            running = False
            start = True
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('click.mp3'))
    else:
        pygame.draw.polygon(screen, (50, 50, 50), ((50, 500+200), (35, 430+200), (360, 430+200), (360, 500+200)))  # Draws title screen button
    screen.blit(hud_text.render('Exit to Desktop', False, (10, 10, 10)), (80, 435+200)) 
    
    if not ticker:
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/tick.mp3'))
    
    pygame.display.update()
    return start, running
    

def hud(surface, gun_bob, crosshair, crosshairSize, current_gun, idle_anim, idle_dir,
        keys, timer, shooting, mag_ammo, total_ammo, reloading, healthRing, posx, posy, points, channel_num):
    # Applies an idle animation to the gun
    if gun_bob == 0:
        if abs(idle_anim) <= 14:
            if abs(idle_anim) > 8:
                idle_anim = idle_anim + idle_dir/4
            else:
                idle_anim = idle_anim + idle_dir/2
        else:
            idle_dir = -idle_dir
            idle_anim = idle_anim + idle_dir/3
    else:
        if idle_anim > 0:
            idle_anim = idle_anim - 1
    
    current_gun, shooting, mag_ammo, total_ammo, reloading, channel_num = gun_draw(
        timer, current_gun, surface, gun_bob, keys, idle_anim, shooting, mag_ammo, total_ammo, reloading, channel_num)

    # Draws crosshair
    surface.blit(crosshair, (0, 0), (gun_bob/2-SCREEN_RES[0]/2 + crosshairSize/2, -abs(gun_bob)/4-SCREEN_RES[1]/2 + crosshairSize/2, SCREEN_RES[0], SCREEN_RES[1]))

    # Draws ammo HUD in lower right part of the screen
    pygame.draw.polygon(surface, (10, 10, 10), ((SCREEN_RES[0]-5, SCREEN_RES[1]-105), (SCREEN_RES[0]-5, SCREEN_RES[1]-155),(SCREEN_RES[0]-175, SCREEN_RES[1]-155), (SCREEN_RES[0]-155, SCREEN_RES[1]-105)))  # Shadow
    pygame.draw.polygon(surface, (50, 50, 50), ((SCREEN_RES[0]-10, SCREEN_RES[1]-110), (SCREEN_RES[0]-10, SCREEN_RES[1]-160), (SCREEN_RES[0]-180, SCREEN_RES[1]-160), (SCREEN_RES[0]-160, SCREEN_RES[1]-110)))  # Draws the HUD rectangle
    surface.blit(hud_text.render(f'{mag_ammo} | {total_ammo}', False, (10, 10, 10)), (SCREEN_RES[0]-150, SCREEN_RES[1]-160))  # Shadow
    surface.blit(hud_text.render(f'{mag_ammo} | {total_ammo}', False, (150, 25, 25)), (SCREEN_RES[0]-155, SCREEN_RES[1]-165))  # Draws the mag_ammo text
    
    # Draws points HUD in lower right part of the screen
    pygame.draw.polygon(surface, (10, 10, 10), ((SCREEN_RES[0]-5, SCREEN_RES[1]-105-70), (SCREEN_RES[0]-5, SCREEN_RES[1]-155-50), (SCREEN_RES[0]-125, SCREEN_RES[1]-155-50), (SCREEN_RES[0]-105, SCREEN_RES[1]-105-70)))  # Shadow
    pygame.draw.polygon(surface, (50, 50, 50), ((SCREEN_RES[0]-10, SCREEN_RES[1]-105-75), (SCREEN_RES[0]-10, SCREEN_RES[1]-155-55), (SCREEN_RES[0]-130, SCREEN_RES[1]-155-55), (SCREEN_RES[0]-110, SCREEN_RES[1]-105-75)))  # Draws the HUD rectangle    
    surface.blit(point_text.render(f'{points}', False, (10, 10, 10)), (SCREEN_RES[0]-93, SCREEN_RES[1]-208))
    surface.blit(point_text.render(f'{points}', False, (150, 25, 25)), (SCREEN_RES[0]-95, SCREEN_RES[1]-210))
    
    # Prompts the player to buy ammo at the (8,1) wall buy station
    if 8.5 < posx < 9 and 1.2 < posy < 1.8:
        surface.blit(prompt_text.render(f'Press F to Buy 1911 Ammo | 250 Points', False, (255, 255, 255)), (SCREEN_RES[0]/2 - 200, SCREEN_RES[1]/2 + 100))
        if keys[ord('f')] and points >= 250 and total_ammo < 56:
            total_ammo = 56
            points = points-250
            pygame.mixer.Channel(13).play(pygame.mixer.Sound('sounds/purchase.mp3'))
    
    # Draws health bar
    surface.blit(healthRing, (0, 0), (-SCREEN_RES[0]+60, -SCREEN_RES[1]+152, SCREEN_RES[0], SCREEN_RES[1]))

    # Black bars at the top and bottom of the screen
    pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(0, 0, SCREEN_RES[0], 100))
    pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(0, SCREEN_RES[1]-100, SCREEN_RES[0], 100))
    
    return idle_anim, idle_dir, current_gun, shooting, mag_ammo, total_ammo, reloading, points, channel_num


def gun_draw(timer, current_gun, surface, gun_bob, keys, idle_anim, shooting, mag_ammo, total_ammo, reloading, channel_num):
    # Plays the gunfire animation
    if keys[pygame.K_SPACE] and mag_ammo > 0 and shooting == 0 and reloading == 0:
        shooting = 1
        if channel_num < 9:
            channel_num += 1
        else:
            channel_num = 0
        pygame.mixer.Channel(channel_num).play(pygame.mixer.Sound('sounds/pistol.mp3'))
        pygame.mixer.Channel(20+channel_num).play(pygame.mixer.Sound('sounds/brass.mp3'))
    
    elif keys[pygame.K_SPACE] and mag_ammo == 0 and shooting == 0 and reloading == 0:
        if not pygame.mixer.Channel(14).get_busy():
            pygame.mixer.Channel(14).play(pygame.mixer.Sound('sounds/empty.mp3'))

    if shooting == 1:
        if current_gun < 4:
            current_gun = current_gun+1
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
        gun = pygame.transform.rotate(reloadEmpty, gun_bob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob-50, -abs(gun_bob)/4-150 + idle_anim/2, SCREEN_RES[0], SCREEN_RES[1]))    

    # Pistol fire animation
    elif current_gun == 0:
        gun = pygame.transform.rotate(pistol, gun_bob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob-50, -abs(gun_bob)/4-150 + idle_anim/2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 1:
        gun = pygame.transform.rotate(pistol1, gun_bob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob-50, -abs(gun_bob)/4-150 + idle_anim/2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 2:
        gun = pygame.transform.rotate(pistol2, gun_bob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob-50, -abs(gun_bob)/4-150 + idle_anim/2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 3:
        gun = pygame.transform.rotate(pistol3, gun_bob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob-50, -abs(gun_bob)/4-150 + idle_anim/2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 4:
        gun = pygame.transform.rotate(pistol4, gun_bob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob-50, -abs(gun_bob)/4-150 + idle_anim/2, SCREEN_RES[0], SCREEN_RES[1]))
    # Pistol reload animation
    elif current_gun == 5:
        gun = pygame.transform.rotate(reload13, gun_bob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob-50, -abs(gun_bob)/4-150 + idle_anim/2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 6:
        gun = pygame.transform.rotate(reload12, gun_bob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob-50, -abs(gun_bob)/4-150 + idle_anim/2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 7:
        gun = pygame.transform.rotate(reload12, gun_bob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob-50, -abs(gun_bob)/4-150 + idle_anim/2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 8:
        gun = pygame.transform.rotate(reload11, gun_bob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob-50, -abs(gun_bob)/4-150 + idle_anim/2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 9:
        gun = pygame.transform.rotate(reload11, gun_bob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob-50, -abs(gun_bob)/4-150 + idle_anim/2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 10:
        gun = pygame.transform.rotate(reload10, gun_bob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob-50, -abs(gun_bob)/4-150 + idle_anim/2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 11:
        gun = pygame.transform.rotate(reload10, gun_bob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob-50, -abs(gun_bob)/4-150 + idle_anim/2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 12:
        gun = pygame.transform.rotate(reload9, gun_bob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob-50, -abs(gun_bob)/4-150 + idle_anim/2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 13:
        gun = pygame.transform.rotate(reload9, gun_bob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob-50, -abs(gun_bob)/4-150 + idle_anim/2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 14:
        gun = pygame.transform.rotate(reload8, gun_bob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob-50, -abs(gun_bob)/4-150 + idle_anim/2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 15:
        gun = pygame.transform.rotate(reload8, gun_bob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob-50, -abs(gun_bob)/4-150 + idle_anim/2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 16:
        gun = pygame.transform.rotate(reload7, gun_bob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob-50, -abs(gun_bob)/4-150 + idle_anim/2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 17:
        gun = pygame.transform.rotate(reload7, gun_bob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob-50, -abs(gun_bob)/4-150 + idle_anim/2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 18:
        gun = pygame.transform.rotate(reload6, gun_bob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob-50, -abs(gun_bob)/4-150 + idle_anim/2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 19:
        gun = pygame.transform.rotate(reload6, gun_bob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob-50, -abs(gun_bob)/4-150 + idle_anim/2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 20:
        gun = pygame.transform.rotate(reload5, gun_bob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob-50, -abs(gun_bob)/4-150 + idle_anim/2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 21:
        gun = pygame.transform.rotate(reload5, gun_bob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob-50, -abs(gun_bob)/4-150 + idle_anim/2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 22:
        gun = pygame.transform.rotate(reload4, gun_bob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob-50, -abs(gun_bob)/4-150 + idle_anim/2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 23:
        gun = pygame.transform.rotate(reload4, gun_bob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob-50, -abs(gun_bob)/4-150 + idle_anim/2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 24:
        gun = pygame.transform.rotate(reload3, gun_bob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob-50, -abs(gun_bob)/4-150 + idle_anim/2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 25:
        gun = pygame.transform.rotate(reload3, gun_bob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob-50, -abs(gun_bob)/4-150 + idle_anim/2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 26:
        gun = pygame.transform.rotate(reload2, gun_bob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob-50, -abs(gun_bob)/4-150 + idle_anim/2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 27:
        gun = pygame.transform.rotate(reload2, gun_bob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob-50, -abs(gun_bob)/4-150 + idle_anim/2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 28:
        gun = pygame.transform.rotate(reload1, gun_bob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob-50, -abs(gun_bob)/4-150 + idle_anim/2, SCREEN_RES[0], SCREEN_RES[1]))
    elif current_gun == 29:
        gun = pygame.transform.rotate(reload1, gun_bob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gun_bob-50, -abs(gun_bob)/4-150 + idle_anim/2, SCREEN_RES[0], SCREEN_RES[1]))      
        reloading = 0
        current_gun = 0
        
        # Replenishes the ammo in the magazine and subtracts from the player's total ammo
        if total_ammo < 7:
            mag_ammo = total_ammo
            total_ammo = 0
        else:    
            total_ammo = total_ammo + (mag_ammo-7)
            mag_ammo = 7
        
    return current_gun, shooting, mag_ammo, total_ammo, reloading, channel_num


if __name__ == "__main__":  # Runs main function
    main()
    pygame.quit()
