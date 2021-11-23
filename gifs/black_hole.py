import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageMath
import os
from pyray.shapes.twod.paraboloid import *
from pyray.shapes.twod.functional import *
from pyray.rotation import *


basedir = '.\\Images\\RotatingCube\\'
if os.name == 'posix':
    basedir = 'Images/RotatingCube/'


## Make circular image of black hole.
base_y = 400
base_x = 100
n = 5
scale = 300

im = Image.new("RGB", (512, 512), (0,0,0))
draw = ImageDraw.Draw(im, 'RGBA')

r = 50

for x in range(50):
    y = np.sqrt(r**2-x**2)
    pt1 = [x+10, y]
    y1 = np.sqrt(r**2-(x+1)**2)
    pt2 = [x+11, y1]
    draw.line((pt1[0], pt1[1], pt2[0], pt2[1]), 
            fill = (120,120,255,255), width = 3)


###############################

## Grid for black hole.
im_ind=0; scale=200; shift=np.array([1000,1000,0])

r1 = np.eye(4)
rot = general_rotation(np.array([0,0,1]), np.pi/20.0 * (8 + im_ind/3.0))
j=4
r = rotation(3, 2 * np.pi * j /30.0)
rr = general_rotation(np.array([0,1,0]), np.pi/20.0 * (im_ind/7.0))
r = np.dot(r, rr)
r = np.dot(r, rot)
r1[:3, :3] = r
im = Image.new("RGB", (2048, 2048), "black")
draw = ImageDraw.Draw(im, 'RGBA')
render_scene_4d_axis(draw, r1, 4, scale, shift)
t=0.1

ix=0
z1 = -0.000001
while abs(z1) < 1/t:
    ix += 1
    z1 -= 0.0001*ix**1.1
    z = z1
    rad = np.sqrt(-t/z-t**2)
    generalized_circle2(draw, r=r, center=np.array([0,0,z]), 
                    vec=np.array([0,0,1]), 
                    radius=rad,
                    rgba=(255,20,147,50))

z=-0.05
rad = np.sqrt(-t/z-t**2)
generalized_circle2(draw, r=r, center=np.array([0,0,z]), 
                    vec=np.array([0,0,1]), 
                    radius=rad,
                    rgba="red")

