import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageMath
from pyray.shapes.polyhedron import *
from pyray.axes import *
from pyray.rotation import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

basedir = '..\\images\\RotatingCube\\'
a = np.array([1,0])
b = np.array([-1,0])
midd = (a+b)/2

perpend = np.dot(planar_rotation(np.pi/2),(a-b))
p = 0.8
c = midd + p*perpend

perpendicular = np.sqrt(sum((c-midd)**2))
base = np.sqrt(sum((a-midd)**2))

## The two equal angles of the isocoloes triangle used to form the quadrilateral.
theta = np.arctan(perpendicular/base)

## The angle between the two equal sides of the quadrilateral.
theta1 = 2*(np.pi/2-theta)

## The rotation needed to convert mesh plot to solid.
phi = np.arccos((np.cos(theta1)**2-np.cos(theta1))/np.sin(theta1)**2)

##################################################


scale=300
shift = np.array([1000,1000,0])
x = 0.0
pt1 = np.array([0,0,0])
pt2 = np.array([1,0,0])
pt3 = np.array([1+x/np.sqrt(2),1+x/np.sqrt(2),0])
pt4 = np.array([0,1,0])
face1 = np.array([pt1,pt2,pt3,pt4]) - np.array([.5,.5,.5])
face1 = face1*scale
r = general_rotation(np.array([1,1,1]),np.pi/6)
face1 = np.dot(face1,r)

basedir = '..\\images\\RotatingCube\\'
poly = [(i[0]+1000, i[1]+1000) for i in face1]

for i in range(31):
	im = Image.new("RGB", (2048, 2048), (1,1,1))
	draw = ImageDraw.Draw(im,'RGBA')
	r_diag = general_rotation(np.array([1,1,1]),-np.pi/15*i)
	face2 = np.dot(face1, r_diag)
	draw.polygon(poly, fill=(255,255,255,150))
	poly2 = [(i[0]+shift[0], i[1]+shift[1]) for i in face2]
	draw.polygon(poly2, fill=(255,255,255))
	im.save(basedir + "im" + str(i) + ".png")


