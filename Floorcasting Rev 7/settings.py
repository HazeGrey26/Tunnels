import pygame

# Global variables
targetFps = 30
screenResX = 1024
screenResY = 768
PISTOL_SIZE = (1000, 550)
sens = 0.005  # Camera sensitivity
renderScale = 0.5  # Scales the render resolution of the game to improve performance
hres = int(screenResX*renderScale)  # Horizontal resolution of the game render
halfvres = int(screenResY*renderScale/2)  # Half of the verical resolution of the game render
screen = pygame.display.set_mode((screenResX, screenResY)) # Resolution of the game window