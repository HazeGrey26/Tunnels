import numpy  # Helps with raycasting
from numba import njit  # Uses optimized math to increase performance

@njit()  # This is a decorator that denotes njit optimizations (from numba)
def newFrame(frame, posx, posy, rot, mod, hres, currentMap, halfvres, wallResX, wallResY, wallBrick, wallWood,
             wallBars, wallPpsh, wallShotgun, wallDoor, wallPistol, wallGrafitti, wallBrickDamaged, wallBrickDamaged1, floorScale, floorResX, floorResY, floor, ceiling):
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

        xx = int((x*1 % 1)*wallResX)
        
        if x % 1 < 0.01 or x % 1 > 0.99:  # If x is close to an integer value
            xx = int((y*1 % 1)*wallResY)
        yy = numpy.linspace(0, 198, h*2) % 199

        # Prevents shade from going above 1 and messing up the color
        shade = 0.1+ 0.8*(h/(halfvres*2))
        if shade > 1:
            shade = 1
       
        # Draws the walls
        for k in range(h*2):
            if currentMap[int(x)][int(y)] == 1:  # Checks if the maph contains a brick(1) or wall(2) texture
                if halfvres - h + k >= 0 and halfvres - h + k < 2*halfvres:
                    frame[i][halfvres - h + k] = shade*wallBrick[xx][int(yy[k])]/255
            if currentMap[int(x)][int(y)] == 2:  # Checks if the maph contains a brick(1) or wall(2) texture
                if halfvres - h + k >= 0 and halfvres - h + k < 2*halfvres:
                    frame[i][halfvres - h + k] = shade*wallWood[xx][int(yy[k])]/255
            if currentMap[int(x)][int(y)] == 3:
                if halfvres - h + k >= 0 and halfvres - h + k < 2*halfvres:
                    frame[i][halfvres - h + k] = shade*wallBars[xx][int(yy[k])]/255
            if currentMap[int(x)][int(y)] == 4:
                if halfvres - h + k >= 0 and halfvres - h + k < 2*halfvres:
                    frame[i][halfvres - h + k] = shade*wallPpsh[xx][int(yy[k])]/255
            if currentMap[int(x)][int(y)] == 5:
                if halfvres - h + k >= 0 and halfvres - h + k < 2*halfvres:
                    frame[i][halfvres - h + k] = shade*wallShotgun[xx][int(yy[k])]/255
            if currentMap[int(x)][int(y)] == 6:
                if halfvres - h + k >= 0 and halfvres - h + k < 2*halfvres:
                    frame[i][halfvres - h + k] = shade*wallDoor[xx][int(yy[k])]/255   
            if currentMap[int(x)][int(y)] == 7:
                if halfvres - h + k >= 0 and halfvres - h + k < 2*halfvres:
                    frame[i][halfvres - h + k] = shade*wallPistol[xx][int(yy[k])]/255
            if currentMap[int(x)][int(y)] == 8:
                if halfvres - h + k >= 0 and halfvres - h + k < 2*halfvres:
                    frame[i][halfvres - h + k] = shade*wallGrafitti[xx][int(yy[k])]/255
            if currentMap[int(x)][int(y)] == 9:
                if halfvres - h + k >= 0 and halfvres - h + k < 2*halfvres:
                    frame[i][halfvres - h + k] = shade*wallBrickDamaged[xx][int(yy[k])]/255     
            if currentMap[int(x)][int(y)] == 10:
                if halfvres - h + k >= 0 and halfvres - h + k < 2*halfvres:
                    frame[i][halfvres - h + k] = shade*wallBrickDamaged1[xx][int(yy[k])]/255            

        # Casts the floor and ceiling
        for j in range(halfvres - h):
            # cos2 corrects the 'fisheye' effect by curving the floor textures at the bottom corners of the screen
            n = (halfvres / (halfvres - j)) / cos2
            x, y = posx + cos*n, posy + sin*n

            # Variables that help draw the floor textures with distortion
            xx, yy = int((x*floorScale % 1)*floorResX), int((y*floorScale % 1)*floorResY)

            # Makes the floor farther from the player darker
            shade = 0.1 + 0.8*(1-j/halfvres)

            # Draws the floor textures
            frame[i][halfvres*2-j-1] = shade*floor[xx][yy]/255
            
            # Draws ceiling textures
            frame[i][-(halfvres*2-j-1)] = shade*ceiling[xx][yy]/255
            
    return frame