import pygame
from settings import PISTOL_SIZE

# Gun animation images
# Pistol firing images
pistol = pygame.image.load('images/1.png')
pistol = pygame.transform.scale(pistol, PISTOL_SIZE)
pistol1 = pygame.image.load('images/2.png')
pistol1 = pygame.transform.scale(pistol1, PISTOL_SIZE)
pistol2 = pygame.image.load('images/3.png')
pistol2 = pygame.transform.scale(pistol2, PISTOL_SIZE)
pistol3 = pygame.image.load('images/4.png')
pistol3 = pygame.transform.scale(pistol3, PISTOL_SIZE)
pistol4 = pygame.image.load('images/5.png')
pistol4 = pygame.transform.scale(pistol4, PISTOL_SIZE)
# Reload animation images
reloadEmpty = pygame.image.load('images/reloadEmpty.png')
reloadEmpty = pygame.transform.scale(reloadEmpty, PISTOL_SIZE)
reload1 = pygame.image.load('images/reload1.png')
reload1 = pygame.transform.scale(reload1, PISTOL_SIZE)
reload2 = pygame.image.load('images/reload2.png')
reload2 = pygame.transform.scale(reload2, PISTOL_SIZE)
reload3 = pygame.image.load('images/reload3.png')
reload3 = pygame.transform.scale(reload3, PISTOL_SIZE)
reload4 = pygame.image.load('images/reload4.png')
reload4 = pygame.transform.scale(reload4, PISTOL_SIZE)
reload5 = pygame.image.load('images/reload5.png')
reload5 = pygame.transform.scale(reload5, PISTOL_SIZE)
reload6 = pygame.image.load('images/reload6.png')
reload6 = pygame.transform.scale(reload6, PISTOL_SIZE)
reload7 = pygame.image.load('images/reload7.png')
reload7 = pygame.transform.scale(reload7, PISTOL_SIZE)
reload8 = pygame.image.load('images/reload8.png')
reload8 = pygame.transform.scale(reload8, PISTOL_SIZE)
reload9 = pygame.image.load('images/reload9.png')
reload9 = pygame.transform.scale(reload9, PISTOL_SIZE)
reload10 = pygame.image.load('images/reload10.png')
reload10 = pygame.transform.scale(reload10, PISTOL_SIZE)
reload11 = pygame.image.load('images/reload11.png')
reload11 = pygame.transform.scale(reload11, PISTOL_SIZE)
reload12 = pygame.image.load('images/reload12.png')
reload12 = pygame.transform.scale(reload12, PISTOL_SIZE)
reload13 = pygame.image.load('images/reload13.png')
reload13 = pygame.transform.scale(reload13, PISTOL_SIZE)

# Wall textures (It would be great to use a dictionary here, but that is unsupported by numba.)
WALL_BRICK = pygame.image.load('images/wallBrick.jpg').convert()
WALL_BRICK.set_colorkey((0, 0, 0))
WALL_BRICK = pygame.surfarray.array3d(WALL_BRICK)

WALL_HOLE = pygame.image.load('images/wallHole.png').convert()
WALL_HOLE.set_colorkey((0, 0, 0))
WALL_HOLE = pygame.surfarray.array3d(WALL_HOLE)

WALL_GUN = pygame.image.load('images/wallGun.png').convert()
WALL_GUN.set_colorkey((0, 0, 0))
WALL_GUN = pygame.surfarray.array3d(WALL_GUN)

WALL_BARS = pygame.image.load('images/bars.png').convert()
WALL_BARS.set_colorkey((0, 0, 0))
WALL_BARS = pygame.surfarray.array3d(WALL_BARS)

WALL_ERROR = pygame.image.load('images/error.jpg').convert()
WALL_ERROR.set_colorkey((0, 0, 0))
WALL_ERROR = pygame.surfarray.array3d(WALL_ERROR)

WALL_BRICK_DAMAGE1 = pygame.surfarray.array3d(pygame.image.load('images/wallBrickDamaged.jpg'))
WALL_BRICK_DAMAGE2 = pygame.surfarray.array3d(pygame.image.load('images/wallBrickDamaged1.jpg'))
WALL_WOOD = pygame.surfarray.array3d(pygame.image.load('images/wallWood.jpg'))
WALL_PPSH = pygame.surfarray.array3d(pygame.image.load('images/wallPpsh.jpg'))
WALL_SHOTGUN = pygame.surfarray.array3d(pygame.image.load('images/wallShotgun.jpg'))
WALL_DOOR = pygame.surfarray.array3d(pygame.image.load('images/wallDoor.png'))
WALL_PISTOL = pygame.surfarray.array3d(pygame.image.load('images/wallPistol.png'))
WALL_GRAFFITI = pygame.surfarray.array3d(pygame.image.load('images/wallGrafitti.png'))

# Loads an image for the floor
floor = pygame.surfarray.array3d(pygame.image.load('images/floor.jpg'))
# Loads an image for the ceiling
ceiling = pygame.surfarray.array3d(pygame.image.load('images/ceiling.jpg'))

# Loads an image for the crosshair
crosshair = pygame.image.load('images/crosshair.png')
crosshair_size = 35
crosshair = pygame.transform.scale(crosshair, (crosshair_size, crosshair_size))

health_ring = pygame.image.load('images/healthRing.png')
health_ring_title = pygame.image.load('images/healthRingTitle.png')
title_gradient = pygame.image.load('images/titleScreen.png')
title_background = pygame.image.load('images/titleBackground.png')
text_box = pygame.image.load('images/textBox.png')
blood = pygame.image.load('images/blood.png')

# Loads a game icon
icon = pygame.image.load('images/healthRing.png')
pygame.display.set_icon(icon)
