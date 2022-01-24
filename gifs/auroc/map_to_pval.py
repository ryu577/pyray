import numpy as np
from scipy.stats import norm, cauchy
from PIL import Image, ImageDraw, ImageFont, ImageMath
from pyray.shapes.twod.paraboloid import *
from pyray.rotation import *
from pyray.imageutils import *
from pyray.axes import *
from pyray.shapes.oned.curve import draw_curve
from pyray.misc import zigzag2
from pyray.global_vars import *


font = ImageFont.truetype(font_loc, 12)
one_sided = False
for i in range(17):
    ix = zigzag2(i,0,10)
    im = Image.new("RGB", (512,512), "black")
    draw = ImageDraw.Draw(im, 'RGBA')
    
    if one_sided:
        fn = lambda x:300-norm.cdf(x,250,std)*100
    else:
        fn_tmp = lambda x:min(norm.cdf(x,250,std),norm.sf(x,250,std))
        fn = lambda x:300-(fn_tmp(x))*200
    draw_curve(fn, draw, rgba=(255,165,0))

    if one_sided:
        fn1 = lambda x:300-cauchy.cdf(x,250,std)*100
    else:
        fn_tmp1 = lambda x:min(cauchy.cdf(x,250,std),cauchy.sf(x,250,std))
        fn1 = lambda x:300-(fn_tmp1(x))*200
    draw_curve(fn1, draw, rgba=(222, 49, 99))

    draw.line((250,200,250,300),"white")
    draw.line((0,300,512,300),"yellow")
    y1 = 300
    x1 = 50+ix/10*(450-50)
    draw.ellipse((x1-3,y1-3,x1+3,y1+3),
                 outline=(255,255,0),
                 fill=(255,255,0,150))
    x2 = 250
    y1 = fn(x1)
    draw.ellipse((x2-3,y1-3,x2+3,y1+3),
                 outline=(255,165,0),
                 fill=(255,165,0,150))
    y1 = fn1(x1)
    draw.ellipse((x2-3,y1-3,x2+3,y1+3),
                 outline=(222,49,99),
                 fill=(222,49,99,150))
    #im = im.rotate(90)
    draw.text((217,183),"p_val",(255,255,255),font=font)
    draw.text((467,317),"t_stat",(255,255,0),font=font)
    
    draw.line((200,320,215,320),(255,165,0))
    draw.line((200,320+15,215,320+15),(222, 49, 99))
    draw.text((217,317),"Normal Tail fn",(255,165,0),font=font)
    draw.text((217,317+15),"Cauchy Tail fn",(222, 49, 99),font=font)
    im.save(basedir + 'im' + str(i) + '.png')

