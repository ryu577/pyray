import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageMath
import os
from pyray.shapes.twod.paraboloid import *
from pyray.shapes.twod.functional import *
from pyray.rotation import *


basedir = '.\\Images\\RotatingCube\\'
if os.name == 'posix':
    basedir = 'Images/RotatingCube/'


def heat_map(j):
    if j < 10:
        return "yellow"
    elif j < 20:
        return "orange"
    elif j < 30:
        return "orange"
    else:
        return "red"


## The singularity of a black hole.
im = Image.new("RGB", (2048, 2048), "black")
draw = ImageDraw.Draw(im, 'RGBA')
rot = general_rotation(np.array([1,0,0]), np.pi/2.0-0.1)
#rot = np.eye(3)
phi = np.pi/10
#phi = 0
for j in range(50):
    cmplx = np.exp(-1j*phi)*(1+j/400)
    generalized_arc(draw, r=rot, vec=np.array([0,0,1]),
                    point=np.array([cmplx.real,cmplx.imag,0]),
                    prcnt=0.6
                    , rgba=heat_map(j))

rot = np.eye(3)
for j in range(50):
    cmplx = np.exp(1j*np.pi+1j*phi)*(1+j/400)
    generalized_arc(draw, r=rot, vec=np.array([0,0,1]),
                    point=np.array([cmplx.real,cmplx.imag,0]),
                    prcnt=0.4
                    , rgba=heat_map(j))
im.show()

###########################
##

im = Image.new("RGB", (2048, 2048), "black")
draw = ImageDraw.Draw(im, 'RGBA')
#rot = general_rotation(np.array([1,0,0]), np.pi/2.0-0.1)
rot = np.eye(3)
phi = np.pi/10
generalized_arc(draw, r=rot, vec=np.array([0,0,1]),
                    point=np.array([1,0,0]),
                    prcnt=1.0
                    , rgba="red")

im.show()


########
rot = general_rotation(np.array([1,0,0]), np.pi/2.0-0.1)
im = Image.new("RGB", (2048, 2048), "black")
draw = ImageDraw.Draw(im, 'RGBA')

for k in range(10):
    generalized_arc(draw, r=np.eye(3), vec=np.array([0,0,1]),
                    point=np.array([1+k/80,0,0]),
                    prcnt=1.0
                    , rgba="red")

for k in range(30):
    draw; r=rot; vec=np.array([0,0,1]); point=np.array([1+k/80,0,0]); prcnt=1
    rgba=(255, 0, 0, 100);
    scale=200;
    shift=np.array([1000, 1000, 0]);
    width=5

    pt1 = np.dot(r, point)
    vec = vec / sum(vec**2)**0.5
    theta = np.pi * 2.0 / 80.0 * prcnt

    for i in range(0, 80):
        if i<40:
            r = general_rotation(np.array([1,0,0]), np.pi/2.0-0.2)
            r1 = general_rotation(np.dot(r, vec), theta)
        else:
            r = np.eye(3)
            r1 = general_rotation(np.dot(r, vec), theta)
        pt2 = np.dot(r1, pt1)
        draw.line(
            (pt1[0] *
                scale +
                shift[0],
                pt1[1] *
                scale +
                shift[1],
                pt2[0] *
                scale +
                shift[0],
                pt2[1] *
                scale +
                shift[1]),
            fill=rgba,
            width=width)
        pt1 = pt2



###############################
## Warped spacetime grid for black hole.
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
                        vec=np.array([0, 0, 1]),
                        radius=rad,
                        rgba=(255,20,147,50))

## Draw the event horizon.
z=-0.05
rad = np.sqrt(-t/z-t**2)
generalized_circle2(draw, r=r, center=np.array([0,0,z]), 
                    vec=np.array([0,0,1]), 
                    radius=rad,
                    rgba="red")

