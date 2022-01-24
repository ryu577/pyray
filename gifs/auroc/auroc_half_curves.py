import numpy as np
from scipy.stats import norm
from PIL import Image, ImageDraw, ImageFont, ImageMath
from pyray.shapes.twod.paraboloid import *
from pyray.rotation import *
from pyray.imageutils import *
from pyray.axes import *
from pyray.shapes.oned.curve import draw_curve
from pyray.misc import zigzag2
from pyray.global_vars import *


def betafn(alpha,std1, std2):
    return norm.cdf(norm.isf(alpha,0,std1),0,std2)


def draw_axes(draw, base_x=250, base_y=320):
    font = ImageFont.truetype(font_loc, 15)
    # Draw the axes first.
    draw.line((base_x,base_y,base_x,base_y+150),fill=(255,0,0))
    draw.line((base_x,base_y+150,base_x+150,base_y+150),fill=(0,255,0))
    draw.line((base_x,base_y+150,base_x,base_y+150*2),fill=(255,0,0))
    draw.line((base_x,base_y+150,base_x-150,base_y+150),fill=(0,255,0))
    draw.text((base_x+150, base_y+150), "FPR", font=font)
    draw.text((base_x, base_y), "TPR", font=font)


def draw_main_curve(draw, std1=30, std2=40, base_x=250, base_y=320, width=1):
    pt1 = np.array([base_x,base_y+150])
    moving_beta=0.0
    for alp in np.arange(0.05,1.0+.05,0.05):
        moving_beta = betafn(alp,std1,std2)
        x1 = base_x+alp*150
        y1 = base_y+(moving_beta)*150
        draw.line((pt1[0],pt1[1],x1,y1),width=width)
        pt1 = np.array([x1,y1])


std = 40
fn = lambda x:300-norm.pdf(x-250,0,std)*7000
for i in range(5):
    fn1 = lambda x:300-norm.pdf(x-250,0,std+i*5)*7000
    im = Image.new("RGB", (512,512), "black")
    draw = ImageDraw.Draw(im, 'RGBA')
    draw_curve(fn, draw, rgba=(255,0,0))
    draw_curve(fn1, draw, rgba=(0,255,0))
    draw_axes(draw)
    draw_main_curve(draw, std1=std, std2=std+i*5,width=3)
    draw_main_curve(draw, std1=std, std2=std)
    im.save(basedir + 'im' + str(i) + '.png')

for i in range(10):
    fn1 = lambda x:300-norm.pdf(x-250,0,std+19-i*5)*7000
    im = Image.new("RGB", (512,512), "black")
    draw = ImageDraw.Draw(im, 'RGBA')
    draw_curve(fn, draw, rgba=(255,0,0))
    draw_curve(fn1, draw, rgba=(0,255,0))
    draw_axes(draw)
    draw_main_curve(draw, std1=std, std2=std+19-i*5,width=3)
    draw_main_curve(draw, std1=std, std2=std)
    im.save(basedir + 'im' + str(i+10) + '.png')


