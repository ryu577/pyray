import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageMath
from pyray.axes import render_scene_4d_axis

from pyray.rotation import *
from pyray.axes import drawXYGrid, arrowV1
from pyray.shapes.oned.circle import draw_circle_x_y, project_circle_on_plane


def rotated_xz_plane(draw, r, r2, scale=200, shift=np.array([1000,1000,0]), translate=np.array([0,0,0])):
    '''
    Takes an x-z plane, translates it by translate parameter, rotates it by r2 and draws it.
    params:
        r: The amount by which the object our plane is cutting is already rotated.
        r2: The amount by which the plane is to be rotated on top of r.
        translate: The amount by which the center of the plane is to be moved.
    '''
    extent = 2.8
    pln = np.array(
            [
                [-extent,0,0],
                [extent,0,0],
                [extent,0,extent*2],
                [-extent,0,extent*2]
            ]
        )
    pln = np.array([i-translate for i in pln]) # translate every point on the plane.
    rr = np.dot(r,r2)
    pln = np.dot(pln, np.transpose(rr))
    pln = np.array([i + np.dot(r,translate) for i in pln])
    pln = pln * scale + shift[:3]
    draw.polygon([(pln[0][0],pln[0][1]),(pln[1][0],pln[1][1]),(pln[2][0],pln[2][1]),(pln[3][0],pln[3][1])], (204,0,255,70))


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



#j = 4 + 46/3.0; im_ind = 0; draw1 = None
def best_plane_direction(j=19.5, im_ind=0, scale=250, shift=np.array([1200,580,0]), draw1=None):
    font = ImageFont.truetype("arial.ttf", 75)
    # For the axes.
    [a,b,c] = np.array([2.5, 2.5, -2.5]) * 410 / 200

    ## Rotation matrices.
    r = rotation(3, 2 * np.pi*j/30.0)
    r1 = np.eye(4)
    r1[:3,:3] = r

    ## Image objects.
    if draw1 is None:
        im = Image.new("RGB", (2048, 2048), "black")
        draw = ImageDraw.Draw(im, 'RGBA')
    else:
        draw = draw1

    ## Create the axes.
    render_scene_4d_axis(draw, r1, 4, scale = scale, shift = shift)
    pt1 = np.dot(r,np.array([a,0,0])) * scale + shift[:3]
    pt2 = np.dot(r,np.array([0,b,0])) * scale + shift[:3]
    pt3 = np.dot(r,np.array([0,0,c])) * scale + shift[:3]

    ## The point where this plane extends.
    pt4 = np.dot(r,np.array([a,b,-c])) * scale + shift[:3]

    draw.line((pt1[0],pt1[1],pt2[0],pt2[1]), fill=(200,80,100), width = 3)
    draw.line((pt1[0],pt1[1],pt2[0],pt2[1]), fill='orange', width = 3)

    draw.polygon([(pt1[0],pt1[1]),(pt3[0],pt3[1]),(pt2[0],pt2[1])], (200,80,100,100))
    draw.polygon([(pt1[0],pt1[1]),(pt4[0],pt4[1]),(pt2[0],pt2[1])], (200,80,100,120))
    draw.line((shift[0],shift[1],pt3[0],pt3[1]), fill = "yellow", width=7)
    draw.line((shift[0],shift[1],pt1[0],pt1[1]), fill = "yellow", width=7)
    draw.line((shift[0],shift[1],pt2[0],pt2[1]), fill = "yellow", width=7)

    ## Draw the x-y grid.
    drawXYGrid(draw, r, 1.25, scale = scale, shift = shift)

    ## We start at 45 degrees and trace a circular arc from there.
    pt_1 = np.array([a/2.0, b/2.0, 0])
    arxExt = int(180*im_ind/10.0)
    draw_circle_x_y(draw=draw, r = r, center=pt_1[:2], radius=1, start = np.array([1/np.sqrt(2), 1/np.sqrt(2), 0]), arcExtent = arxExt, scale = scale, shift=shift)
    project_circle_on_plane(draw=draw, r = r, center=pt_1[:2], radius=1, plane = np.array([a,b,c]), 
        start = np.array([1/np.sqrt(2), 1/np.sqrt(2), 0]), arcExtent=arxExt, scale = scale, shift = shift)

    ## Draw a point right at the center of the orange line.
    pt = np.dot(r, pt_1)*scale + shift[:3]
    width = 10
    draw.ellipse((pt[0]-width,pt[1]-width,pt[0]+width,pt[1]+width),fill=(102,255,51))

    # We start at 45 degrees and trace a circular arc from there.
    theta = np.arctan(a/b) + np.pi*im_ind/10.0
    pt_2 = pt_1 + 1.0 * np.array([np.cos(theta), np.sin(theta), 0])
    arrowV1(draw, r, pt_1, pt_2, scale = scale, shift = shift)

    ## Draw a pink triangle with vertices: head of arrow, tail of arrow, projection on plane.
    arrow_w_projection(im, draw, r, pt_1, pt_2, plane = np.array([a,b,c]))

    ## If you didn't provide the draw object, we will save the image.
    if draw1 is None:
        im.save('.\\im' + str(im_ind) + '.png')


