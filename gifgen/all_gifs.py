import numpy as np
from rotation.rotation import *
from PIL import Image, ImageDraw, ImageFont, ImageMath


#j = 4 + 46/3.0; im_ind = 0; draw1 = None
def best_direction(j=19.5, im_ind=0, scale=250, shift=np.array([1200,580,0]), draw1=None):
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



