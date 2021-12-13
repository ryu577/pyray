import numpy as np
from scipy.stats import norm
from PIL import Image, ImageDraw, ImageFont, ImageMath
from pyray.shapes.twod.paraboloid import *
from pyray.shapes.zerod.pointswarm import *
from pyray.rotation import *
from pyray.imageutils import *
from pyray.axes import *
from pyray.shapes.oned.curve import draw_curve
from pyray.misc import zigzag2
import os


basedir = '.\\Images\\RotatingCube\\'
font_loc = "arial.ttf"
if os.name == 'posix':
    basedir = 'Images/RotatingCube/'
    font_loc = 'Arial.ttf'



#############################################################################
## Scene 9 - rotate scene.
for i in range(11):
    (im, draw) = binary_classificn_pts(4, r=planar_rotation(-np.pi/4*(i)/10))
    im.save(basedir + "/im" + str(int(i)) + ".png")

#############################################################################
## Scene 10 - let it rain over me.

ind = 11
for t in range(180):
    if t%5==0:
        (im, draw) = binary_classificn_pts(5, r=planar_rotation(-np.pi/4), t1=t)
        im.save(basedir + "/im" + str(int(ind)) + ".png")
        ind+=1

base = ind
im.close()
ind=0
for t in range(185):
    if t%5==0:
        (im, draw) = binary_classificn_pts(5, r=planar_rotation(-np.pi/4), t1=180, t2=t)
        im.save(basedir + "/im" + str(int(base+ind)) + ".png")
        ind+=1

base+=ind
for t in range(10):
    (im, draw) = binary_classificn_pts(5, r=planar_rotation(-np.pi/4), t1=180, t2=185)
    im.save(basedir + "/im" + str(int(base+t)) + ".png")
