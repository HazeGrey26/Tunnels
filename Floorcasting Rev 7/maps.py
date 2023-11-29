import numpy
from PIL import Image
from math import floor
from settings import WALL_BASE_SCALE

# Generates the game map
# The map is flipped across the y-axis. It is a mirror image of the intended map...

def generate_map():
    # Color of wall = 0
    # Color of blank space = 0
    # Color of door = 15
    im = Image.open('map_info/map.bmp')  # This is a 16-color bmp. Pixel vales go from 0 to 15.
    pix = im.load()
    image_size = im.size  # Get the width and height of the image
    map = []
    for y in range(image_size[1]):
        row_of_pixels = []
        for x in range(image_size[0]):
            if pix[x, y] == 0:
                row_of_pixels.append(1)
            if pix[x, y] == 15:
                row_of_pixels.append(3)
            if pix[x, y] == 9:
                row_of_pixels.append(0)
            if pix[x, y] == 12:
                row_of_pixels.append(2)
        map.append(row_of_pixels)

    map1 = numpy.array((
    map[0], map[1], map[2], map[3], map[4], map[5], map[6], map[7], map[8], map[9], map[10], map[11],
    map[12], map[13], map[14], map[15], map[16], map[17], map[18], map[19], map[20], map[21], map[22],
    map[23], map[24], map[25], map[26], map[27]))

    # [x_pox, y_pos]
    door_locations = []

    row_num = 0
    for row in map1:
        col_num = 0
        for column in row:
            if column == 3:
                door_data = [col_num, row_num, True]
                door_locations.append(door_data)
            col_num += 1
        row_num += 1
    print(door_locations)

    return map1, door_locations

def generate_zones():
    im = Image.open('map_info/zones(256-colors).bmp') # This is a 256-color bmp. Pixel vales go from 0 to 255.
    pix = im.load()
    image_size = im.size  # Get the width and height of the image
    zones = []
    for y in range(image_size[1]):
        row_of_pixels = []
        for x in range(image_size[0]):
            if pix[x, y] == 0:
                row_of_pixels.append(0)
            elif pix[x, y] == 1:
                row_of_pixels.append(1)
            elif pix[x, y] == 2:
                row_of_pixels.append(2)
            elif pix[x, y] == 3:
                row_of_pixels.append(3)
            elif pix[x, y] == 4:
                row_of_pixels.append(4)
            elif pix[x, y] == 5:
                row_of_pixels.append(5)
            elif pix[x, y] == 6:
                row_of_pixels.append(6)
            elif pix[x, y] == 7:
                row_of_pixels.append(7)
            elif pix[x, y] == 164:
                row_of_pixels.append(8)
            elif pix[x, y] == 249:
                row_of_pixels.append(9)
            elif pix[x, y] == 250:
                row_of_pixels.append(10)
            elif pix[x, y] == 251:
                row_of_pixels.append(11)
            elif pix[x, y] == 252:
                row_of_pixels.append(12)
            elif pix[x, y] == 253:
                row_of_pixels.append(13)
            elif pix[x, y] == 254:
                row_of_pixels.append(14)
            elif pix[x, y] == 255:
                row_of_pixels.append(15)
            elif pix[x, y] == 192:
                row_of_pixels.append(16)
            elif pix[x, y] == 64:
                row_of_pixels.append(17)
            else:
                row_of_pixels.append(pix[x, y])
        zones.append(row_of_pixels)

    zone_map = numpy.array((
    zones[0], zones[1], zones[2], zones[3], zones[4], zones[5], zones[6], zones[7], zones[8], zones[9], zones[10], zones[11],
    zones[12], zones[13], zones[14], zones[15], zones[16], zones[17], zones[18], zones[19], zones[20], zones[21], zones[22],
    zones[23], zones[24], zones[25], zones[26], zones[27]))
    return zone_map

def locate_zone(position, zone_map):
    y = int(position[0])
    x = int(position[1])
    zone_number = zone_map[floor(x)][floor(y)]
    #print(f"You are in zone {zone_number}.")
    return zone_number
