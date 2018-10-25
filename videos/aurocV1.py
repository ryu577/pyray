import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageMath
from pyray.shapes.paraboloid import *
from pyray.shapes.pointswarm import *
from pyray.rotation import *
from pyray.imageutils import *
from pyray.axes import *
import pandas as pd


#############################################################################
## Scene 1 - this is a space.
im = Image.new("RGB", (2048, 2048), (1, 1, 1))
draw = ImageDraw.Draw(im, 'RGBA')
txt = "This is a space..."
for i in range(20):
    writeStaggeredText(txt, draw, i, speed=2)
    im.save("..\\images\\RotatingCube\\im" + str(int(i)) + ".png")

#############################################################################
## Scene 2 - It has infinite points.
base = i
(im, draw) = binary_classificn_pts(0)
txt = "It has infinite points..."
np.random.seed(0)
width=5
for i in range(40):
    pt = [int(np.random.uniform()*2048), int(np.random.uniform()*2048)]
    draw.ellipse((pt[0]-width,pt[1]-width,pt[0]+width,pt[1]+width),fill=(150,150,150))
    writeStaggeredText(txt, draw, i, speed=2)
    im.save("..\\images\\RotatingCube\\im" + str(int(i+base)) + ".png")

#############################################################################
## Scene 3 - but that's boring.
txt = "But that's boring\nlet's color the points\nred and green."
w=width
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

(im, draw) = binary_classificn_pts(0)
for i in range(m.shape[0]):
    draw.ellipse((m[i][0]-w,m[i][1]-w,m[i][0]+w,m[i][1]+w), fill = (255,20,102), outline = (0,0,0))
    if i%10==0:
       writeStaggeredText(txt, draw, int(i/10), speed=2)
       im.save("..\\images\\RotatingCube\\im" + str(int(i/10)) + ".png")

means = means2*p+means1*(1-p)
center_2 = means
np.random.seed(4)
m = np.random.multivariate_normal(means, covs, 200)
base = int(i/10)


for i in range(m.shape[0]):
    draw.ellipse((m[i][0]-w,m[i][1]-w,m[i][0]+w,m[i][1]+w), fill = (20,255,102), outline = (0,0,0))
    if i%10==0:
       writeStaggeredText(txt, draw, base+int(i/10), speed=2)
       im.save("..\\images\\RotatingCube\\im" + str(int(base+i/10)) + ".png")

#############################################################################
## Scene 4 - given data, can we guess color of new points.
txt = "Now given the data from\nthe points on the screen,\ncan we predict the color\nof any new points\nin this space?"
width = 5
(im, draw) = binary_classificn_pts(2)
for i in range(40): 
    writeStaggeredText(txt, draw, i, speed=4)
    pt = [int(np.random.uniform()*2048), int(np.random.uniform()*2048)]
    draw.ellipse((pt[0]-width,pt[1]-width,pt[0]+width,pt[1]+width),fill=(150,150,150,200))
    im.save("..\\images\\RotatingCube\\im" + str(i) + ".png")

#############################################################################
## Scene 5 - given data, can we guess color of new points.
txt = "Now given the data from\nthe points on the screen,\ncan we predict the color\nof any new points\nin this space?"
width = 5
(im, draw) = binary_classificn_pts(2)
for i in range(40): 
    writeStaggeredText(txt, draw, i, speed=4)
    pt = [int(np.random.uniform()*2048), int(np.random.uniform()*2048)]
    draw.ellipse((pt[0]-width,pt[1]-width,pt[0]+width,pt[1]+width),fill=(150,150,150,200))
    im.save("..\\images\\RotatingCube\\im" + str(i) + ".png")

#############################################################################
## Scene 6 - separating line.
# Draw the separating line.

txt = "One way is to\nsay everything to the\ntop right of this line\nis red and bottom left\nis green."
center = (center_1+center_2)/2
orthog = -np.dot(planar_rotation(-np.pi/2), (center_2-center_1))
main_dircn = (center_2 - center_1)
p=2.0
pt_1 = center + orthog*p
(im, draw) = binary_classificn_pts(2)
for i in range(37):
    writeStaggeredText(txt, draw, i, speed=4)
    pt_2 = pt_1 - orthog* min(4,i/7.5)
    draw.line((pt_1[0], pt_1[1], pt_2[0], pt_2[1]), fill = 'grey', width = 7)
    im.save("..\\images\\RotatingCube\\im" + str(i) + ".png")


#############################################################################
## Scene 7 - scores.

txt = "We can even give\neach point a score, the perpendicular\ndistance from the line."
for i in range(60):
    dd1 = []
    (im, draw) = binary_classificn_pts(3, dd1)
    writeStaggeredText(txt, draw, i, speed=2)
    for j in range(min(int(i/4), len(dd1))):
        pt = dd1[j]
        pt1 = np.concatenate((dd1[j],[0]))
        if pt1[0]>pt1[1]:
            arrowV1(draw, np.eye(3), np.array(pt1)/100, np.array([sum(pt)/2,sum(pt)/2,0])/100, scale=100.0, shift=np.array([0,0,0]), rgb=(255,30,100))
        else:
            arrowV1(draw, np.eye(3), np.array(pt1)/100, np.array([sum(pt)/2,sum(pt)/2,0])/100, scale=100.0, shift=np.array([0,0,0]), rgb=(20,255,102))
    im.save("..\\images\\RotatingCube\\im" + str(int(i)) + ".png")


#############################################################################
## Scene 8 - bins.

txt = "One way to visualize\nthese scores is to\nbin them."
main_dircn = (center_2 - center_1)

for i in range(33):
    (im, draw) = binary_classificn_pts(3, dd1)
    for j in range(1,min(8,int(i/2))):
        pt_1_a = pt_1 + main_dircn*j/7
        pt_1_b = pt_1 - main_dircn*j/7
        
        pt_2_a = pt_2 + main_dircn*j/7
        pt_2_b = pt_2 - main_dircn*j/7
        
        pt_1_c = (pt_1_a+pt_2_a)/2
        pt_2_c = (pt_1_b+pt_2_b)/2

        pt_1_c = np.concatenate((pt_1_c,[0]))
        pt_2_c = np.concatenate((pt_2_c,[0]))
        draw.line((pt_1_a[0], pt_1_a[1], pt_2_a[0], pt_2_a[1]), fill = (255,255,255,100), width = 4)
        draw.line((pt_1_b[0], pt_1_b[1], pt_2_b[0], pt_2_b[1]), fill = (255,255,255,100), width = 4)
        
    pt_c = (pt_1+pt_2)/2
    pt_c = np.concatenate((pt_c,[0]))
    writeStaggeredText(txt, draw, i, speed=2)
    if i>3 and i<19:
        arrowV1(draw, np.eye(3), pt_c/100, pt_2_c/100, scale=100.0, shift=np.array([0,0,0]), rgb=(255,255,80))
        arrowV1(draw, np.eye(3), pt_c/100, pt_1_c/100, scale=100.0, shift=np.array([0,0,0]), rgb=(255,255,80))
        
    im.save("..\\images\\RotatingCube\\im" + str(int(i)) + ".png")


#############################################################################
## Scene 9 - rotate scene.


for i in range(11):
    (im, draw) = binary_classificn_pts(4, r=planar_rotation(-np.pi/4*(i)/10))
    im.save("..\\images\\RotatingCube\\im" + str(int(i)) + ".png")

#############################################################################
## Scene 10 - let it rain over me.
txt = "Like this..."

ind = 0
for t in range(180):
    if t%5==0:
        (im, draw) = binary_classificn_pts(5, r=planar_rotation(-np.pi/4), t1=t)
        #writeStaggeredText(txt, draw, ind, speed=1)
        im.save("..\\images\\RotatingCube\\im" + str(int(ind)) + ".png")
        ind+=1

base = ind
im.close()
ind=0
for t in range(185):
    if t%5==0:
        (im, draw) = binary_classificn_pts(5, r=planar_rotation(-np.pi/4), t1=180, t2=t)
        #writeStaggeredText(txt, draw, base+ind, speed=1)
        im.save("..\\images\\RotatingCube\\im" + str(int(base+ind)) + ".png")
        ind+=1

base+=ind
for t in range(10):
    (im, draw) = binary_classificn_pts(5, r=planar_rotation(-np.pi/4), t1=180, t2=185)
    #writeStaggeredText(txt, draw, base+t, speed=1)
    im.save("..\\images\\RotatingCube\\im" + str(int(base+t)) + ".png")
    
#############################################################################
## Scene 11 - not a bad model.

txt = "This is a pretty good\nmodel but it isn't perfect."
j=0
for j in np.arange(26):
    (im, draw) = binary_classificn_pts(5, r=planar_rotation(-np.pi/4), t1=180, t2=185)
    writeStaggeredText(txt, draw, j, speed=3)
    im.save("..\\images\\RotatingCube\\im" + str(int(j)) + ".png")

#############################################################################
## Scene 12 - red have high.

txt = "The red points have\nhigh scores.."
j=0
for j in np.arange(26):
    (im, draw) = binary_classificn_pts(5, r=planar_rotation(-np.pi/4), t1=180, t2=185, trnsp1=120-4*j, trp1_hi=120-4*j, trp1_lo=120-4*j)
    writeStaggeredText(txt, draw, j, speed=3)
    im.save("..\\images\\RotatingCube\\im" + str(int(j)) + ".png")



#############################################################################
## Scene 13 - green have low.

txt = "while the greens\nhave low scores.."
j=0
for j in np.arange(26):
    (im, draw) = binary_classificn_pts(5, r=planar_rotation(-np.pi/4), t1=180, t2=185, trnsp2=120-4*j, trnsp1=120-100+4*j,
        trp1_hi=120-100+4*j,trp1_lo=120-100+4*j,trp2_hi=120-4*j,trp2_lo=120-4*j)
    writeStaggeredText(txt, draw, j, speed=3)
    im.save("..\\images\\RotatingCube\\im" + str(int(j)) + ".png")


#############################################################################
## Scene 14 - best we can do.

txt = "The best we can do\nis call everything in\nthe right half red.."
j=0
for j in np.arange(31):
    (im, draw) = binary_classificn_pts(5, r=planar_rotation(-np.pi/4), t1=180, t2=185, trnsp2=120-100+4*j, trnsp1=120,
        trp1_hi=120,trp1_lo=120,trp2_hi=120-100+4*j,trp2_lo=120-100+4*j)
    xx = 1000+j*(2048-1000)/31
    pt1 = (1000,2048)
    pt2 = (1000,0)
    pt3 = (xx, 0)
    pt4 = (xx,2048)
    draw.polygon([pt1,pt2,pt3,pt4], fill=(255,20,102,100))
    writeStaggeredText(txt, draw, j, speed=3)
    im.save("..\\images\\RotatingCube\\im" + str(int(j)) + ".png")

#############################################################################
## Scene 15 - left half green.

txt = "And the left part green.."
j=0
for j in np.arange(31):
    (im, draw) = binary_classificn_pts(5, r=planar_rotation(-np.pi/4), t1=180, t2=185, trnsp2=120-100+4*j, trnsp1=120,
        trp1_hi=120,trp1_lo=120,trp2_hi=120-100+4*j,trp2_lo=120-100+4*j)
    #xx = 1000+j*(2048-1000)/31
    xx = 2048
    pt1 = (1000,2048)
    pt2 = (1000,0)
    pt3 = (xx, 0)
    pt4 = (xx,2048)
    draw.polygon([pt1,pt2,pt3,pt4], fill=(255,20,102,100))
    xx = 1000-j*(2048-1000)/31
    pt1 = (1000,2048)
    pt2 = (1000,0)
    pt3 = (xx, 0)
    pt4 = (xx,2048)
    draw.polygon([pt1,pt2,pt3,pt4], fill=(20,255,102,100))
    writeStaggeredText(txt, draw, j, speed=3)
    im.save("..\\images\\RotatingCube\\im" + str(int(j)) + ".png")


#############################################################################
## Scene 16 - 

txt = "But even this\nmeans the highlighted points\nare the wrong color."
j=0
for j in np.arange(38):
    (im, draw) = binary_classificn_pts(5, r=planar_rotation(-np.pi/4), t1=180, t2=185, 
        trnsp2=120-j*3, trnsp1=120-j*3,
        trp1_hi=120+j*2,trp1_lo=120-j*3,trp2_hi=120-j*3,trp2_lo=120+j*2,
        hi1_ind=8, lo1_ind=0,
        hi2_ind=13, lo2_ind=9)
    #xx = 1000+j*(2048-1000)/31
    xx = 2048
    pt1 = (1000,2048)
    pt2 = (1000,0)
    pt3 = (xx, 0)
    pt4 = (xx,2048)
    draw.polygon([pt1,pt2,pt3,pt4], fill=(255,20,102,max(100-j*3,10)))
    xx = 0
    pt1 = (1000,2048)
    pt2 = (1000,0)
    pt3 = (xx, 0)
    pt4 = (xx,2048)
    draw.polygon([pt1,pt2,pt3,pt4], fill=(20,255,102,max(100-j*3,10) ))
    writeStaggeredText(txt, draw, j, speed=3)
    im.save("..\\images\\RotatingCube\\im" + str(int(j)) + ".png")


#############################################################################
## Scene 17 - 

txt = "If the distributions\nare completely separated\nwe get a perfect classifier."
j=0
for j in np.arange(38):
    (im, draw) = binary_classificn_pts(5, r=planar_rotation(-np.pi/4), t1=180, t2=185, 
        trnsp2=120-37*3+j*3, trnsp1=120-37*3+j*3,
        trp1_hi=120+37*2-j*2,trp1_lo=120-37*3+j*3,trp2_hi=120-37*3+j*3,trp2_lo=120-37*2+j*2,
        hi1_ind=8, lo1_ind=0,
        hi2_ind=13, lo2_ind=9,
        xshift1=-j*3,xshift2=j*3)
    writeStaggeredText(txt, draw, j, speed=3)
    im.save("..\\images\\RotatingCube\\im" + str(int(j)) + ".png")

#############################################################################
## Scene 18 (static)- 

txt = "If the distributions\nare completely separated\nwe get a perfect classifier."
j=0
for j in np.arange(8):
    (im, draw) = binary_classificn_pts(5, r=planar_rotation(-np.pi/4), t1=180, t2=185, 
        xshift1=-37*3,xshift2=37*3)
    writeStaggeredText(txt, draw, j+37, speed=3)
    im.save("..\\images\\RotatingCube\\im" + str(int(j)) + ".png")

#############################################################################
## Scene 19 - 

txt = "In the next video\nwe will convert these\nscores to a single metric."
j=0
for j in np.arange(28):
    (im, draw) = binary_classificn_pts(5, r=planar_rotation(-np.pi/4), t1=180, t2=185, 
        xshift1=-37*3,xshift2=37*3)
    writeStaggeredText(txt, draw, j, speed=3)
    im.save("..\\images\\RotatingCube\\im" + str(int(j)) + ".png")


#############################################################################
## Scene 20 - 

txt = "That captures the\nquality of the classifier\nthat produced the scores."
j=0
for j in np.arange(36):
    (im, draw) = binary_classificn_pts(5, r=planar_rotation(-np.pi/4), t1=180, t2=185, 
        xshift1=-37*3,xshift2=37*3)
    writeStaggeredText(txt, draw, j, speed=3)
    im.save("..\\images\\RotatingCube\\im" + str(int(j)) + ".png")



