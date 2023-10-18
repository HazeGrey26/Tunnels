def hud(surface, screenResX, screenResY, pistol, ppsh, gunBob, gunBobDirection, hudText, crosshair, crosshairSize, currentGun, idleAnimation, idleDir, roundNumber):
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

    # Draws gun
    if currentGun == 0:
        gun = pygame.transform.rotate(pistol, gunBob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (0, 0), (gunBob-450, -abs(gunBob)/4-350 + idleAnimation/2, 1024, 768))

    if currentGun == 1:
        gun = pygame.transform.rotate(ppsh, gunBob/16)  # Rotates the pistol when the player turns
        surface.blit(gun, (30, 60), (gunBob-450, -abs(gunBob)/4-350 + idleAnimation/2, 1024, 768))

    # Draws round number
    surface.blit(roundNumber, (0, 0), (50, -520, 1024, 768))

    # Draws crosshair
    surface.blit(crosshair, (0, 0), (gunBob/2-screenResX/2 + crosshairSize/2, -abs(gunBob)/4-screenResY/2 + crosshairSize/2, 1024, 768))

    # Draws ammo HUD
    pygame.draw.polygon(surface, (10, 10, 10), ((screenResX-5, screenResY-105), (screenResX-5, screenResY-155), (screenResX-195, screenResY-155), (screenResX-175, screenResY-105)))  # Shadow
    pygame.draw.polygon(surface, (50, 50, 50), ((screenResX-10, screenResY-110), (screenResX-10, screenResY-160), (screenResX-200, screenResY-160), (screenResX-180, screenResY-110)))  # Draws the HUD rectangle

    surface.blit(hudText.render('7 / 21', False, (10, 10, 10)), (screenResX-160, screenResY-155))  # Shadow
    surface.blit(hudText.render('7 / 21', False, (150, 25, 25)), (screenResX-165, screenResY-160))  # Draws the ammo text

    # Black bars at the top and bottom of the screen
    pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(0, 0, screenResX, 100))
    pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(0, screenResY-100, screenResX, 100))

    return idleAnimation, idleDir