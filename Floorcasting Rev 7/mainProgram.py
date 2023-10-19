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
hudText = pygame.font.SysFont('agencyfb', 45)
pointText = pygame.font.SysFont('agencyfb', 25)
promptText = pygame.font.SysFont('couriernew', 18)

def main():
    frame = numpy.random.uniform(0, 0, (hres, halfvres * 2, 3)) # Where the game render will be stored before being sent to pygame
    
    # Variable to set the player's movements to be independent from the framerate
    clock = pygame.time.Clock()

    mod = hres / 60  # Scales to a 60 degrees field of view
    posx, posy, rot = 1.2, 1.2, 0  # Sets player's starting position to avoid collisions and rotation to zero
    
    # Audio files
    pygame.mixer.set_num_channels(99)
    pygame.mixer.music.load('sounds/background.mp3')
    pygame.mixer.music.play(-1)
    ticker = False
    channelNum = 0

    # Variables to define various gun actions
    gunBob = 0  # Movement animation for the gun
    gunBobDirection = 1  # Direction of the movement animation
    currentGun = 0  # Current image of the gun animation that is rendered
    shooting = 0  # Is the player trying to shoot?
    magAmmo = 7  # Amount of ammo in the magazine
    totalAmmo = 21  # Total ammo the player has outside of the magazine
    reloading = 0  # Is the player trying to reload?

    # Defines an idle animation for the gun
    idleAnimation = 0
    idleDir = 1
    
    points = 500
    
    # Starts title screen
    start = False
    surface = pygame.surfarray.make_surface(frame * 255)
    surface = pygame.transform.scale(surface, (screenResX, screenResY))
    
    pygame.display.set_caption("Aaron's Raycasting Demo")
    
    while start == False:
        pygame.event.get()  # Prevents the game from going non-responsive
        start, running = titleScreen(surface, healthRingTitle, pygame.key.get_pressed(), start, titleGradient, titleBackground, textBox, ticker)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
    
    pygame.mixer.music.stop()  # Stops title screen music
    pause = 0  # Variable to pause the game
    
    pygame.mixer.music.load('sounds/static.wav')
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)

    setUpdate = False
    frameUpdate = False
    while running:
        millisecondsStart = timer() * 1000
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if frameUpdate == True:
            newMod = newHres / 60  # Scales to a 60 degrees field of view
            frame = newFrame(frame, posx, posy, rot, newMod, newHres, map1, newHalfvres, wallResX, wallResY, wallBrick, wallWood,wallBars, wallPpsh, wallShotgun,
                             wallDoor, wallPistol, wallGrafitti, wallBrickDamaged, wallBrickDamaged1, floorScale, floorResX, floorResY, floor, ceiling)
        else:
            frame = newFrame(frame, posx, posy, rot, mod, hres, map1, halfvres, wallResX, wallResY, wallBrick, wallWood, wallBars, wallPpsh, wallShotgun,
                         wallDoor, wallPistol, wallGrafitti, wallBrickDamaged, wallBrickDamaged1, floorScale, floorResX, floorResY, floor, ceiling)

        # Converts the numpy frame into a surface displayable by pygame (with 256-bit color depth)
        surface = pygame.surfarray.make_surface(frame * 255)
        # Scales game up to the full resolution
        surface = pygame.transform.scale(surface, (screenResX, screenResY))

        # Starts pause screen
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            pause = 1
            while pause == 1:
                if setUpdate == True:
                    running, pause, newHres, newHalfvres, newSens, newScale = pauseScreen(
                        pause, titleBackground, titleGradient, healthRingTitle, textBox, ticker, screen, hudText, newScale, newSens, screenResX, screenResY)
                else:
                    running, pause, newHres, newHalfvres, newSens, newScale = pauseScreen(
                        pause, titleBackground, titleGradient, healthRingTitle, textBox, ticker, screen, hudText, render_scale, sens, screenResX, screenResY)
                setUpdate = True
                frameUpdate = True
            pause = 0

        # Displays the game HUD
        idleAnimation, idleDir, currentGun, shooting, magAmmo, totalAmmo, reloading, points, channelNum = hud(
            surface, gunBob, gunBobDirection, crosshair, crosshairSize, currentGun, idleAnimation, idleDir, pygame.key.get_pressed(),
            clock.tick(), shooting, magAmmo, totalAmmo, reloading, healthRing, posx, posy, points, channelNum)

        screen.blit(surface, (0, 0))  # Passes the surface to the frame buffer
        pygame.display.update()

        # Fetches the player position and rotation from the movement function
        if setUpdate == True:
            posx, posy, rot, gunBob = movement(posx, posy, rot, pygame.key.get_pressed(), clock.tick(), gunBob, map1, newSens)
        else:
            posx, posy, rot, gunBob = movement(posx, posy, rot, pygame.key.get_pressed(), clock.tick(), gunBob, map1, sens)
        
        # Displays frames per second
        fps = int(clock.get_fps()/2)
        pygame.display.set_caption("Aaron's Raycasting Demo    fps = " + str(fps))
        
        # Sets the frame timing for a capped fps
        fpsDelay = (1000/targetFps - (timer() * 1000 - millisecondsStart))/1000
        print(int(1000/(33.34-(fpsDelay*1000))))

        if fpsDelay > 0:
            time.sleep(fpsDelay)  # Caps the game fps

def titleScreen(surface, titleImage, keys, start, titleGradient, titleBackground, textBox, ticker):       
    start = False
    running = True

    screen.blit(titleBackground, (0, 0), (200, 100, screenResX, screenResY))
    screen.blit(titleGradient, (0, 0), (0, 0, screenResX, screenResY))
    screen.blit(titleImage, (0, 0), (40, 65, screenResX, screenResY))
    screen.blit(textBox, (0, 0), (90, 0, screenResX, screenResY))
    
    mouse = pygame.mouse.get_pos()
    
    if 50<mouse[0]<360 and 430<mouse[1]<500:
        ticker = True
        # Draws title screen button lighter on mouse rollover
        pygame.draw.polygon(screen, (100, 100, 100), ((50, 500), (35, 430), (360, 430), (360, 500)))
        buttonMouse = pygame.event.get()
        if pygame.mouse.get_pressed()[0]:  # Detects if you click the button
            start = True
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/click.mp3'))
    else:
        pygame.draw.polygon(screen, (50, 50, 50), ((50, 500), (35, 430), (360, 430), (360, 500)))  # Draws title screen button
    screen.blit(hudText.render('Enter the Tunnels', False, (10, 10, 10)), (80, 435))
    
    if 50<mouse[0]<360 and 430+100<mouse[1]<500+100:
        ticker = True
        # Draws title screen button lighter on mouse rollover
        pygame.draw.polygon(screen, (100, 100, 100), ((50, 500+100), (35, 430+100), (360, 430+100), (360, 500+100)))
    else:
        pygame.draw.polygon(screen, (50, 50, 50), ((50, 500+100), (35, 430+100), (360, 430+100), (360, 500+100))) # Draws title screen button
    screen.blit(hudText.render('Options', False, (10, 10, 10)), (80, 435+100))

    if 50<mouse[0]<360 and 430+200<mouse[1]<500+200:
        ticker = True
        # Draws title screen button lighter on mouse rollover
        pygame.draw.polygon(screen, (100, 100, 100), ((50, 500+200), (35, 430+200), (360, 430+200), (360, 500+200)))
        buttonMouse = pygame.event.get()
        if pygame.mouse.get_pressed()[0]:  # Detects if you click the button       
            running = False
            start = True
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('click.mp3'))
    else:
        pygame.draw.polygon(screen, (50, 50, 50), ((50, 500+200), (35, 430+200), (360, 430+200), (360, 500+200)))  # Draws title screen button
    screen.blit(hudText.render('Exit to Desktop', False, (10, 10, 10)), (80, 435+200)) 
    
    if ticker != True:
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/tick.mp3'))
    
    pygame.display.update()
    return start, running
    

def hud(surface, gunBob, gunBobDirection, crosshair, crosshairSize, currentGun, idleAnimation, idleDir,
        keys, timer, shooting, magAmmo, totalAmmo, reloading, healthRing, posx, posy, points, channelNum):
    # Applies an idle animation to the gun
    if gunBob == 0:
        if abs(idleAnimation) <= 14:
            if abs(idleAnimation) > 8:
                idleAnimation = idleAnimation + idleDir/4
            else:
                idleAnimation = idleAnimation + idleDir/2
        else:
            idleDir = -idleDir
            idleAnimation = idleAnimation + idleDir/3
    else:
        if idleAnimation > 0:
            idleAnimation = idleAnimation - 1
    
    currentGun, shooting, magAmmo, totalAmmo, reloading, channelNum = gunDraw(
        timer, currentGun, surface, gunBob, keys, idleAnimation, shooting, magAmmo, totalAmmo, reloading, channelNum)

    # Draws crosshair
    surface.blit(crosshair, (0, 0), (gunBob/2-screenResX/2 + crosshairSize/2, -abs(gunBob)/4-screenResY/2 + crosshairSize/2, screenResX, screenResY))

    # Draws ammo HUD in lower right part of the screen
    pygame.draw.polygon(surface, (10, 10, 10), ((screenResX-5, screenResY-105), (screenResX-5, screenResY-155),(screenResX-175, screenResY-155), (screenResX-155, screenResY-105)))  # Shadow
    pygame.draw.polygon(surface, (50, 50, 50), ((screenResX-10, screenResY-110), (screenResX-10, screenResY-160), (screenResX-180, screenResY-160), (screenResX-160, screenResY-110)))  # Draws the HUD rectangle
    surface.blit(hudText.render(f'{magAmmo} | {totalAmmo}', False, (10, 10, 10)), (screenResX-150, screenResY-160))  # Shadow
    surface.blit(hudText.render(f'{magAmmo} | {totalAmmo}', False, (150, 25, 25)), (screenResX-155, screenResY-165))  # Draws the magAmmo text
    
    # Draws points HUD in lower right part of the screen
    pygame.draw.polygon(surface, (10, 10, 10), ((screenResX-5, screenResY-105-70), (screenResX-5, screenResY-155-50), (screenResX-125, screenResY-155-50), (screenResX-105, screenResY-105-70)))  # Shadow
    pygame.draw.polygon(surface, (50, 50, 50), ((screenResX-10, screenResY-105-75), (screenResX-10, screenResY-155-55), (screenResX-130, screenResY-155-55), (screenResX-110, screenResY-105-75)))  # Draws the HUD rectangle    
    surface.blit(pointText.render(f'{points}', False, (10, 10, 10)), (screenResX-93, screenResY-208))
    surface.blit(pointText.render(f'{points}', False, (150, 25, 25)), (screenResX-95, screenResY-210))
    
    # Prompts the player to buy ammo at the (8,1) wall buy station
    if 8.5<posx<9 and 1.2<posy<1.8:
        surface.blit(promptText.render(f'Press F to Buy 1911 Ammo | 250 Points', False, (255, 255, 255)), (screenResX/2 - 200, screenResY/2 + 100))
        if keys[ord('f')] and points >= 250 and totalAmmo < 56:
            totalAmmo = 56
            points = points-250
            pygame.mixer.Channel(13).play(pygame.mixer.Sound('sounds/purchase.mp3'))
    
    # Draws health bar
    surface.blit(healthRing, (0, 0), (-screenResX+60, -screenResY+152, screenResX, screenResY))

    # Black bars at the top and bottom of the screen
    pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(0, 0, screenResX, 100))
    pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(0, screenResY-100, screenResX, 100))
    
    return idleAnimation, idleDir, currentGun, shooting, magAmmo, totalAmmo, reloading, points, channelNum

def gunDraw(timer, currentGun, surface, gunBob, keys, idleAnimation, shooting, magAmmo, totalAmmo, reloading, channelNum):
    # Plays the gunfire animation
    if keys[pygame.K_SPACE] and magAmmo > 0 and shooting == 0 and reloading == 0:
        shooting = 1
        if channelNum < 9:
            channelNum += 1
        else:
            channelNum = 0
        pygame.mixer.Channel(channelNum).play(pygame.mixer.Sound('sounds/pistol.mp3'))
        pygame.mixer.Channel(20+channelNum).play(pygame.mixer.Sound('sounds/brass.mp3'))
    
    elif keys[pygame.K_SPACE] and magAmmo == 0 and shooting == 0 and reloading == 0:
        if pygame.mixer.Channel(14).get_busy() == False:
            pygame.mixer.Channel(14).play(pygame.mixer.Sound('sounds/empty.mp3'))

    if shooting == 1:
        if currentGun < 4:
            currentGun = currentGun+1
        else:
            currentGun = 0
            shooting = 0
            magAmmo = magAmmo - 1
    
    # Steps through the reload animation        
    if reloading == 1:
        currentGun = currentGun + 1
    
    # Initiates the reloading process if the player wants to reload or the gun is out of ammo
    if magAmmo == 0 and reloading == 0 or keys[ord('r')] and reloading == 0:
        if magAmmo < 7 and totalAmmo > 0:
            reloading = 1
            currentGun = 5
            pygame.mixer.Channel(12).play(pygame.mixer.Sound('sounds/pistolReload.mp3'))

    # Draws the gun on the screen (0-4 is the shooting animation) (5-13 is the reload animation)
    if magAmmo == 0 and totalAmmo == 0 and shooting == 0:
        gun = pygame.transform.rotate(reloadEmpty, gunBob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gunBob-50, -abs(gunBob)/4-150 + idleAnimation/2, screenResX, screenResY))    

    # Pistol fire animation
    elif currentGun == 0:
        gun = pygame.transform.rotate(pistol, gunBob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gunBob-50, -abs(gunBob)/4-150 + idleAnimation/2, screenResX, screenResY))
    elif currentGun == 1:
        gun = pygame.transform.rotate(pistol1, gunBob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gunBob-50, -abs(gunBob)/4-150 + idleAnimation/2, screenResX, screenResY))
    elif currentGun == 2:
        gun = pygame.transform.rotate(pistol2, gunBob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gunBob-50, -abs(gunBob)/4-150 + idleAnimation/2, screenResX, screenResY))
    elif currentGun == 3:
        gun = pygame.transform.rotate(pistol3, gunBob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gunBob-50, -abs(gunBob)/4-150 + idleAnimation/2, screenResX, screenResY))
    elif currentGun == 4:
        gun = pygame.transform.rotate(pistol4, gunBob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gunBob-50, -abs(gunBob)/4-150 + idleAnimation/2, screenResX, screenResY))
    # Pistol reload animation
    elif currentGun == 5:
        gun = pygame.transform.rotate(reload13, gunBob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gunBob-50, -abs(gunBob)/4-150 + idleAnimation/2, screenResX, screenResY))
    elif currentGun == 6:
        gun = pygame.transform.rotate(reload12, gunBob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gunBob-50, -abs(gunBob)/4-150 + idleAnimation/2, screenResX, screenResY))
    elif currentGun == 7:
        gun = pygame.transform.rotate(reload12, gunBob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gunBob-50, -abs(gunBob)/4-150 + idleAnimation/2, screenResX, screenResY))
    elif currentGun == 8:
        gun = pygame.transform.rotate(reload11, gunBob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gunBob-50, -abs(gunBob)/4-150 + idleAnimation/2, screenResX, screenResY))
    elif currentGun == 9:
        gun = pygame.transform.rotate(reload11, gunBob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gunBob-50, -abs(gunBob)/4-150 + idleAnimation/2, screenResX, screenResY))
    elif currentGun == 10:
        gun = pygame.transform.rotate(reload10, gunBob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gunBob-50, -abs(gunBob)/4-150 + idleAnimation/2, screenResX, screenResY))
    elif currentGun == 11:
        gun = pygame.transform.rotate(reload10, gunBob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gunBob-50, -abs(gunBob)/4-150 + idleAnimation/2, screenResX, screenResY))
    elif currentGun == 12:
        gun = pygame.transform.rotate(reload9, gunBob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gunBob-50, -abs(gunBob)/4-150 + idleAnimation/2, screenResX, screenResY))
    elif currentGun == 13:
        gun = pygame.transform.rotate(reload9, gunBob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gunBob-50, -abs(gunBob)/4-150 + idleAnimation/2, screenResX, screenResY))
    elif currentGun == 14:
        gun = pygame.transform.rotate(reload8, gunBob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gunBob-50, -abs(gunBob)/4-150 + idleAnimation/2, screenResX, screenResY))
    elif currentGun == 15:
        gun = pygame.transform.rotate(reload8, gunBob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gunBob-50, -abs(gunBob)/4-150 + idleAnimation/2, screenResX, screenResY))
    elif currentGun == 16:
        gun = pygame.transform.rotate(reload7, gunBob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gunBob-50, -abs(gunBob)/4-150 + idleAnimation/2, screenResX, screenResY))
    elif currentGun == 17:
        gun = pygame.transform.rotate(reload7, gunBob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gunBob-50, -abs(gunBob)/4-150 + idleAnimation/2, screenResX, screenResY))
    elif currentGun == 18:
        gun = pygame.transform.rotate(reload6, gunBob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gunBob-50, -abs(gunBob)/4-150 + idleAnimation/2, screenResX, screenResY))
    elif currentGun == 19:
        gun = pygame.transform.rotate(reload6, gunBob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gunBob-50, -abs(gunBob)/4-150 + idleAnimation/2, screenResX, screenResY))
    elif currentGun == 20:
        gun = pygame.transform.rotate(reload5, gunBob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gunBob-50, -abs(gunBob)/4-150 + idleAnimation/2, screenResX, screenResY))
    elif currentGun == 21:
        gun = pygame.transform.rotate(reload5, gunBob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gunBob-50, -abs(gunBob)/4-150 + idleAnimation/2, screenResX, screenResY))
    elif currentGun == 22:
        gun = pygame.transform.rotate(reload4, gunBob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gunBob-50, -abs(gunBob)/4-150 + idleAnimation/2, screenResX, screenResY))
    elif currentGun == 23:
        gun = pygame.transform.rotate(reload4, gunBob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gunBob-50, -abs(gunBob)/4-150 + idleAnimation/2, screenResX, screenResY))
    elif currentGun == 24:
        gun = pygame.transform.rotate(reload3, gunBob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gunBob-50, -abs(gunBob)/4-150 + idleAnimation/2, screenResX, screenResY))
    elif currentGun == 25:
        gun = pygame.transform.rotate(reload3, gunBob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gunBob-50, -abs(gunBob)/4-150 + idleAnimation/2, screenResX, screenResY))
    elif currentGun == 26:
        gun = pygame.transform.rotate(reload2, gunBob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gunBob-50, -abs(gunBob)/4-150 + idleAnimation/2, screenResX, screenResY))
    elif currentGun == 27:
        gun = pygame.transform.rotate(reload2, gunBob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gunBob-50, -abs(gunBob)/4-150 + idleAnimation/2, screenResX, screenResY))
    elif currentGun == 28:
        gun = pygame.transform.rotate(reload1, gunBob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gunBob-50, -abs(gunBob)/4-150 + idleAnimation/2, screenResX, screenResY))
    elif currentGun == 29:
        gun = pygame.transform.rotate(reload1, gunBob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gunBob-50, -abs(gunBob)/4-150 + idleAnimation/2, screenResX, screenResY))      
        reloading = 0
        currentGun = 0
        
        # Replenishes the ammo in the magazine and subtracts from the player's total ammo
        if totalAmmo < 7:
            magAmmo = totalAmmo
            totalAmmo = 0
        else:    
            totalAmmo = totalAmmo + (magAmmo-7)
            magAmmo = 7
        
    return currentGun, shooting, magAmmo, totalAmmo, reloading, channelNum

if __name__ == "__main__":  # Runs main function
    main()
    pygame.quit()