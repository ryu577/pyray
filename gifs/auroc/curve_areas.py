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


def draw_axes(draw, base_x=250, base_y=180):
    font = ImageFont.truetype(font_loc, 15)
    # Draw the axes first.
    draw.line((base_x,base_y,base_x,base_y+150),fill=(255,0,0))
    draw.line((base_x,base_y+150,base_x+150,base_y+150),fill=(0,255,0))
    draw.line((base_x,base_y+150,base_x,base_y+150*2),fill=(255,0,0))
    draw.line((base_x,base_y+150,base_x-150,base_y+150),fill=(0,255,0))
    draw.text((base_x+150, base_y+150), "FPR", font=font)
    draw.text((base_x-30, base_y), "TPR", font=font)
    draw.text((base_x+75, base_y+75), "P(A>B)")
    draw.text((base_x+15, base_y+10), "P(B>A)")
    #draw.text((base_x-150, base_y+150), "-FPR", font=font)
    #draw.text((base_x, base_y+150*2), "-TPR", font=font)


def draw_main_curve(draw, effect=50, std=30, base_x=250, base_y=180, alpha_mx=1.0):
    """
    Draws AUROC curve along with shaded areas.
    """
    pts = [(base_x+150, base_y+150), (base_x,base_y+150)]
    pts2 = [(base_x, base_y), (base_x,base_y+150)]
    pt1 = np.array([base_x,base_y+150]); moving_beta=0.0
    for alp in np.arange(0.05,alpha_mx+.05,0.05):
        moving_beta = betafn(alp,effect,std)
        x1 = base_x+alp*150
        y1 = base_y+(moving_beta)*150
        draw.line((pt1[0],pt1[1],x1,y1))
        pt1 = np.array([x1,y1])
        pts.append((x1,y1))
        pts2.append((x1,y1))
    draw.polygon(pts,(255,20,147,50))
    draw.polygon(pts2,(0,102,255,50))

def betafn(alpha,effect,std):
    return norm.cdf(-effect+norm.isf(alpha,0,std),0,std)


effect = 50
std=30
im = Image.new("RGB", (512,512), "black")
draw = ImageDraw.Draw(im, 'RGBA')
draw_axes(draw)
draw_main_curve(draw, effect, std, alpha_mx=1)
im.show()

