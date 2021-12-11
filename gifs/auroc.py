import numpy as np
from scipy.stats import norm
from PIL import Image, ImageDraw, ImageFont, ImageMath
from pyray.shapes.twod.paraboloid import *
from pyray.shapes.zerod.pointswarm import *
from pyray.rotation import *
from pyray.imageutils import *
from pyray.axes import *
from pyray.shapes.oned.curve import draw_curve
from pyray.misc import zigzag2
import os


basedir = '.\\Images\\RotatingCube\\'
font_loc = "arial.ttf"
if os.name == 'posix':
    basedir = 'Images/RotatingCube/'
    font_loc = 'Arial.ttf'



#############################################################################
## Scene 9 - rotate scene.
for i in range(11):
    (im, draw) = binary_classificn_pts(4, r=planar_rotation(-np.pi/4*(i)/10))
    im.save(basedir + "/im" + str(int(i)) + ".png")

#############################################################################
## Scene 10 - let it rain over me.

ind = 11
for t in range(180):
    if t%5==0:
        (im, draw) = binary_classificn_pts(5, r=planar_rotation(-np.pi/4), t1=t)
        im.save(basedir + "/im" + str(int(ind)) + ".png")
        ind+=1

base = ind
im.close()
ind=0
for t in range(185):
    if t%5==0:
        (im, draw) = binary_classificn_pts(5, r=planar_rotation(-np.pi/4), t1=180, t2=t)
        im.save(basedir + "/im" + str(int(base+ind)) + ".png")
        ind+=1

base+=ind
for t in range(10):
    (im, draw) = binary_classificn_pts(5, r=planar_rotation(-np.pi/4), t1=180, t2=185)
    im.save(basedir + "/im" + str(int(base+t)) + ".png")

############################################


def draw_alpha_beta_curve(draw,alpha=0.15865525393145707,effect=50,std=30,draw_curve=True):
    font = ImageFont.truetype(font_loc, 12)
    # Draw the axes first.
    draw.line((26,332,26,332+150),fill=(255,0,0))
    draw.line((26,332+150,26+150,332+150),fill=(0,255,0))
    # Now draw the curve.
    if draw_curve:
        pt1 = np.array([26,332]); moving_beta=1.0
        for alp in np.arange(0.05,1.05,0.05):
            moving_beta = betafn(alp,effect,std)
            x1 = 26+alp*150; y1=332+(1-moving_beta)*150
            draw.line((pt1[0],pt1[1],x1,y1))
            pt1 = np.array([x1,y1])
    
    beta = betafn(alpha,effect,std)
    x1 = 26+alpha*150; y1 = 332+(1-beta)*150
    draw.ellipse((x1-3,y1-3,x1+3,y1+3),outline=(255,255,0),fill=(255,255,0,150))
    # The two lines from point to axes.
    draw.line((x1,y1,26,y1),fill=(0,255,0))
    draw.line((x1,y1,x1,332+150),fill=(255,0,0))
    # Legend for probabilities.
    draw.text((134-40,335),"FPR= "+str(round(alpha,2)), (0,255,0), font=font)
    draw.text((134-40,335+20),"FNR= "+str(round(beta,2)), (255,0,0), font=font)


def draw_roc_curve(draw,alpha=0.15865525393145707,effect=50,std=30,draw_curve=True):
    base_x = 250
    font = ImageFont.truetype(font_loc, 12)
    # Draw the axes first.
    draw.line((base_x,332,base_x,332+150),fill=(255,0,0))
    draw.line((base_x,332+150,base_x+150,332+150),fill=(0,255,0))
    # Now draw the curve.
    if draw_curve:
        pt1 = np.array([base_x,332+150]); moving_beta=0.0
        for alp in np.arange(0.05,1.05,0.05):
            moving_beta = betafn(alp,effect,std)
            x1 = base_x+alp*150; y1=332+(moving_beta)*150
            draw.line((pt1[0],pt1[1],x1,y1))
            pt1 = np.array([x1,y1])
    beta = betafn(alpha,effect,std)
    # Draw the point.
    x1 = base_x+(alpha)*150; y1 = 332+(beta)*150
    draw.ellipse((x1-3,y1-3,x1+3,y1+3),outline=(255,255,0),fill=(255,255,0,150))
    # The two lines from point to axes.
    draw.line((x1,y1,base_x,y1),fill=(0,255,0))
    draw.line((x1,y1,x1,332+150),fill=(255,0,0))
    # Legend for probabilities.
    draw.text((350-26+134-40,345),"FPR= "+str(round(alpha,2)), (0,255,0), font=font)
    draw.text((350-26+134-40,345+20),"TPR= "+str(round(1-beta,2)), (255,0,0), font=font)


def draw_confusion_matrix(draw):
    font = ImageFont.truetype(font_loc, 9)
    draw.polygon([(26, 200), (26, 250),
                    (26+50, 250), (26+50, 200)],\
                        outline=(255,255,255,150))
    draw.line((26,225,26+50,225))
    draw.line((26+25,200,26+25,250))
    draw.text((26+2, 200+2), "TPR", font=font)
    draw.text((26+2+25, 200+2), "FNR", font=font)
    draw.text((26+2, 200+2+25), "FPR", font=font)
    draw.text((26+2+25, 200+2+25), "TNR", font=font)
    draw.polygon([(26, 200+25), (26, 250),
                    (26+25, 250), (26+25, 200+25)],\
                        outline=(255,255,255,200),
                        fill=(0,255,0,100))
    draw.polygon([(26+25, 200), (26+25, 200+25),
                    (26+25*2, 200+25), (26+25*2, 200)],\
                        outline=(255,255,255,200),
                        fill=(255,0,0,100))
    draw.polygon([(26, 200), (26, 200+25),
                    (26+25, 200+25), (26+25, 200)],\
                        outline=(0,255,0))
    draw.polygon([(26+25, 200+25), (26+25, 200+25*2),
                    (26+25*2, 200+25*2), (26+25*2, 200+25)],\
                        outline=(255,0,0))


def betafn(alpha,effect,std):
    return norm.cdf(-effect+norm.isf(alpha,0,std),0,std)


def draw_two_gauss(draw,ix=0,extrema=500,std=30,h1=0,h2=0,gap=50,
                    alpha=0.15865525393145707):
    fn = lambda x:300-norm.pdf(x-250,0,std)*7000
    draw_curve(fn, draw, rgba="green")
    fn2 = lambda x:300-norm.pdf(x-250,gap,std)*7000
    draw_curve(fn2,draw,rgba="red")
    delta = norm.isf(alpha,0,std)
    color_graphs(draw, delta, fn, fn2, extrema)


def color_graphs(draw, delta, fn, fn2, extrema):
    x1 = 250+delta
    draw.line((x1,0,x1,512),fill=(255,255,0,150),width=1)
    y1 = fn(x1)
    pts = [(x1,y1),(x1,300),(extrema,fn(extrema))]
    for xx in np.arange(extrema-1,x1,-1):
        yx = fn(xx)
        pts.append((xx,yx))
    draw.polygon(pts,(0,255,0,100))
    y2=fn2(x1)
    pts = [(x1,y2),(x1,300),(180,fn2(180))]
    for xx in np.arange(179+1,x1,1):
        yx = fn2(xx)
        pts.append((xx,yx))
    draw.polygon(pts,(255,0,0,100))


def draw_full(gap=50, std=30, alpha=0.15865525393145707,
         write=False, ix=0):
    im = Image.new("RGB", (512,512), "black")
    draw = ImageDraw.Draw(im, 'RGBA')
    
    draw_two_gauss(draw, gap=gap, std=std, alpha=alpha)
    #draw_alpha_beta_curve(draw,alpha,std=std,effect=gap,draw_curve=True)
    #draw_roc_curve(draw,alpha,std=std,effect=gap,draw_curve=True)
    draw_confusion_matrix(draw)
    if not write:
        im.show()
    else:
        im.save(basedir + 'im' + str(ix) + '.png')


def main():
    i=0
    for alpha in np.arange(0.15865525393145707,.46,.08):
        draw_full(ix=i,gap=80,alpha=alpha,write=True)
        i+=1
    for alpha in np.arange(.46,.02,-.1):
        draw_full(ix=i,gap=80,alpha=alpha,write=True)
        i+=1
    for alpha in np.arange(.1,0.15865525393145707,.04):
        draw_full(ix=i,gap=80,alpha=alpha,write=True)
        i+=1


def main2():
    i=0
    for g in np.arange(80,5,-10):
        draw_full(ix=i,gap=g,alpha=0.15865525393145707,write=True)
        i+=1
    for g in np.arange(10,80,10):
        draw_full(ix=i,gap=g,alpha=0.15865525393145707,write=True)
        i+=1

