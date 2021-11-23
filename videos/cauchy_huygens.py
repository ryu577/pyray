import numpy as np
from scipy.stats import cauchy
import os
from PIL import Image, ImageDraw
from pyray.shapes.oned.curve import *


basedir = '.\\Images\\RotatingCube\\'
if os.name == 'posix':
    basedir = 'Images/RotatingCube/'

im = Image.new("RGB", (512,512), "black")
draw = ImageDraw.Draw(im, 'RGBA')
fn = lambda x:500-cauchy.pdf((x-250)/50)*700
draw_curve(fn,draw)
draw.line((0,500,512,500),fill="white",width=1)
draw.line((250,0,250,512),fill="white",width=1)
im.save(basedir + 'im' + str(0) + '.png')

