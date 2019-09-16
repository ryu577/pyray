import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageMath
from pyray.axes import *
from pyray.rotation import *
from pyray.shapes.twod.paraboloid import *
from pyray.shapes.twod.functional import *
from pyray.axes import Path, ZigZagPath, draw_grid, draw_grey_grid
from pyray.misc import dist
from pyray.shapes.twod.plot import *


def draw_base_diagram(origin=np.array([8,8])):
	im = Image.new("RGB", (1024, 1024), (0,0,0))
	draw = ImageDraw.Draw(im,'RGBA')
	scale = 64
	#The origin coordinates should be divisible by the scale.
	origin = np.array([scale*origin[0],scale*origin[1]])
	r = general_rotation(np.array([.11,1,0]),np.pi/0.5)[:2,:2]
	## Draw the base grid.
	for i in np.arange(-64, 1154, scale):
		pt1 = np.dot(r,np.array([i,-64])-origin) + origin
		pt2 = np.dot(r,np.array([i,1154])-origin) + origin
		draw.line((pt1[0],pt1[1],pt2[0],pt2[1]), 
                    fill=(120,120,120,120), width=2)
		pt1 = np.dot(r,np.array([-64,i])-origin) + origin
		pt2 = np.dot(r,np.array([1154,i])-origin) + origin
		draw.line((pt1[0],pt1[1],pt2[0],pt2[1]), 
                    fill=(120,120,120,120), width=2)
	## Draw the axes.
	Canvas.draw_2d_arrow_s(draw, r, np.array([-8,0]), np.array([8,0]),
                    scale=scale,rgba="grey",width=3,origin=origin)
	Canvas.draw_2d_arrow_s(draw, r, np.array([0,8]), np.array([0,-8]),
                    scale=scale,rgba="grey",width=3,origin=origin)
	pt1 = np.dot(r,np.array([origin[0],0])-origin) + origin
	pt2 = np.dot(r,np.array([origin[0],1024])-origin) + origin
	#draw.line((pt1[0],pt1[1],pt2[0],pt2[1]), fill=(255,70,20,255), width=7)

	pt1 = np.dot(r,np.array([0,origin[1]])-origin) + origin
	pt2 = np.dot(r,np.array([1024, origin[1]])-origin) + origin
	#draw.line((pt1[0],pt1[1],pt2[0],pt2[1]), fill=(255,70,20,255), width=7)

	## Draw the grey grid.
	#draw_grey_grid(draw, r, end_pt=np.array([6,-2]))
	
	pt = np.dot(r,np.array([6, -2]))*scale + origin
	#draw.ellipse((pt[0]-8, pt[1]-8, pt[0]+8, pt[1]+8), fill = (255,0,0,150), outline = (0,0,0))
	## Draw the purple target line From the top.
	pt1 = np.dot(r,np.array([-scale,origin[1]-3*scale])-origin) + origin
	pt2 = np.dot(r,np.array([1154,origin[1]-3*scale])-origin) + origin
	#draw.line((pt1[0],pt1[1],pt2[0],pt2[1]), fill=(148,0,211,255), width=4)

	#Draw solid orange line.
	pt1 = np.dot(r,np.array([2, -2]))*scale + origin
	pt2 = np.dot(r,np.array([6, -2]))*scale + origin
	#draw.line((pt1[0],pt1[1],pt2[0],pt2[1]), fill=(255,165,0), width=8)

	pt1 = np.dot(r,np.array([3, -3]))*scale + origin
	pt2 = np.dot(r,np.array([5, -3]))*scale + origin
	#draw.line((pt1[0],pt1[1],pt2[0],pt2[1]), fill=(128,0,128,150), width=8)

	pt = np.dot(r,np.array([0, 0]))*scale + origin
	#draw.ellipse((pt[0]-8, pt[1]-8, pt[0]+8, pt[1]+8), fill = (30,144,255,250), outline = (0,0,0))
	pt = np.dot(r,np.array([1, -1]))*scale + origin
	draw.ellipse((pt[0]-8, pt[1]-8, pt[0]+8, pt[1]+8), 
            fill = (25,255,25,250), outline = (0,0,0))
	pt = np.dot(r,np.array([-1, 1]))*scale + origin
	draw.ellipse((pt[0]-8, pt[1]-8, pt[0]+8, pt[1]+8), 
            fill = (255,25,25,250), outline = (0,0,0))
	## The grey grid arrows.
    #draw_2d_arrow(draw, r, np.array([-3,3]), np.array([9,-9]))
	#draw_2d_arrow(draw, r, np.array([-3,-3]), np.array([5,5]))
	Canvas.draw_2d_line_s(draw, r, np.array([8,8]), np.array([-8,-8]),
                    scale=scale,rgba="purple",width=5,origin=origin)
	Canvas.draw_2d_line_s(draw, r, np.array([8,-8]), np.array([-8,8]),
                    scale=scale,rgba=(250,250,0,150),width=2,origin=origin)
	font = ImageFont.truetype("arial.ttf", 18)
	pos = MapCoord.plot_to_im_s(1,1,np.array([8,8]),scale=64)
	draw.text(pos, "(1,1)", (25,255,25), font=font)
	pos = MapCoord.plot_to_im_s(-1,-1,np.array([8,8]),scale=64)
	draw.text(pos, "(-1,-1)", (255,25,25), font=font)
	return im


basedir = '.\\images\\RotatingCube\\'

im = draw_base_diagram()
im.save(basedir + "im" + str(0) + ".png")

