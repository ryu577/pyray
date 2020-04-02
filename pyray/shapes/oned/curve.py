import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageMath
from scipy.stats import norm


def draw_curve(fn, draw,rgba=(250,255,0)):
    x = 0
    eps=1.0
    for _ in range(1000):
        pt1 = np.array([x,fn(x)])
        pt2 = np.array([x+eps,fn(x+eps)])
        x=x+eps
        draw.line((pt1[0],pt1[1],pt2[0],pt2[1]),fill=rgba,width=1)


