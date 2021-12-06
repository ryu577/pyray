import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageMath
import os
from pyray.shapes.twod.paraboloid import *
from pyray.shapes.twod.functional import *
from pyray.rotation import *


im = Image.new("RGB", (2048, 2048), "black")
draw = ImageDraw.Draw(im, 'RGBA')
########
for k in range(10):
    generalized_arc(draw, r=np.eye(3), vec=np.array([0,0,1]),
                    point=np.array([1+k/40,0,0]),
                    prcnt=0.5
                    , rgba="red", width=2)

rot = general_rotation(np.array([1,0,0]), np.pi/2.0-0.1)

for k in range(30):
    draw; r=rot; vec=np.array([0,0,1]); point=np.array([1+k/80,0,0]); prcnt=1
    rgba=(255, 0, 0, 100);
    scale=200;
    shift=np.array([1000, 1000, 0]);
    
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
            width=7)
        pt1 = pt2

def make_streaks(col):
    for k in range(10):
        u = np.random.uniform()
        z = (1+k/40)*np.exp(1j*2*np.pi*u)
        generalized_arc(draw, r=np.eye(3), vec=np.array([0,0,1]),
                        point=np.array([z.real,z.imag,0]),
                        prcnt=0.05
                        , rgba=col, width=8)

    for k in range(10):
        u = np.random.uniform()
        z = (1+k/40)*np.exp(1j*1*np.pi*u)
        rot = general_rotation(np.array([1,0,0]), np.pi/2.0-0.2)
        generalized_arc(draw, r=rot, vec=np.array([0,0,1]),
                        point=np.array([z.real,z.imag,0]),
                        prcnt=0.05
                        , rgba=col, width=4)

make_streaks((255,255,0,50))
make_streaks((255,127,80,50))
make_streaks((255,140,0,50))

im.show()

