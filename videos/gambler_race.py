import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageMath
from pyray.rotation import *
from utils.imageutils import *
from functions.functionalforms import *
from pyray.shapes.polyhedron import *
from pyray.axes import *
from pyray.rotation import *

#basedir = '..\\images\\RotatingCube\\'
basedir = '.\\images\\RotatingCube\\'

def draw_grid(ix, max_ix, im=Image.new("RGB", (1024, 1024), (255,255,255))):
	draw = ImageDraw.Draw(im,'RGBA')
	#drawXYGrid(draw, r, meshLen=1.0, scale=300, shift=np.array([1000,1000,0]))
	scale = 64
	#The origin coordinates should be divisible by the scale.
	origin = np.array([scale*4,scale*10])
	r = general_rotation(np.array([0,0,1]),np.pi/0.5)[:2,:2]
	writeLatex(im, "\\kappa", (200,50))
	## Draw the base grid.
	for i in np.arange(-64, 1154, scale):
		pt1 = np.dot(r,np.array([i,-64])-origin) + origin
		pt2 = np.dot(r,np.array([i,1154])-origin) + origin
		draw.line((pt1[0],pt1[1],pt2[0],pt2[1]), fill=(220,100,5,120), width=1)
		pt1 = np.dot(r,np.array([-64,i])-origin) + origin
		pt2 = np.dot(r,np.array([1154,i])-origin) + origin
		draw.line((pt1[0],pt1[1],pt2[0],pt2[1]), fill=(220,100,5,120), width=1)

	## Draw the axes.
	#arrowV1(draw, np.eye(3), np.array([0,-0.8,0]), np.array([0,0.8,0]), rgb=(0,255,0), scale=100, shift=np.array([500,500,0]))
	#arrowV1(draw, np.eye(3), np.array([-0.8,0,0]), np.array([0.8,0,0]), rgb=(0,255,0), scale=100, shift=np.array([500,500,0]))
	draw_2d_arrow(draw, r, np.array([-3,0]), np.array([12,0]),rgba="red",width=3)
	draw_2d_arrow(draw, r, np.array([0,-3]), np.array([0,-10]),rgba="red",width=3)
	pt1 = np.dot(r,np.array([origin[0],0])-origin) + origin
	pt2 = np.dot(r,np.array([origin[0],1024])-origin) + origin
	draw.line((pt1[0],pt1[1],pt2[0],pt2[1]), fill=(255,70,20,255), width=7)

	pt1 = np.dot(r,np.array([0,origin[1]])-origin) + origin
	pt2 = np.dot(r,np.array([1024, origin[1]])-origin) + origin
	draw.line((pt1[0],pt1[1],pt2[0],pt2[1]), fill=(255,70,20,255), width=7)

	## Draw the grey grid.
	draw_grey_grid(draw, r, end_pt=np.array([6,-2]))
	draw_grey_grid(draw, r, start_pt = np.array([0,-6]),end_pt=np.array([4,-4]))

	pt = np.dot(r,np.array([6, -2]))*scale + origin
	draw.ellipse((pt[0]-8, pt[1]-8, pt[0]+8, pt[1]+8), fill = (255,0,0,150), outline = (0,0,0))
	## Draw the purple target line From the top.
	pt1 = np.dot(r,np.array([-scale,origin[1]-3*scale])-origin) + origin
	pt2 = np.dot(r,np.array([1154,origin[1]-3*scale])-origin) + origin
	draw.line((pt1[0],pt1[1],pt2[0],pt2[1]), fill=(148,0,211,255), width=4)

	#Draw solid orange line.
	pt1 = np.dot(r,np.array([2, -2]))*scale + origin
	pt2 = np.dot(r,np.array([6, -2]))*scale + origin
	draw.line((pt1[0],pt1[1],pt2[0],pt2[1]), fill=(255,165,0), width=8)

	pt1 = np.dot(r,np.array([3, -3]))*scale + origin
	pt2 = np.dot(r,np.array([5, -3]))*scale + origin
	draw.line((pt1[0],pt1[1],pt2[0],pt2[1]), fill=(128,0,128,150), width=8)

	pt = np.dot(r,np.array([0, -6]))*scale + origin
	draw.ellipse((pt[0]-8, pt[1]-8, pt[0]+8, pt[1]+8), fill = (30,144,255,250), outline = (0,0,0))
	draw_2d_arrow(draw, r, np.array([-3,3]), np.array([9,-9]))
	draw_2d_arrow(draw, r, np.array([-3,-3]), np.array([5,5]))

	y1=0
	pt1 = np.dot(r,np.array([0, y1]))*scale + origin
	y2=1
	pt2 = np.dot(r,np.array([1, y2]))*scale + origin
	y3=-3
	pt3 = np.dot(r,np.array([5, y3]))*scale + origin

	y1_ref = refl_abt_horizntl(y1)
	pt1_ref = np.dot(r,np.array([0, y1_ref]))*scale + origin
	y2_ref = refl_abt_horizntl(y2)
	pt2_ref = np.dot(r,np.array([1, y2_ref]))*scale + origin
	y3_ref = refl_abt_horizntl(y3)
	pt3_ref = np.dot(r,np.array([5, y3_ref]))*scale + origin

	#draw.line((pt1[0],pt1[1],pt2[0],pt2[1]), fill="yellow", width=8)
	#draw.line((pt1_ref[0],pt1_ref[1],pt2_ref[0],pt2_ref[1]), fill="yellow", width=8)
	zg = ZigZagPath(np.array([pt1, pt2, pt3]))
	zg.draw_lines(draw, prop_dist=ix/max_ix)
	zg = ZigZagPath(np.array([pt1_ref, pt2_ref, pt3_ref]))
	zg.draw_lines(draw, prop_dist=ix/max_ix)
	im.save(basedir + "im" + str(ix) + ".png")


class ZigZagPath(object):
	def __init__(self, points):
		self.points = points
		self.distances = []
		for i in range(len(self.points)-1):
			self.distances.append(dist(self.points[i], self.points[i+1]))
		self.distances = np.array(self.distances)

	def draw_lines(self, draw, prop_dist=1.0):
		remaining_dist = sum(self.distances)*prop_dist
		total_dist = remaining_dist
		for i in range(len(self.distances)):
			if remaining_dist < self.distances[i]:
				pp = float(remaining_dist/self.distances[i])
				pt1 = self.points[i]
				pt2 = self.points[i+1]
				pt2 = pp*pt2+(1-pp)*pt1
				draw.line((pt1[0], pt1[1], pt2[0], pt2[1]), fill=(255,250,204), width=3)
				break
			else:
				pt1 = self.points[i]
				pt2 = self.points[i+1]
				draw.line((pt1[0], pt1[1], pt2[0], pt2[1]), fill=(255,250,204), width=3)
				remaining_dist -= self.distances[i]


def dist(pt1, pt2):
	return np.sqrt(sum((pt2-pt1)**2))


def refl_abt_horizntl(y, y_ref=-3):
	delta = (y_ref-y)
	return y+2*delta

def draw_grey_grid(draw, r, start_pt=np.array([0,0]), end_pt=np.array([7,-3]), \
					origin=np.array([4*64,10*64]), scale=64):
	vec = (end_pt - start_pt)
	up_ext = np.array([int((vec[0]+vec[1])/2), int((vec[0]+vec[1])/2)])
	down_ext = np.array([int((vec[0]-vec[1])/2), int((-vec[0]+vec[1])/2)])
	for i in range(abs(int(up_ext[0]))+1):
		pt1 = np.dot(r,np.array([i, i])+start_pt)*scale + origin
		pt2 = np.dot(r,np.array([i, i])+down_ext+start_pt)*scale + origin
		draw.line((pt1[0],pt1[1],pt2[0],pt2[1]), fill="grey", width=2)
	##
	for i in range(abs(int(down_ext[0]))+1):
		pt1 = np.dot(r,np.array([i, -i])+start_pt)*scale + origin
		pt2 = np.dot(r,np.array([i, -i])+up_ext+start_pt)*scale + origin
		draw.line((pt1[0],pt1[1],pt2[0],pt2[1]), fill="grey", width=2)


def draw_2d_arrow(draw, r, start_pt=np.array([0,0]),
					end_pt=np.array([7,-3]), \
					origin=np.array([4*64,10*64]), scale=64, rgba="grey",
					width=2):
	pt1 = np.dot(r,start_pt)*scale + origin
	pt2 = np.dot(r,end_pt)*scale + origin
	draw.line((pt1[0],pt1[1],pt2[0],pt2[1]), fill=rgba, width=width)
	vec = (pt2-pt1)
	vec = vec/np.sqrt(sum(vec**2))/2
	r1 = planar_rotation(5*np.pi/4)
	arrow_foot = np.dot(r1,vec)*scale + pt2
	draw.line((arrow_foot[0],arrow_foot[1],pt2[0],pt2[1]), fill=rgba, width=width)
	r1 = planar_rotation(3*np.pi/4)
	arrow_foot = np.dot(r1,vec)*scale + pt2
	draw.line((arrow_foot[0],arrow_foot[1],pt2[0],pt2[1]), fill=rgba, width=width)


def draw_coin():
	verts = 15
	width= 2
	polygon = np.array([[3*np.cos(2*np.pi/verts*n), 3*np.sin(2*np.pi/verts*n),1] for n in np.arange(1,verts+1)])
	planes = [polygon]
	for j in range(verts):
		poly = [polygon[j], polygon[(j+1)%verts], \
			polygon[(j+1)%verts]-np.array([0,0,width]), polygon[(j)]-np.array([0,0,width])]
		planes.append(poly)
	planes.append(polygon+np.array([0,0,-width]))
	for ii in range(20):
		im = Image.new("RGB", (1024, 1024), (1,1,1))
		draw = ImageDraw.Draw(im,'RGBA')
		r = general_rotation(np.array([0,1,0]),2*np.pi/20*ii)
		render_solid_planes(planes, draw, r, shift=np.array([512, 512, 0]), scale=75)
		im.save(basedir + "im" + str(ii) + ".png")


