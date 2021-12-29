import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageMath
import os


basedir = '.\\Images\\RotatingCube\\'
font_loc = "arial.ttf"
if os.name == 'posix':
    basedir = 'Images/RotatingCube/'
    font_loc = 'Arial.ttf'


def circle(draw, center = (256,256), r=50, frac=1.0, start_angle=0):
    for t in np.arange(start_angle, start_angle+2*np.pi*frac+0.01, 0.01):
        pt1 = np.exp(-1j*t)*r + (center[0]+1j)+center[1]*(1j)
        pt2 = np.exp(-1j*(t+0.01))*r+(center[0]+1j)+center[1]*(1j)
        draw.line((pt1.real, pt1.imag, pt2.real, pt2.imag), fill=(255,0,0))



r=30
center_o = np.array([500-r,256])
base_pt = center_o + np.array([0,r])
for ix in range(11):
    im = Image.new("RGB", (512,512), "black")
    draw = ImageDraw.Draw(im, 'RGBA')
    t = np.pi*2*ix/10
    center = center_o + np.array([-t*r,r])
    circle(draw, center, r, 1-t/2/np.pi, np.pi/2)
    pt2 = center-np.array([0,r])
    draw.line((base_pt[0],base_pt[1]-r, center[0], center[1]-r), fill=(255,0,0))
    im.save(basedir + 'im' + str(ix) + '.png')



im = Image.new("RGB", (512,512), "black")
draw = ImageDraw.Draw(im, 'RGBA')
r=30
center = (256,256)
circle(draw, center, r, 0.7, np.pi/2)

