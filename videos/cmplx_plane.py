import numpy as np
from scipy.stats import norm

from pyray.misc import zigzag2
from pyray.shapes.oned.curve import *

from pyray.shapes.twod.plot import *
from pyray.shapes.oned.circle import draw_circle_x_y, generalized_arc


def make_circle():
	for ii in range(10):
		theta = -np.pi*2*ii/9
		im=Image.new("RGB", (512, 512), (256,256,256))
		draw=ImageDraw.Draw(im,'RGBA')
		mc = MapCoord(im_size=np.array([512,512]),origin=np.array([4,4]))
		cnv = Canvas(mc, im=im, draw=draw)
		cnv.draw_grid()
		cnv.draw_2d_arrow(np.array([-4,0]), np.array([4,0]))
		cnv.draw_2d_arrow(np.array([0,4]), np.array([0,-4]))
		#cnv.draw_2d_line(np.array([-4,-4]),np.array([4,4]),rgba="purple")
		#cnv.draw_2d_line(np.array([4,-4]),np.array([-4,4]),rgba="yellow")

		pt1 = np.array([np.cos(theta), np.sin(theta)])
		pt2 = np.array([np.cos(theta), -np.sin(theta)])

		cnv.draw_2d_arrow(np.array([0,0]), pt1)
		cnv.draw_point(pt2, fill=(220,150,10,180))
		prcnt = theta/2/np.pi
		generalized_arc(draw, np.eye(3), np.array([0,0,1]),
			            point=np.array([.5,0,0]),
						scale=mc.scale, shift=np.array([256, 256,0]),
						prcnt=prcnt, width=1)
		#cnv.draw_point(np.array([1,1]),fill="green")
		#cnv.write_txt((1,1),"(1,1)","green")
		#cnv.write_txt((-1,-1),"(-1,-1)","red")

		mc.plot_to_im(0,0)
		draw_circle_x_y(cnv.draw, np.eye(3), radius=1, shift=np.array([256-mc.scale, 
					    256-mc.scale,0]), scale=mc.scale,
						arcExtent=360.0, width=1, start=np.array([0,1,0]), 
						rgba="grey")
		basedir = './Images/RotatingCube/'
		cnv.im.save(basedir + "im" + str(ii) + ".png")


def halving_lemma():
	for ii in range(30):
		im=Image.new("RGB", (512, 512), (256,256,256))
		draw=ImageDraw.Draw(im,'RGBA')
		mc = MapCoord(im_size=np.array([512,512]),origin=np.array([4,4]))
		cnv = Canvas(mc, im=im, draw=draw)
		cnv.draw_grid()
		cnv.draw_2d_arrow(np.array([-4,0]), np.array([4,0]))
		cnv.draw_2d_arrow(np.array([0,4]), np.array([0,-4]))

		for jj in range(8):
			theta = -np.pi*2*jj/8*(1+ii/29.0)
			pt1 = np.array([np.cos(theta), np.sin(theta)])
			pt2 = np.array([np.cos(theta), -np.sin(theta)])

			cnv.draw_2d_arrow(np.array([0,0]), pt1, rgba=(50,50,50,50))
			cnv.draw_point(pt2, fill=(int(220*jj/7.0),150,10,180))

		mc.plot_to_im(0,0)
		draw_circle_x_y(cnv.draw, np.eye(3), radius=1,
						shift=np.array([256-mc.scale,
					    256-mc.scale,0]), scale=mc.scale,
						arcExtent=360.0, width=1, 
						start=np.array([0,1,0]),
						rgba="grey")
		basedir = './Images/RotatingCube/'
		cnv.im.save(basedir + "im" + str(ii) + ".png")

