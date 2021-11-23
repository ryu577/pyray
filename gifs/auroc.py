import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageMath
from pyray.shapes.twod.paraboloid import *
from pyray.shapes.zerod.pointswarm import *
from pyray.rotation import *
from pyray.imageutils import *
from pyray.axes import *
import pandas as pd
import os

basedir = '.\\Images\\RotatingCube\\'
if os.name == 'posix':
    basedir = 'Images/RotatingCube/'

#############################################################################
## Scene 9 - rotate scene.
for i in range(11):
    (im, draw) = binary_classificn_pts(4, r=planar_rotation(-np.pi/4*(i)/10))
    im.save(basedir + "/im" + str(int(i)) + ".png")

#############################################################################
## Scene 10 - let it rain over me.
txt = "Like this..."

ind = 11
for t in range(180):
    if t%5==0:
        (im, draw) = binary_classificn_pts(5, r=planar_rotation(-np.pi/4), t1=t)
        #writeStaggeredText(txt, draw, ind, speed=1)
        im.save(basedir + "/im" + str(int(ind)) + ".png")
        ind+=1

base = ind
im.close()
ind=0
for t in range(185):
    if t%5==0:
        (im, draw) = binary_classificn_pts(5, r=planar_rotation(-np.pi/4), t1=180, t2=t)
        #writeStaggeredText(txt, draw, base+ind, speed=1)
        im.save(basedir + "/im" + str(int(base+ind)) + ".png")
        ind+=1

base+=ind
for t in range(10):
    (im, draw) = binary_classificn_pts(5, r=planar_rotation(-np.pi/4), t1=180, t2=185)
    #writeStaggeredText(txt, draw, base+t, speed=1)
    im.save(basedir + "/im" + str(int(base+t)) + ".png")
