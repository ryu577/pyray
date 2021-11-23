from pyray.shapes.twod.paraboloid import *
from pyray.shapes.zerod.pointswarm import *
from pyray.rotation import *
from pyray.imageutils import *
from pyray.axes import *
from PIL import Image, ImageDraw, ImageFont, ImageMath
import pandas as pd

w=5
im = Image.new("RGB", (2048, 2048), (1, 1, 1))
draw = ImageDraw.Draw(im, 'RGBA')

means1 = np.array([500, 1500])
means2 = np.array([1500, 500])

p=0.3
means = means1*p+means2*(1-p)
center_1 = means
stds = [300, 300]
corr = 0.8         # correlation
covs = [[stds[0]**2          , stds[0]*stds[1]*corr], 
        [stds[0]*stds[1]*corr,           stds[1]**2]] 

np.random.seed(0)
m = np.random.multivariate_normal(means, covs, 200)

for i in range(m.shape[0]):
    draw.ellipse((m[i][0]-w,m[i][1]-w,m[i][0]+w,m[i][1]+w), fill = (255,255,102), outline = (0,0,0))
    #if i%10==0:
    #   im.save("..\\images\\RotatingCube\\im" + str(int(i/10)) + ".png")

means = means2*p+means1*(1-p)
center_2 = means
np.random.seed(4)
m = np.random.multivariate_normal(means, covs, 200)
base = int(i/10)

for i in range(m.shape[0]):
    draw.ellipse((m[i][0]-w,m[i][1]-w,m[i][0]+w,m[i][1]+w), fill = (20,255,102), outline = (0,0,0))
    #if i%10==0:
    #   im.save("..\\images\\RotatingCube\\im" + str(int(base+i/10)) + ".png")
base += int(i/10)

txt = "Looking at this picture,\nwhat's the first thing you notice?"
for i in range(35):
    writeStaggeredText(txt, draw, i, speed=3)
    #im.save("..\\images\\RotatingCube\\im" + str(int(base+i)) + ".png")

#############################################################################

im.close()
(im, draw) = make_again()
#base += i+1

center = (center_1+center_2)/2
orthog = (center_2-center_1)*np.array([-1,1])


for i in range(16):
    p=i/8.0
    pt_1 = center + orthog*p
    pt_2 = center - orthog*p
    draw.line((pt_1[0], pt_1[1], pt_2[0], pt_2[1]), fill = 'orange', width = 7)
    im.save("..\\images\\RotatingCube\\im" + str(int(i)) + ".png")

base = i+1

txt = "Was it how the green\nand yellow dots\nare separated so well\nby this line?"
for i in range(35):
    writeStaggeredText(txt, draw, i, speed=3)
    im.save("..\\images\\RotatingCube\\im" + str(int(base+i)) + ".png")

#############################################################################
im.close()
(im, draw) = make_again(1)
txt = "This is what\na binary classfication\nproblem looks like.\nGiven the data,\ncome up with a model\nto predict the color of\neach point (given\nonly where it lies in space)."
for i in range(66):
    writeStaggeredText(txt, draw, i, speed=3)
    im.save("..\\images\\RotatingCube\\im" + str(int(i)) + ".png")

#############################################################################
mistakes = [(1113,1072),(1064,1003),(1010,961),(1064,1002),(1030,1061),(709,734)]

im.close()

txt = "However, looking at the picture it is clear that\nthe classifier made some mistakes."
for i in range(46):
    (im, draw) = make_again(1)
    writeStaggeredText(txt, draw, i, speed=3)
    for j in range(int(i/5)):
        v = mistakes[min(j,5)]
        ww = 15+5*np.sin(i*np.pi/10)
        draw.ellipse((v[0]-ww, v[1]-ww, v[0]+ww, v[1]+ww),
                         fill=(255,0,0,20), outline='red')
    im.save("..\\images\\RotatingCube\\im" + str(int(i)) + ".png")


#############################################################################

im.close()
txt = "The good news is that all the mistakes\nwere close to the boundary\nso the model\nwas never sure\nabout these points\nanyway."

for i in range(46):
    (im, draw) = make_again(1)
    writeStaggeredText(txt, draw, i, speed=4)
    for j in range(6):
        v = mistakes[min(j,5)]
        ww = 15+5*np.sin(i*np.pi/10)
        draw.ellipse((v[0]-ww, v[1]-ww, v[0]+ww, v[1]+ww),
                         fill=(255,0,0,20), outline='red')
    im.save("..\\images\\RotatingCube\\im" + str(int(i)) + ".png")

#############################################################################
im.close()
txt = "Maybe it's a good idea then\nfor the model to\nproduce a score for\neach point."
for i in range(33):
    (im, draw) = make_again(1)
    writeStaggeredText(txt, draw, i, speed=4)
    im.save("..\\images\\RotatingCube\\im" + str(int(i)) + ".png")

#############################################################################
im.close()
txt = "Say, high score\nmeans the point\nis probably yellow\nand low score means\nit's green."
for i in range(33):
    (im, draw) = make_again(1)
    writeStaggeredText(txt, draw, i, speed=4)
    im.save("..\\images\\RotatingCube\\im" + str(int(i)) + ".png")

#############################################################################
im.close()
txt = "For example,\nthe score could be the\ndistance from the orange line."

for i in range(29):
    (im, draw) = make_again(1)
    writeStaggeredText(txt, draw, i, speed=4)
    im.save("..\\images\\RotatingCube\\im" + str(int(i)) + ".png")



#############################################################################
im.close()
txt = "These points\nare far from\nthe orange line,\nso get a high\nscore."

for i in range(29):
    dd1 = []
    (im, draw) = make_again(1, dd1)
    writeStaggeredText(txt, draw, i, speed=4)
    for j in range(min(int(i/4), len(dd1))):
        pt = dd1[j]
        pt1 = np.concatenate((dd1[j],[0]))
        arrowV1(draw, np.eye(3), np.array([sum(pt)/2,sum(pt)/2,0])/100, np.array(pt1)/100, scale=100.0, shift=np.array([0,0,0]))
    im.save("..\\images\\RotatingCube\\im" + str(int(i)) + ".png")


for i in range(10):
    (im, draw) = make_again(1, dd1,1+i/4)
    im.save("..\\images\\RotatingCube\\im" + str(int(i)) + ".png")

#############################################################################

(im, draw) = make_again(1, dd1, r=planar_rotation(0))
im.save("..\\images\\RotatingCube\\im" + str(int(0)) + ".png")
im.save("..\\images\\RotatingCube\\im" + str(int(1)) + ".png")
im.save("..\\images\\RotatingCube\\im" + str(int(2)) + ".png")


im.close()
for i in range(3,14):
    (im, draw) = make_again(1, dd1, r=planar_rotation(-np.pi/4*(i-3)/10))
    im.save("..\\images\\RotatingCube\\im" + str(int(i)) + ".png")


##Scene: points falling like rain.
#############################################################################

base = i
im.close()
ind = 0
for t in range(180):
    if t%5==0:
        (im, draw) = make_again(2, dd1, r=planar_rotation(-np.pi/4), t1=t)
        im.save("..\\images\\RotatingCube\\im" + str(int(base+ind)) + ".png")
        ind+=1

##Scene: points falling like rain.
#############################################################################

base = base + ind
im.close()
ind=0
for t in range(185):
    if t%5==0:
        (im, draw) = make_again(2, dd1, r=planar_rotation(-np.pi/4), t1=180, t2=t)
        im.save("..\\images\\RotatingCube\\im" + str(int(base+ind)) + ".png")
        ind+=1


