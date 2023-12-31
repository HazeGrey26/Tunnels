from time import time as timer
import time
from math import pi

import pygame

# My imported functions:
from pause import pause_screen
from raycaster import new_frame
from walking import movement
from settings import *
from images import *
from maps import *
from gun_handler import *
from hud_handler import *
from sprite_classes import *
from health_handler import *
map1, door_locations = generate_map()
zone_map = generate_zones()
waypoint_list = generate_waypoints(zone_map)
from purchase_handler import door_prompt

pygame.init()
running = True

# Creates HUD text
hud_text = pygame.font.SysFont('agencyfb', 45)
point_text = pygame.font.SysFont('agencyfb', 25)
prompt_text = pygame.font.SysFont('couriernew', 18)

def main(map1, number_of_enemies):
    # Where the game render will be stored before being sent to pygame
    frame = numpy.random.uniform(0, 0, (hres, halfvres * 2, 3))
    
    # Variable to set the player's movements to be independent of the frame rate
    clock = pygame.time.Clock()

    mod = hres / FIELD_OF_VIEW  # Scales to a 60 degrees field of view
    pos_x, pos_y, rot = STARTING_POSITION[0], STARTING_POSITION[1], pi/2  # Sets player's starting position to avoid collisions and rotation to zero
    
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
    total_ammo = 21  # Total ammo the player has outside the magazine
    reloading = 0  # Is the player trying to reload?
    vertical_angle = 0  # The up and down angle of the player's camera
    player_health = DEFAULT_HEALTH
    click_reset = True
    mouse_down = False

    # Defines an idle animation for the gun
    idle_anim = 0
    idle_dir = 1

    points = 500
    
    # Starts title screen
    start = False
    surface = pygame.surfarray.make_surface(frame * 255)
    surface = pygame.transform.scale(surface, (SCREEN_RES[0], SCREEN_RES[1]))
    
    pygame.display.set_caption("Aaron's Ray Casting Demo")
    
    while not start:
        pygame.event.get()  # Prevents the game from going non-responsive
        start, running = title_screen(health_ring_title, title_gradient, title_background, text_box, ticker)
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

    pygame.mouse.set_visible(False)  # Hides the mouse

    areas_open = 1
    wave = 1
    number_killed = 0

    while running:
        milliseconds = timer() * 1000

        if number_killed > wave:
            wave += 1
            number_killed = 0
            print(f"Wave {wave}")

        # Spawns in enemies
        if number_of_enemies < wave:
            enemies.add(Enemy(areas_open, wave))
            number_of_enemies += 1

        # Returns the pistol to the center
        if gun_bob <= GUN_BOB_AMOUNT:
            gun_bob = gun_bob + GUN_BOB_AMOUNT
        if gun_bob >= GUN_BOB_AMOUNT:
            gun_bob = gun_bob - GUN_BOB_AMOUNT
        if -GUN_BOB_AMOUNT <= gun_bob <= GUN_BOB_AMOUNT:
            gun_bob = 0

        frame = new_frame(frame, pos_y, pos_x, rot, mod, hres, map1, halfvres, floor, ceiling, vertical_angle)

        # Converts the numpy frame into a surface displayable by pygame (with 256-bit color depth)
        surface = pygame.surfarray.make_surface(frame * 255)
        # Scales game up to the full resolution
        surface = pygame.transform.scale(surface, (SCREEN_RES[0], SCREEN_RES[1]))

        # Starts pause screen
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            pause = True
            death = 0
            pygame.mouse.set_visible(True)  # Shows the mouse cursor
            while pause:
                running, pause = pause_screen(pause, title_background, title_gradient, health_ring_title, text_box, ticker, screen, hud_text, SCREEN_RES, death)
            pygame.mouse.set_visible(False)  # Hides the mouse cursor

        # Fetches the player position and rotation from the movement function
        pos_y, pos_x, rot, gun_bob, vertical_angle = movement(pos_y, pos_x, rot, pygame.key.get_pressed(), clock.tick(), gun_bob, map1, vertical_angle)

        player_zone = locate_zone((pos_x, pos_y), zone_map)  # Fetches the player's zone

        # Ensures that close enemies are blitted last
        layer_list = []
        for sprite in enemies:
            distance = sprite.get_distance(pos_x, pos_y)
            layer_list.append((distance, sprite))
        try:
            layer_list.sort(reverse=True)
        except:
            # Sometimes .sort fails because two enemies have the exact same distance from the player
            print("Caught Exception")

        # Calculates damage taken by the player
        player_damage = 0
        for item in layer_list:
            sprite = item[1]
            sprite.draw_enemy(surface, hres, rot, pos_y, pos_x, halfvres)
            temp_damage = sprite.move_to_player(pos_x, pos_y, player_zone, zone_map)
            if temp_damage:
                player_damage += temp_damage
        temp_health = damage_function(player_damage, player_health, surface, screen)
        player_health = temp_health
        if player_health < DEFAULT_HEALTH:
            surface.blit(blood, (0, 0))

        # Draws the gun
        (current_gun, shooting, mag_ammo, total_ammo, reloading, channel_num, idle_anim, idle_dir, rot, points,
         number_killed, number_of_enemies) = gun_draw(clock.tick(), current_gun, surface, gun_bob,
                                                      pygame.key.get_pressed(), idle_anim, shooting, mag_ammo,
                                                      total_ammo, reloading, channel_num, mouse_down, idle_dir, rot,                                                  points, number_killed, number_of_enemies)
        # Are we at a location to buy an item?
        points, map1, areas_open, mag_ammo, total_ammo = door_prompt(pos_x, pos_y, surface, prompt_text, pygame.key.get_pressed(), points, map1, areas_open, mag_ammo, total_ammo)

        # Displays the game HUD
        points, total_ammo = hud(surface, gun_bob, crosshair, crosshair_size, pygame.key.get_pressed(),
            clock.tick(), mag_ammo, total_ammo, health_ring, pos_y, pos_x, points)

        # Alters the health indicator based on the player's current health value
        if player_health >= DEFAULT_HEALTH:
            # Draws health bar
            surface.blit(health_ring, (0, 0), (-SCREEN_RES[0] + 60, -SCREEN_RES[1] + 152, SCREEN_RES[0], SCREEN_RES[1]))
        elif player_health >= DEFAULT_HEALTH * 0.65:
            surface.blit(health_ring1, (0, 0), (-SCREEN_RES[0] + 60, -SCREEN_RES[1] + 152, SCREEN_RES[0], SCREEN_RES[1]))
        elif player_health >= DEFAULT_HEALTH * 0.45:
            surface.blit(health_ring2, (0, 0), (-SCREEN_RES[0] + 60, -SCREEN_RES[1] + 152, SCREEN_RES[0], SCREEN_RES[1]))
        else:
            surface.blit(health_ring3, (0, 0), (-SCREEN_RES[0] + 60, -SCREEN_RES[1] + 152, SCREEN_RES[0], SCREEN_RES[1]))
        
        # Sets the frame timing for a capped fps
        fps_delay = (1000/TARGET_FPS - (timer() * 1000 - milliseconds))/1000

        screen.blit(surface, (0, 0))  # Passes the surface to the frame buffer
        pygame.display.update()

        if fps_delay > 0:
            time.sleep(fps_delay)  # Caps the game fps

        # Displays frames per second
        fps = int(clock.get_fps()/2)
        pygame.display.set_caption("Aaron's Ray Casting Demo    Uncapped FPS = " + str(fps))


def title_screen(title_image, title_gradient, title_background, text_box, ticker):
    start = False
    running = True

    screen.blit(title_background, (0, 0), (200, 100, SCREEN_RES[0], SCREEN_RES[1]))
    screen.blit(title_gradient, (0, 0), (0, 0, SCREEN_RES[0], SCREEN_RES[1]))
    screen.blit(title_image, (0, 0), (40, 65, SCREEN_RES[0], SCREEN_RES[1]))
    screen.blit(text_box, (0, 0), (90, 0, SCREEN_RES[0], SCREEN_RES[1]))
    
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
        pygame.draw.polygon(screen, (50, 50, 50), ((50, 500+100), (35, 430+100), (360, 430+100), (360, 500+100)))  # Draws title screen button
    screen.blit(hud_text.render(f'Difficulty | {difficulty}', False, (10, 10, 10)), (80, 435+100))

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


if __name__ == "__main__":  # Runs main function
    main(map1, number_of_enemies)
    pygame.quit()
