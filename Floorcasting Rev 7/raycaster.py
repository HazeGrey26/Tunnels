import numpy  # Helps with raycasting
from numba import njit  # Uses optimized math to increase performance

@njit()  # This is a decorator that denotes njit optimizations (from numba)
def newFrame(frame, posx, posy, rot, mod, hres, currentMap, halfvres, WALL_RES, WALL_BRICK, WALL_WOOD, WALL_BARS, WALL_PPSH, WALL_SHOTGUN,
                             WALL_DOOR, WALL_PISTOL, WALL_GRAFFITI, WALL_BRICK_DAMAGE1, WALL_BRICK_DAMAGE2, floorScale, FLOOR_RES, floor, ceiling):
    for i in range(hres):
        # Casts rays horizontally from -30 degrees to 30 degrees
        rot_i = rot + numpy.deg2rad(i/mod - 30)
        # cos2 corrects the 'fisheye' effect
        sin, cos, cos2 = numpy.sin(rot_i), numpy.cos(rot_i), numpy.cos(numpy.deg2rad(i/mod - 30))
        x, y = posx, posy
        # Specifies locations to draw the walls
        while currentMap[int(x)][int(y)] == 0:
            x, y = x + 0.01*cos, y + 0.01*sin

        n = abs((x - posx)/cos)
        h = int(halfvres/(n*cos2 + 0.001))  # 0.001 guarantees there will be no division by zero

        xx = int((x*1 % 1)*WALL_RES[0])
        
        if x % 1 < 0.01 or x % 1 > 0.99:  # If x is close to an integer value
            xx = int((y*1 % 1)*WALL_RES[1])
        yy = numpy.linspace(0, 198, h*2) % 199

        # Prevents shade from going above 1 and messing up the color
        shade = 0.1 + 0.8*(h/(halfvres*2))
        if shade > 1:
            shade = 1
       
        # Draws the walls
        for k in range(h*2):
            if currentMap[int(x)][int(y)] == 1:  # Checks if the maph contains a brick(1) or wall(2) texture
                if halfvres - h + k >= 0 and halfvres - h + k < 2*halfvres:
                    frame[i][halfvres - h + k] = shade*WALL_BRICK[xx][int(yy[k])]/255
            if currentMap[int(x)][int(y)] == 2:  # Checks if the maph contains a brick(1) or wall(2) texture
                if halfvres - h + k >= 0 and halfvres - h + k < 2*halfvres:
                    frame[i][halfvres - h + k] = shade*WALL_WOOD[xx][int(yy[k])]/255
            if currentMap[int(x)][int(y)] == 3:
                if halfvres - h + k >= 0 and halfvres - h + k < 2*halfvres:
                    frame[i][halfvres - h + k] = shade*WALL_BARS[xx][int(yy[k])]/255
            if currentMap[int(x)][int(y)] == 4:
                if halfvres - h + k >= 0 and halfvres - h + k < 2*halfvres:
                    frame[i][halfvres - h + k] = shade*WALL_PPSH[xx][int(yy[k])]/255
            if currentMap[int(x)][int(y)] == 5:
                if halfvres - h + k >= 0 and halfvres - h + k < 2*halfvres:
                    frame[i][halfvres - h + k] = shade*WALL_SHOTGUN[xx][int(yy[k])]/255
            if currentMap[int(x)][int(y)] == 6:
                if halfvres - h + k >= 0 and halfvres - h + k < 2*halfvres:
                    frame[i][halfvres - h + k] = shade*WALL_DOOR[xx][int(yy[k])]/255
            if currentMap[int(x)][int(y)] == 7:
                if halfvres - h + k >= 0 and halfvres - h + k < 2*halfvres:
                    frame[i][halfvres - h + k] = shade*WALL_PISTOL[xx][int(yy[k])]/255
            if currentMap[int(x)][int(y)] == 8:
                if halfvres - h + k >= 0 and halfvres - h + k < 2*halfvres:
                    frame[i][halfvres - h + k] = shade*WALL_GRAFFITI[xx][int(yy[k])]/255
            if currentMap[int(x)][int(y)] == 9:
                if halfvres - h + k >= 0 and halfvres - h + k < 2*halfvres:
                    frame[i][halfvres - h + k] = shade*WALL_BRICK_DAMAGE1[xx][int(yy[k])]/255
            if currentMap[int(x)][int(y)] == 10:
                if halfvres - h + k >= 0 and halfvres - h + k < 2*halfvres:
                    frame[i][halfvres - h + k] = shade*WALL_BRICK_DAMAGE2[xx][int(yy[k])]/255

        # Casts the floor and ceiling
        for j in range(halfvres - h):
            # cos2 corrects the 'fisheye' effect by curving the floor textures at the bottom corners of the screen
            n = (halfvres / (halfvres - j)) / cos2
            x, y = posx + cos*n, posy + sin*n

            # Variables that help draw the floor textures with distortion
            xx, yy = int((x*floorScale % 1)*FLOOR_RES[0]), int((y*floorScale % 1)*FLOOR_RES[1])

            # Makes the floor farther from the player darker
            shade = 0.1 + 0.8*(1-j/halfvres)

            # Draws the floor textures
            frame[i][halfvres*2-j-1] = shade*floor[xx][yy]/255
            
            # Draws ceiling textures
            frame[i][-(halfvres*2-j-1)] = shade*ceiling[xx][yy]/255
            
    return frame
