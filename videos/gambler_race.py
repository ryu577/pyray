import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageMath
from pyray.rotation import *
from pyray.imageutils import *
from pyray.shapes.twod.paraboloid import *
from pyray.shapes.solid.polyhedron import *
from pyray.axes import *
from pyray.rotation import *
from pyray.axes import Path, ZigZagPath, draw_grid, draw_grey_grid
from pyray.misc import dist

basedir = '.\\Images\\RotatingCube\\'

class CreateGif(object):
	@staticmethod
	def scene1(write=True,ix=None):
		for i in range(11):
			im = draw_grid()
			draw = ImageDraw.Draw(im,'RGBA')
			pts = np.array([[0,0],[1,1],[5,-3]])
			pth = Path(pts)
			pth.zg.draw_lines(draw,i/10.0)
			if write:
				im.save(basedir + "im" + str(i) + ".png")

	@staticmethod
	def scene2():
		for i in range(11):
			im = draw_grid()
			draw = ImageDraw.Draw(im,'RGBA')
			pts = np.array([[0.,0.],[1.,1.],[5.,-3.]])
			pth = Path(pts,theta=np.pi*float(i)/10.0)
			pth.zg.draw_lines(draw,10.0/10.0)
			pth.refl_zg.draw_lines(draw,10.0/10.0)
			im.save(basedir + "im" + str(i) + ".png")

	@staticmethod
	def scene3():
		for i in range(11):
			im = draw_grid()
			draw = ImageDraw.Draw(im,'RGBA')
			pts = np.array([[0.,0.],[1.,1.],[5.,-3.]])
			pth = Path(pts)
			#pth.zg.draw_lines(draw,10.0/10.0)
			pth.refl_zg.draw_lines(draw,1.0,width=4)
			pts = np.array([[0,0],[1,-1],[2,0],[5,-3]])
			pth = Path(pts)
			pth.zg.draw_lines(draw,i/10.0)
			im.save(basedir + "im" + str(i) + ".png")

	@staticmethod
	def scene4():
		for i in range(11):
			im = draw_grid()
			draw = ImageDraw.Draw(im,'RGBA')
			pts = np.array([[0.,0.],[1.,1.],[5.,-3.]])
			pth = Path(pts)
			#pth.zg.draw_lines(draw,10.0/10.0)
			pth.refl_zg.draw_lines(draw,1.0,width=4)
			pts = np.array([[0.,0.],[1.,-1.],[2.,0.],[5.,-3.]])
			pth = Path(pts,theta=np.pi*i/10.0)
			pth.zg.draw_lines(draw,10.0/10.0,width=4)
			pth.refl_zg.draw_lines(draw,10.0/10.0)
			im.save(basedir + "im" + str(i) + ".png")

	@staticmethod
	def scene5():
		for i in range(11):
			im = draw_grid()
			draw = ImageDraw.Draw(im,'RGBA')
			pts = np.array([[0.,0.],[1.,1.],[5.,-3.]])
			pth = Path(pts)
			#pth.zg.draw_lines(draw,10.0/10.0)
			pth.refl_zg.draw_lines(draw,1.0,width=4)
			pts = np.array([[0.,0.],[1.,-1.],[2.,0.],[5.,-3.]])
			pth = Path(pts,theta=np.pi*10.0/10.0)
			#pth.zg.draw_lines(draw,10.0/10.0,width=4)
			pth.refl_zg.draw_lines(draw,10.0/10.0,width=4)
			pts = np.array([[0.,0.],[2.,-2.],[3.,-1.],[5.,-3.]])
			pth = Path(pts,theta=np.pi*i/10.0)
			pth.zg.draw_lines(draw,i/10.0)
			im.save(basedir + "im" + str(i) + ".png")

	@staticmethod
	def scene6():
		for i in range(11):
			im = draw_grid()
			draw = ImageDraw.Draw(im,'RGBA')
			pts = np.array([[0.,0.],[1.,1.],[5.,-3.]])
			pth = Path(pts)
			#pth.zg.draw_lines(draw,10.0/10.0)
			pth.refl_zg.draw_lines(draw,1.0,width=4)
			pts = np.array([[0.,0.],[1.,-1.],[2.,0.],[5.,-3.]])
			pth = Path(pts,theta=np.pi*10.0/10.0)
			#pth.zg.draw_lines(draw,10.0/10.0,width=4)
			pth.refl_zg.draw_lines(draw,10.0/10.0,width=4)
			pts = np.array([[0.,0.],[2.,-2.],[3.,-1.],[5.,-3.]])
			pth = Path(pts,theta=np.pi*i/10.0)
			#pth.zg.draw_lines(draw,10.0/10.0)
			pth.refl_zg.draw_lines(draw,10.0/10.0,width=7)
			im.save(basedir + "im" + str(i) + ".png")

	@staticmethod
	def scene7():
		for i in range(11):
			im = draw_grid()
			draw = ImageDraw.Draw(im,'RGBA')
			pts = np.array([[0.,0.],[1.,1.],[5.,-3.]])
			pth = Path(pts)
			#pth.zg.draw_lines(draw,10.0/10.0)
			pth.refl_zg.draw_lines(draw,1.0,width=4)
			pts = np.array([[0.,0.],[1.,-1.],[2.,0.],[5.,-3.]])
			pth = Path(pts,theta=np.pi*10.0/10.0)
			#pth.zg.draw_lines(draw,10.0/10.0,width=4)
			pth.refl_zg.draw_lines(draw,10.0/10.0,width=4)
			pts = np.array([[0.,0.],[2.,-2.],[3.,-1.],[5.,-3.]])
			pth = Path(pts,theta=np.pi*10.0/10.0)
			#pth.zg.draw_lines(draw,10.0/10.0)
			pth.refl_zg.draw_lines(draw,10.0/10.0,width=4)
			pts = np.array([[0.,0.],[3.,-3.]])
			pth = Path(pts,theta=np.pi*i/10.0)
			pth.zg.draw_lines(draw,i/10.0)
			im.save(basedir + "im" + str(i) + ".png")

	@staticmethod
	def scene8():
		for i in range(11):
			im = draw_grid()
			draw = ImageDraw.Draw(im,'RGBA')
			pts = np.array([[0.,0.],[1.,1.],[5.,-3.]])
			pth = Path(pts)
			#pth.zg.draw_lines(draw,10.0/10.0)
			pth.refl_zg.draw_lines(draw,1.0,width=4)
			pts = np.array([[0.,0.],[1.,-1.],[2.,0.],[5.,-3.]])
			pth = Path(pts,theta=np.pi*10.0/10.0)
			#pth.zg.draw_lines(draw,10.0/10.0,width=4)
			pth.refl_zg.draw_lines(draw,10.0/10.0,width=4)
			pts = np.array([[0.,0.],[2.,-2.],[3.,-1.],[5.,-3.]])
			pth = Path(pts,theta=np.pi*10.0/10.0)
			#pth.zg.draw_lines(draw,10.0/10.0)
			pth.refl_zg.draw_lines(draw,10.0/10.0,width=4)
			pts = np.array([[0.,0.],[3.,-3.]])
			pth = Path(pts,theta=np.pi*i/10.0)
			#pth.zg.draw_lines(draw,i/10.0)
			pth.refl_zg.draw_lines(draw,10.0/10.0,width=7)
			im.save(basedir + "im" + str(i) + ".png")


