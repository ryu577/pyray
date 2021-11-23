import numpy as np
from scipy.stats import binom, binom_test
from PIL import Image, ImageDraw, ImageFont, ImageMath
import os

basedir = '.\\Images\\RotatingCube\\'
if os.name == 'posix':
    basedir = 'Images/RotatingCube/'

base_y = 400
base_x = 100
n = 5
scale = 300

def draw_binom():
    im = Image.new("RGB", (512, 512), (0,0,0))
    draw = ImageDraw.Draw(im,'RGBA')

    #binom.pmf(np.arange(11),10,.5)
    for i in range(n+1):
        pt1 = [base_x+i*20,base_y]
        pt2 = [base_x+5+i*20,base_y]
        y = binom.pmf(i,n,.5)
        pt3 = [base_x+5+i*20,base_y-y*scale]
        pt4 = [base_x+i*20,base_y-y*scale]
        draw.polygon([(pt1[0], pt1[1]), (pt2[0], pt2[1]),
                    (pt3[0], pt3[1]), (pt4[0], pt4[1])],\
                        (0,102,255,150))
        draw.text((base_x+2.3+i*20,base_y+8), str(i))

    pt1 = [base_x-5, base_y]
    pt2 = [base_x-5, base_y-100]
    draw.line((pt1[0], pt1[1], pt2[0], pt2[1]), 
            fill = (255,255,255,100), width = 2)

    ticks = [ .1,  .2, .3]

    for ti in ticks:
        y = base_y-ti*300
        pt1 = [base_x, y]
        pt2 = [base_x+512, y]
        draw.line((pt1[0], pt1[1], pt2[0], pt2[1]), 
            fill = (120,120,255,40), width = 1)
        draw.text((base_x-33,y-3), str(ti))
    return im, draw

## Draw region of p-value.
j=3
for i in range(9):
    (im, draw) = draw_binom()
    x_ext = ((n-j)*20+10)*i/8
    pt1 = [base_x+j*20, base_y]
    pt2 = [base_x+j*20+x_ext, base_y]
    pt3 = [base_x+j*20+x_ext, base_y-0.4*scale]
    pt4 = [base_x+j*20, base_y-0.4*scale]

    draw.polygon([(pt1[0], pt1[1]), (pt2[0], pt2[1]),
                    (pt3[0], pt3[1]), (pt4[0], pt4[1])],\
                        (12,255,102,100))

    draw.line((pt1[0], pt1[1]+10, pt4[0], pt4[1]-10), 
            fill = (120,120,255,40), width = 1)

    draw.text((pt4[0],pt4[1]),"j=3")
    im.save(basedir + "im" + str(i) + ".png")

