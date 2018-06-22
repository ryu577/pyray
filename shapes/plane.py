import numpy as np
from rotation.rotation import *
from PIL import Image, ImageDraw, ImageFont, ImageMath

def xzplane(draw, r, y, shift = np.array([1000, 1000, 0, 0]), scale = 300):
    """
    Draws an x-z plane on the draw object of an image.
    """
    extent = 2.8
    pln = np.array(
            [
                [-extent,y,0],
                [extent,y,0],
                [extent,y,extent*2],
                [-extent,y,extent*2]
            ]
        )
    pln = np.dot(pln, np.transpose(r))
    pln = pln * scale + shift[:3]
    draw.polygon([(pln[0][0],pln[0][1]),(pln[1][0],pln[1][1]),(pln[2][0],pln[2][1]),(pln[3][0],pln[3][1])], (0,102,255,70))


def xyplane(draw, r, x, shift = np.array([1000, 1000, 0, 0]), scale = 300):
    """
    Draws an x-y plane on the draw object of an image.
    """
    extent = 2.8
    pln = np.array(
            [
                [x,-extent,0],
                [x,extent,0],
                [x,extent,extent*2],
                [x,-extent,extent*2]
            ]
        )
    pln = np.dot(pln,np.transpose(r))
    pln = pln * scale + shift[:3]
    draw.polygon([(pln[0][0],pln[0][1]),(pln[1][0],pln[1][1]),(pln[2][0],pln[2][1]),(pln[3][0],pln[3][1])], (0,102,255,70))


def arrow_w_projection(im, draw, r, pt_1, pt_2, shift = np.array([1000, 1000, 0, 0]), 
                       scale=250, pt_proj = None, plane = np.array([2.5,2.5,-2.5])*410.0/200.0):
    [a,b,c] = plane    
    z_pt_3 = c * (1 - pt_2[0]/a - pt_2[1]/b)
    pt_3 = np.array([pt_2[0], pt_2[1], z_pt_3])
    pt_3_big = np.dot(r, np.array([pt_2[0], pt_2[1], z_pt_3])) * scale + shift[:3]
    pt_2_big = np.dot(r, pt_2) * scale + shift[:3]
    pt_1_big = np.dot(r, pt_1) * scale + shift[:3]
    draw.polygon(((pt_1_big[0],pt_1_big[1]),(pt_2_big[0],pt_2_big[1]),(pt_3_big[0],pt_3_big[1])), (204,102,255,120))
    if pt_proj is not None:
        pt_proj_big = np.dot(r, pt_proj) * scale + shift[:3]
        draw.line((pt_1_big[0], pt_1_big[1], pt_proj_big[0], pt_proj_big[1]), fill = 'pink', width = 7)
        draw.line((pt_2_big[0], pt_2_big[1], pt_proj_big[0], pt_proj_big[1]), fill = 'pink', width = 7)


