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
from pyray.global_vars import *


def betafn(alpha,effect,std):
    return norm.cdf(-effect+norm.isf(alpha,0,std),0,std)


def draw_axes(draw, base_x=250, base_y=180):
    font = ImageFont.truetype(font_loc, 15)
    # Draw the axes first.
    draw.line((base_x,base_y,base_x,base_y+150),fill=(255,0,0))
    draw.line((base_x,base_y+150,base_x+150,base_y+150),fill=(0,255,0))
    draw.line((base_x,base_y+150,base_x,base_y+150*2),fill=(255,0,0))
    draw.line((base_x,base_y+150,base_x-150,base_y+150),fill=(0,255,0))
    draw.text((base_x+150, base_y+150), "FPR", font=font)
    draw.text((base_x, base_y), "TPR", font=font)
    draw.text((base_x-150, base_y+150), "-FPR", font=font)
    draw.text((base_x, base_y+150*2), "-TPR", font=font)


def draw_pt(draw,alpha=0.15865525393145707,effect=50,std=30,
            base_x=250, base_y=180):
    # Now draw the curve.
    beta = betafn(alpha,effect,std)
    # Draw the point.
    x1 = base_x+(alpha)*150; y1 = base_y+(beta)*150
    draw.ellipse((x1-3,y1-3,x1+3,y1+3),outline=(255,255,0),fill=(255,255,0,150))
    # The two lines from point to axes.
    draw.line((x1,y1,base_x,y1),fill=(0,255,0))
    draw.line((x1,y1,x1,base_y+150),fill=(255,0,0))


def draw_main_curve(draw, effect=50, std=30, base_x=250, base_y=180, alpha_mx=1.0):
    pt1 = np.array([base_x,base_y+150]); moving_beta=0.0
    for alp in np.arange(0.05,alpha_mx+.05,0.05):
        moving_beta = betafn(alp,effect,std)
        x1 = base_x+alp*150
        y1 = base_y+(moving_beta)*150
        draw.line((pt1[0],pt1[1],x1,y1))
        pt1 = np.array([x1,y1])


def draw_neg_curve(draw, effect=50, std=30, base_x=250, base_y=180, alpha_mx=1.0):
    pt1 = np.array([base_x,base_y+150])
    moving_beta=0.0
    for alp in np.arange(0.05,alpha_mx+.05,0.05):
        moving_beta = betafn(alp,effect,std)
        x1 = base_x-alp*150
        y1 = base_y+150+(1-moving_beta)*150
        draw.line((pt1[0],pt1[1],x1,y1),fill="orange",width=3)
        pt1 = np.array([x1,y1])

effect = 50
std=30
for i in range(16):
    pp = np.sin(i*2*np.pi/30)**2
    im = Image.new("RGB", (512,512), "black")
    draw = ImageDraw.Draw(im, 'RGBA')
    draw_axes(draw)
    draw_pt(draw, alpha=pp)
    draw_main_curve(draw, effect, std, alpha_mx=pp)
    draw_neg_curve(draw, alpha_mx=pp)
    im.save(basedir + 'im' + str(i) + '.png')

