# This is the function that handles the pause screen
import pygame


def pause_screen(pause, title_background, title_gradient, title_image, text_box, ticker, screen, hud_text, SCREEN_RES, death):
    running = True
    pygame.event.get()
    mouse = pygame.mouse.get_pos()
    screen.fill((255, 0, 0))
    screen.blit(title_background, (0, 0), (200, 100, 1024, 768))
    screen.blit(title_gradient, (0, 0), (0, 0, 1024, 768))
    screen.blit(title_image, (0, 0), (40, 65, 1024, 768))
    screen.blit(text_box, (0, 0), (90, 0, 1024, 768))

    if death == 1:
        screen.blit(hud_text.render('PAUSED', False, (100, 10, 10)), (160, 10))
        if 50 < mouse[0] < 360 and 430 < mouse[1] < 500:
            ticker = True
            pygame.draw.polygon(screen, (100, 100, 100), (
            (50, 500), (35, 430), (360, 430), (360, 500)))  # Draws pause screen button lighter on mouse rollover
            if pygame.mouse.get_pressed()[0]:  # Detects if you click the button
                pause = 0
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/click.mp3'))
        else:
            pygame.draw.polygon(screen, (50, 50, 50),
                                ((50, 500), (35, 430), (360, 430), (360, 500)))  # Draws pause screen button
        screen.blit(hud_text.render('Resume', False, (10, 10, 10)), (80, 435))

        if 50 < mouse[0] < 360 and 430 + 100 < mouse[1] < 500 + 100:
            ticker = True
            pygame.draw.polygon(screen, (100, 100, 100), ((50, 500 + 100), (35, 430 + 100), (360, 430 + 100), (
            360, 500 + 100)))  # Draws pause screen button lighter on mouse rollover
            if pygame.mouse.get_pressed()[0]:  # Detects if you click the button
                running = False
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/click.mp3'))
                pause = 0
        else:
            pygame.draw.polygon(screen, (50, 50, 50), (
            (50, 500 + 100), (35, 430 + 100), (360, 430 + 100), (360, 500 + 100)))  # Draws pause screen button
        screen.blit(hud_text.render('Exit to Desktop', False, (10, 10, 10)), (80, 435 + 100))

        if not ticker:
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/tick.mp3'))
    elif death == 2:
        screen.blit(hud_text.render('YOU WON! GAME FINISHED', False, (100, 10, 10)), (100, 10))
        if 50 < mouse[0] < 360 and 430 + 100 < mouse[1] < 500 + 100:
            ticker = True
            pygame.draw.polygon(screen, (100, 100, 100), ((50, 500 + 100), (35, 430 + 100), (360, 430 + 100), (
                360, 500 + 100)))  # Draws pause screen button lighter on mouse rollover
            if pygame.mouse.get_pressed()[0]:  # Detects if you click the button
                running = False
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/click.mp3'))
                pause = 0
        else:
            pygame.draw.polygon(screen, (50, 50, 50), (
                (50, 500 + 100), (35, 430 + 100), (360, 430 + 100), (360, 500 + 100)))  # Draws pause screen button
        screen.blit(hud_text.render('Exit to Desktop', False, (10, 10, 10)), (80, 435 + 100))

        if not ticker:
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/tick.mp3'))
    else:
        screen.blit(hud_text.render('YOU DIED', False, (100, 10, 10)), (160, 10))
        if 50 < mouse[0] < 360 and 430 + 100 < mouse[1] < 500 + 100:
            ticker = True
            pygame.draw.polygon(screen, (100, 100, 100), ((50, 500 + 100), (35, 430 + 100), (360, 430 + 100), (
            360, 500 + 100)))  # Draws pause screen button lighter on mouse rollover
            if pygame.mouse.get_pressed()[0]:  # Detects if you click the button
                running = False
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/click.mp3'))
                pause = 0
        else:
            pygame.draw.polygon(screen, (50, 50, 50), (
            (50, 500 + 100), (35, 430 + 100), (360, 430 + 100), (360, 500 + 100)))  # Draws pause screen button
        screen.blit(hud_text.render('Exit to Desktop', False, (10, 10, 10)), (80, 435 + 100))

        if not ticker:
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/tick.mp3'))
    
    pygame.display.update()
    return running, pause
