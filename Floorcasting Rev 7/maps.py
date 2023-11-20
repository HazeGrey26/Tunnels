import numpy
from PIL import Image

# Generates the game map
# The map is flipped across the y-axis. It is a mirror image of the intended map...


def generate_map():
    # Color of wall = 0
    # Color of blank space = 0
    # Color of door = 15
    im = Image.open('map_info/map.bmp')
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
        map.append(row_of_pixels)

    map1 = numpy.array((
    map[0], map[1], map[2], map[3], map[4], map[5], map[6], map[7], map[8], map[9], map[10], map[11],
    map[12], map[13], map[14], map[15], map[16], map[17], map[18], map[19], map[20], map[21], map[22],
    map[23], map[24], map[25], map[26], map[27]))
    return map1


# [x_pox, y_pos, points, purchased, location on map]
map_buy_details = [[32, 17, 100, False, (32, 18)], [29, 12, 100, False, (29, 11)], [11, 17, 100, False, (11, 18)],
                   [21, 17, 100, False, (8, 22)], [5, 3, 100, False, (5, 4)]]

