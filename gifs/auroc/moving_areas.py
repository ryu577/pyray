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


def draw_gauss(draw, fn, ix=0,std=30,h1=0,h2=0,
                    alpha=0.15865525393145707, p=0.01,
                    rgb=(0,255,0)):
    draw_curve(fn, draw, rgba=rgb)
    #fn2 = lambda x:300-norm.pdf(x-250,gap,std)*7000
    #draw_curve(fn2,draw,rgba="red")
    delta = norm.isf(alpha,0,std)
    pts1 = color_graphs(draw, delta, fn)
    pts2 = color_graphs2(draw, delta, fn)
    pts = []
    for i in range(len(pts1)):
        x = pts1[i][0]*(1-p)+pts2[i][0]*p
        y = pts1[i][1]*(1-p)+pts2[i][1]*p
        pts.append((x,y))
    draw.polygon(pts,rgb+(100,))


def color_graphs(draw, delta, fn):
    x1 = 250+delta
    # The vertical line
    draw.line((x1,0,x1,512),fill=(255,255,0,150),width=1)
    y1 = fn(x1)
    pts = [(x1,y1),(x1,300),(x1+150,fn(x1+150))]
    for xx in np.arange(x1+150-1,x1,-1):
        yx = fn(xx)
        pts.append((xx,yx))
    #draw.polygon(pts,(0,255,0,100))
    return pts


def color_graphs2(draw, delta, fn):
    x1 = 250+delta
    draw.line((x1,0,x1,512),fill=(255,255,0,150),width=1)
    y2=fn(x1)
    pts = [(x1,y2),(x1,300),(x1-150,fn(x1-150))]
    for xx in np.arange(x1-150+1,x1,1):
        yx = fn(xx)
        pts.append((xx,yx))
    #draw.polygon(pts,(0,255,0,100))
    return pts


std = 30
alpha = 0.15865525393145707
delta = norm.isf(alpha,0,std)
font = ImageFont.truetype(font_loc, 15)
fn = lambda x:300-norm.pdf(x-250,0,std)*7000
for i in range(11):
    r = general_rotation(np.array([0,1,0]),np.pi*i/10)
    im = Image.new("RGB", (512,512), "black")
    draw = ImageDraw.Draw(im, 'RGBA')
    draw_gauss(draw, fn, p=i/10, std=std, alpha=alpha)
    arrowV1(draw, r, start=np.array([0,0,0]),
            end=np.array([1,0,0]), scale=50,
            shift=np.array([250+delta,320,0]),
            rgb=(127,255,30))
    if i==0:
        draw.text((250+delta+15, 300-30), "FPR", font=font)
        draw.text((250+delta+15, 300+20), "yes", font=font)
    if i==10:
        draw.text((250+delta-55, 300-30), "FPR", font=font)
        draw.text((250+delta-55, 300+20), "yes", font=font)
    im.save(basedir + 'im' + str(i) + '.png')



std = 30
gap = 50
alpha = 0.15865525393145707
delta = norm.isf(alpha,0,std)
font = ImageFont.truetype(font_loc, 15)
fn = lambda x:300-norm.pdf(x-250,gap,std)*7000
for i in range(11):
    r = general_rotation(np.array([0,1,0]),np.pi*i/10)
    im = Image.new("RGB", (512,512), "black")
    draw = ImageDraw.Draw(im, 'RGBA')
    draw_gauss(draw, fn, p=i/10, std=std, alpha=alpha,rgb=(255,0,0))
    arrowV1(draw, r, start=np.array([0,0,0]),
            end=np.array([1,0,0]), scale=50,
            shift=np.array([250+delta,320,0]),
            rgb=(127,255,30))
    if i==0:
        draw.text((250+delta+15, 300-30), "TPR", font=font)
        draw.text((250+delta+15, 300+20), "yes", font=font)
    if i==10:
        draw.text((250+delta-55, 300-30), "TPR", font=font)
        draw.text((250+delta-55, 300+20), "yes", font=font)
    im.save(basedir + 'im' + str(i) + '.png')


