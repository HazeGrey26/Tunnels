import pygame

# Global variables
TARGET_FPS = 30
SCREEN_RES = (1024, 768)
PISTOL_SIZE = (1000, 550)
sens = 0.005  # Camera sensitivity
render_scale = 0.5  # Scales the render resolution of the game to improve performance
hres = int(SCREEN_RES[0]*render_scale)  # Horizontal resolution of the game render
halfvres = int(SCREEN_RES[1]*render_scale/2)  # Half of the vertical resolution of the game render
screen = pygame.display.set_mode((SCREEN_RES[0], SCREEN_RES[1]))  # Resolution of the game window

WALL_RES = (200, 200)  # Dimensions of the wall texture in pixels
FLOOR_RES = (240, 240)  # Dimensions of the floor texture in pixels
FLOOR_SCALE = 1.5  # Sets the scale of your rendered floor texture
