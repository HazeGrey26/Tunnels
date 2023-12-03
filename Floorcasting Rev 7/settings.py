import pygame

# Global variables
TARGET_FPS = 30
SCREEN_RES = (1024, 768)
PISTOL_SIZE = (1000, 550)
MOUSE_SENSITIVITY = 0.8
MAX_AMMO = 56
WALL_BASE_SCALE = 1.75
GUN_BOB_AMOUNT = 12
FIELD_OF_VIEW = 60  # Field of view in degrees
sens = 0.005  # Camera sensitivity
render_scale = 0.5  # Scales the render resolution of the game to improve performance
hres = int(SCREEN_RES[0]*render_scale)  # Horizontal resolution of the game render
halfvres = int(SCREEN_RES[1]*render_scale/2)  # Half of the vertical resolution of the game render
screen = pygame.display.set_mode((SCREEN_RES[0], SCREEN_RES[1]))  # Resolution of the game window
difficulty = 'Normal'

# Ray casting variables
WALL_RES = (200, 400)  # Dimensions of the wall texture in pixels
FLOOR_RES = (240, 240)  # Dimensions of the floor texture in pixels
FLOOR_SCALE = 1.5  # Sets the scale of your rendered floor texture

# Prices
AMMO_PISTOL_PRICE = 250

# Gun Stats
PISTOL_MAX_AMMO = 105
damage_value = 15

# Player Stats
STARTING_POSITION = (36.2, 13.2)
PLAYER_SPEED = 0.002

# Enemy Stats
number_of_enemies = 0
WEAK_ENEMY_HEALTH = 100

