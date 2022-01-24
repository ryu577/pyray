import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageMath
from pyray.axes import *
from pyray.rotation import *


pts1 = np.array([
    [0,0,0],
    [1,0,0],
    [2,0,0],
    [3,0,0],
    [4,0,0],
    [5,0,0],
    [6,0,0],
    [0,1,0],#
    [1,1,0],
    [2,1,0],
    [3,1,0],
    [0,2,0],
    [1,2,0],
    [2,2,0],
    [0,3,0]
])
scale = 64

for i in range(10):
    r = general_rotation(np.array([1,1,0]), np.pi/10*i)
    pts = np.dot(pts1, r)
    im = Image.new("RGB", (512, 512), (0,0,0))
    draw = ImageDraw.Draw(im,'RGBA')

    pts = pts * scale + np.array([20, 20, 0])

    for pt in pts:
        draw.ellipse((pt[0]-8, pt[1]-8, pt[0]+8, pt[1]+8), fill = (255,0,0,150), outline = (0,0,0))
    draw.line((20,20,255,255), 
                    fill=(120,120,120,120), width=2)

    basedir = '.\\images\\RotatingCube\\'
    im.save(basedir + "im" + str(i) + ".png")

for i in range(10):
    r = general_rotation(np.array([1,1,0]), np.pi/10*(10-i) )
    pts = np.dot(pts1, r)
    im = Image.new("RGB", (512, 512), (0,0,0))
    draw = ImageDraw.Draw(im,'RGBA')

    pts = pts * scale + np.array([20, 20, 0])

    for pt in pts:
        draw.ellipse((pt[0]-8, pt[1]-8, pt[0]+8, pt[1]+8), fill = (255,0,0,150), outline = (0,0,0))
    draw.line((20,20,255,255), 
                    fill=(120,120,120,120), width=2)

    basedir = '.\\images\\RotatingCube\\'
    im.save(basedir + "im" + str(i+10) + ".png")


# Convert to video and gif.
#ffmpeg -framerate 10 -f image2 -i im%d.png -vb 20M vid.avi
