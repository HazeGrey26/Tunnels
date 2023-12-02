from images import *
from mainProgram import *
DEFAULT_HEALTH = 100
RECOVERY_RATE = 0.1


def damage_function(player_damage, player_health, surface, screen):
    if player_damage == 0:
        if player_health < DEFAULT_HEALTH:
            player_health += RECOVERY_RATE
        return player_health
    else:
        player_health -= player_damage
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/hit.wav'))
        if player_health <= 0:
            death_screen(surface, screen)
    return player_health


def death_screen(surface, screen):
    death = 1
    hud_text = pygame.font.SysFont('agencyfb', 45)
    pygame.mouse.set_visible(True)  # Shows the mouse cursor
    pause = True
    ticker = False
    while pause:
        running, pause = pause_screen(pause, title_background, title_gradient, health_ring_title, text_box, ticker,
                                          screen, hud_text, SCREEN_RES, death)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    if running == False:
        pygame.quit()
