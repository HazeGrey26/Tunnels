# This is the function that handles the pause screen
import pygame

def pauseScreen(pause, titleBackground, titleGradient, titleImage, textBox, ticker, screen, hudText, render_scale, sens, screenResX, screenResY):
    running = True

    pygame.event.get()
    mouse = pygame.mouse.get_pos()
    screen.fill((255,0,0))
    screen.blit(titleBackground, (0, 0), (200, 100, 1024, 768))
    screen.blit(titleGradient, (0, 0), (0, 0, 1024, 768))
    screen.blit(titleImage, (0, 0), (40, 65, 1024, 768))
    screen.blit(textBox, (0, 0), (90, 0, 1024, 768))
    
    screen.blit(hudText.render('PAUSED', False, (100, 10, 10)), (160, 10))
    
    if 50<mouse[0]<360 and 430<mouse[1]<500:
        ticker = True
        pygame.draw.polygon(screen, (100, 100, 100), ((50, 500), (35, 430), (360, 430), (360, 500)))  # Draws pause screen button lighter on mouse rollover
        button_mouse = pygame.event.get()
        if pygame.mouse.get_pressed()[0]:  # Detects if you click the button
            pause = 0
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/click.mp3'))
    else:
        pygame.draw.polygon(screen, (50, 50, 50), ((50, 500), (35, 430), (360, 430), (360, 500)))  # Draws pause screen button
    screen.blit(hudText.render('Resume', False, (10, 10, 10)), (80, 435))
    
    if 50<mouse[0]<360 and 430+100<mouse[1]<500+100:
        ticker = True
        pygame.draw.polygon(screen, (100, 100, 100), ((50, 500+100), (35, 430+100), (360, 430+100), (360, 500+100)))  # Draws pause screen button lighter on mouse rollover
        button_mouse = pygame.event.get()
        if pygame.mouse.get_pressed()[0]:  # Detects if you click the button
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/click.mp3'))
            #brightness = int(input("Enter a brightness value (0-100): "))
            sens = int(input("Enter a sensitivity value (0-100): "))/10000
            render_scale = (int(input("Enter a video scaler value (0-100): ")))/100
            print(f'Camera sensitivity = {sens}')
            print(f'Render scale = {render_scale}')
    else:
        pygame.draw.polygon(screen, (50, 50, 50), ((50, 500+100), (35, 430+100), (360, 430+100), (360, 500+100))) # Draws pause screen button
    screen.blit(hudText.render('Options', False, (10, 10, 10)), (80, 435+100))

    if 50<mouse[0]<360 and 430+200<mouse[1]<500+200:
        ticker = True
        pygame.draw.polygon(screen, (100, 100, 100), ((50, 500+200), (35, 430+200), (360, 430+200), (360, 500+200)))  # Draws pause screen button lighter on mouse rollover
        button_mouse = pygame.event.get()
        if pygame.mouse.get_pressed()[0]:  # Detects if you click the button       
            running = False
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/click.mp3'))
            pause = 0
    else:
        pygame.draw.polygon(screen, (50, 50, 50), ((50, 500+200), (35, 430+200), (360, 430+200), (360, 500+200)))  # Draws pause screen button
    screen.blit(hudText.render('Exit to Desktop', False, (10, 10, 10)), (80, 435+200))      
    
    if ticker != True:
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/tick.mp3'))

    newHres = int(screenResX * render_scale)  # Horizontal resolution of the game render
    newHalfvres = int(screenResY * render_scale / 2)  # Half of the verical resolution of the game render
    
    pygame.display.update()
    return running, pause, newHres, newHalfvres, sens, render_scale