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
wallBrick = pygame.image.load('images/wallBrick.jpg').convert()
wallBrick.set_colorkey((0,0,0))
wallBrick = pygame.surfarray.array3d(wallBrick)

wallBars = pygame.image.load('images/bars.png').convert()
wallBars.set_colorkey((0,0,0))
wallBars = pygame.surfarray.array3d(wallBars)

wallBrickDamaged = pygame.surfarray.array3d(pygame.image.load('images/wallBrickDamaged.jpg'))
wallBrickDamaged1 = pygame.surfarray.array3d(pygame.image.load('images/wallBrickDamaged1.jpg'))
wallWood = pygame.surfarray.array3d(pygame.image.load('images/wallWood.jpg'))
wallPpsh = pygame.surfarray.array3d(pygame.image.load('images/wallPpsh.jpg'))
wallShotgun = pygame.surfarray.array3d(pygame.image.load('images/wallShotgun.jpg'))
wallDoor = pygame.surfarray.array3d(pygame.image.load('images/wallDoor.png'))
wallPistol = pygame.surfarray.array3d(pygame.image.load('images/wallPistol.png'))
wallGrafitti = pygame.surfarray.array3d(pygame.image.load('images/wallGrafitti.png'))

# Loads an image for the floor
floor = pygame.surfarray.array3d(pygame.image.load('images/floor.jpg'))
#Loads an image for the ceiling
ceiling = pygame.surfarray.array3d(pygame.image.load('images/ceiling.jpg'))

# Loads an image for the crosshair
crosshair = pygame.image.load('images/crosshair.png')
crosshairSize = 35
crosshair = pygame.transform.scale(crosshair, (crosshairSize, crosshairSize))

healthRing = pygame.image.load('images/healthRing.png')
healthRingTitle = pygame.image.load('images/healthRingTitle.png')
titleGradient = pygame.image.load('images/titleScreen.png')
titleBackground = pygame.image.load('images/titleBackground.png')
textBox = pygame.image.load('images/textBox.png')

# Loads a game icon
icon = pygame.image.load('images/healthRing.png')
pygame.display.set_icon(icon)