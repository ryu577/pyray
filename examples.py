import numpy as np
from circle import * 
from rotation import *


def draw_rotating_hot_pink_sphere():
    for i in np.arange(30):
        r = rotation(3, np.pi*i/10.0)
        im = Image.new("RGB", (2024, 2024), (1, 1, 1))
        draw = ImageDraw.Draw(im, 'RGBA')
        draw_sphere(draw, np.array([0,0,0]), np.array([0,0,1]), 1, r,)
        im.save('Images\\RotatingCube\\im' + str(i) + '.png')

if __name__ == "__main__":
    draw_rotating_hot_pink_sphere()