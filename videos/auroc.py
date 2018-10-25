from pyray.shapes.paraboloid import *
from pyray.shapes.pointswarm import *
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



#############################################################################
## Repeat functions.
#############################################################################

def make_again(extent=0, datt=[], scale=1, r=np.eye(2), t1=0, t2=0):
    # Basic stuff with points.
    w=5
    im = Image.new("RGB", (2048, 2048), (1, 1, 1))
    draw = ImageDraw.Draw(im, 'RGBA')
    means1_orig = np.array([500, 1500])
    means2_orig = np.array([1500, 500])

    means1 = generalized_planar_rotation(means1_orig, np.array([1000,1000]), r)
    means2 = generalized_planar_rotation(means2_orig, np.array([1000,1000]), r)
    p=0.3
    center_1_orig = means1_orig*p+means2_orig*(1-p)
    center_2_orig = means2_orig*p+means1_orig*(1-p)
    center_1 = means1*p+means2*(1-p)
    center_2 = means2*p+means1*(1-p)
    means = center_1
    stds = [300, 300]
    corr = 0.8         # correlation
    covs = [[stds[0]**2          , stds[0]*stds[1]*corr], 
            [stds[0]*stds[1]*corr,           stds[1]**2]] 
    np.random.seed(0)
    m_1 = np.random.multivariate_normal(center_1_orig, covs, 200)*scale
    m = m_1
    for i in range(m.shape[0]):
        r_pt = generalized_planar_rotation(m[i], np.array([1000,1000]), r)
        if extent < 2:
            draw.ellipse((r_pt[0]-w,r_pt[1]-w,r_pt[0]+w,r_pt[1]+w), fill = (255,255,102), outline = (0,0,0))
    means = center_2
    np.random.seed(4)
    m_2 = np.random.multivariate_normal(center_2_orig, covs, 200)*scale
    m = m_2
    for i in range(m.shape[0]):
        r_pt = generalized_planar_rotation(m[i], np.array([1000,1000]), r)
        if extent < 2:
            draw.ellipse((r_pt[0]-w,r_pt[1]-w,r_pt[0]+w,r_pt[1]+w), fill = (20,255,102), outline = (0,0,0))

    if extent > 0:
        # Draw the separating line.
        center = (center_1+center_2)/2
        orthog = -np.dot(planar_rotation(-np.pi/2), (center_2-center_1))
        main_dircn = (center_2 - center_1)
        p=2.0
        pt_1 = center + orthog*p
        pt_2 = center - orthog*p
        draw.line((pt_1[0], pt_1[1], pt_2[0], pt_2[1]), fill = 'orange', width = 7)

    avgs = []
    means = np.sum(m_1,axis=1)/2
    for i in range(len(means)):
        avgs.append( (((m_1[i][1]<m_1[i][0]))-0.5)*2*np.sqrt(sum((m_1[i]-means[i])**2)))
    avgs = np.array(avgs)
    dat1 = m_1[avgs > np.percentile(avgs,97)]
    for i in dat1:
        datt.append(i)
    xs = [1000]
    for i in range(1,8):
        pt_1_a = pt_1 + main_dircn*i/7
        pt_1_b = pt_1 - main_dircn*i/7
        pt_2_a = pt_2 + main_dircn*i/7
        pt_2_b = pt_2 - main_dircn*i/7
        draw.line((pt_1_a[0], pt_1_a[1], pt_2_a[0], pt_2_a[1]), fill = (255,255,255,100), width = 4)
        draw.line((pt_1_b[0], pt_1_b[1], pt_2_b[0], pt_2_b[1]), fill = (255,255,255,100), width = 4)
        xs.append(pt_1_a[0])
        xs.append(pt_1_b[0])
    xs.sort()
    xs.append(max(xs)+xs[1]-xs[0])
    xs.append(min(xs)-xs[1]+xs[0])
    # I basically want to transfer the last element to the first position
    # so sort is overkill. But it's a small array, so no matter.
    xs.sort()
    if extent >=2:
        drip_to_bins(draw, xs, m, t1, rgb=(20,255,102))
        drip_to_bins(draw, xs, m_1, t2, rgb=(255,255,102))
    return (im, draw)



