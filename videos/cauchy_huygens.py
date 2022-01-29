import os

import numpy as np
from PIL import Image, ImageDraw
from scipy.stats import cauchy

from pyray.shapes.oned.curve import *

basedir = ".\\Images\\RotatingCube\\"
if os.name == "posix":
    basedir = "Images/RotatingCube/"

im = Image.new("RGB", (512, 512), "black")
draw = ImageDraw.Draw(im, "RGBA")
fn = lambda x: 256 - cauchy.pdf((x - 256) / 50) * 700
draw_curve(fn, draw)
draw.line((0, 256, 512, 256), fill="white", width=1)
draw.line((256, 0, 256, 512), fill="white", width=1)
draw.line((0, 512, 512, 0), fill="red", width=2)
im.save(basedir + "im" + str(0) + ".png")
