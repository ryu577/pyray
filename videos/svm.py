import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageMath
from pyray.axes import *
from pyray.rotation import *
from pyray.shapes.twod.paraboloid import *
from pyray.shapes.twod.functional import *
from pyray.axes import Path, ZigZagPath, draw_grid, draw_grey_grid
from pyray.misc import dist
from pyray.shapes.twod.plot import *
from pyray.misc import zigzag2
from pyray.rotation import planar_rotation


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

def tst():
	basedir = '.\\images\\RotatingCube\\'
	im = draw_base_diagram()
	im.save(basedir + "im" + str(0) + ".png")

##############################################################

def tst_2d_random_plot(draw_sep_line=True,idx=0,yellow_ext=0,writestuff=True):
    np.random.seed(0)
    mc = MapCoord(im_size=np.array([512,512]),origin=np.array([4,4]))
    cnv = Canvas(mc)
    cnv.draw_grid()
    cnv.draw_2d_arrow(np.array([-4,0]), np.array([4,0]))
    cnv.draw_2d_arrow(np.array([0,4]), np.array([0,-4]))
    if draw_sep_line:
        eps = zigzag2(idx,0,5,-5)/5
        cnv.draw_2d_line(np.array([-4,-4-eps]),np.array([4,4+eps]),rgba="purple")
    for _ in range(50):
        pt = 4*np.random.uniform(size=2)-2.0
        if np.random.uniform()>0.2 and abs(pt[0]+pt[1])>.3:
            if sum(pt)>0.1:
                cnv.draw_point(pt,fill="green",size=4)
            elif sum(pt)<-0.1:
                cnv.draw_point(pt,fill="red",size=4)
        else:
            #cnv.draw_point(pt,fill="yellow",size=4)
            if sum(pt)>0.1:
                cnv.draw_point(pt,fill=(255-yellow_ext*10,255,0),size=4)
            elif sum(pt)<-0.1:
                cnv.draw_point(pt,fill=(255,255-yellow_ext*10,0),size=4)
    if writestuff:
        font = ImageFont.truetype("arial.ttf", 18)
        cnv.draw.text((338,362), "critical point", (255,0,0), font=font)
        cnv.draw.text((151,132), "flips label", (255,255,0), font=font)
    basedir = '.\\images\\RotatingCube\\'
    cnv.im.save(basedir + "im" + str(idx) + ".png")


##Fig 1: Without purple line 
tst_2d_random_plot(False)

##Fig 2: With purple line
tst_2d_random_plot(True)


for i in range(10):
	tst_2d_random_plot(idx=i,yellow_ext=0)


def eqn_of_line(idx=0, r=planar_rotation(np.pi*3/20.0)):
    mc = MapCoord(im_size=np.array([512,512]),origin=np.array([4,4]))
    cnv = Canvas(mc)
    cnv.draw_grid()
    cnv.draw_2d_arrow(np.array([-4,0]), np.array([4,0]))
    cnv.draw_2d_arrow(np.array([0,4]), np.array([0,-4]))
    cnv.draw_2d_arrow(np.array([0,0]), np.array([0,-2]),rgba="orange",r=r)
    cnv.draw_2d_arrow(np.array([-4,0]), np.array([4,0]),rgba="grey",r=r)
    basedir = '.\\images\\RotatingCube\\'
    cnv.im.save(basedir + "im" + str(idx) + ".png")

for i in range(10):
	eqn_of_line(i,r=planar_rotation(2*np.pi*i/10.0))


def scaling_w(idx=0, r=planar_rotation(np.pi*3/20.0)):
    mc = MapCoord(im_size=np.array([512,512]),origin=np.array([4,4]))
    cnv = Canvas(mc)
    cnv.draw_grid()
    cnv.draw_2d_arrow(np.array([-4,0]), np.array([4,0]))
    cnv.draw_2d_arrow(np.array([0,4]), np.array([0,-4]))
    eps = zigzag2(idx,0,5,-5)/5
    cnv.draw_2d_arrow(np.array([0,0]), np.array([0,-2*(1+eps)]),rgba="orange",r=r)
    cnv.draw_2d_arrow(np.array([-4,0]), np.array([4,0]),rgba="white",r=r)
    basedir = '.\\images\\RotatingCube\\'
    cnv.im.save(basedir + "im" + str(idx) + ".png")

for i in range(10):
	scaling_w(i,r=planar_rotation(2*np.pi*3.4/10.0))


def proof_eqn_line(idx, r=planar_rotation(np.pi*3/20.0)):
    mc = MapCoord(im_size=np.array([512,512]),origin=np.array([4,4]))
    cnv = Canvas(mc)
    cnv.draw_grid()
    cnv.draw_2d_arrow(np.array([-4,0]), np.array([4,0]))
    cnv.draw_2d_arrow(np.array([0,4]), np.array([0,-4]))
    cnv.draw_point(np.array([0,0]),fill="yellow",size=5)
    cnv.write_txt(np.array([0,0]),"O",(255,255,0,200))
    pt1=np.array([-1,4])
    pt2=np.array([3,-2])
    l = Line(pt1,pt2)
    cnv.draw_line(pt1, pt2,fill="purple")
    cnv.draw_line(np.array([0,0]), l.closest_pt_from_origin*5,fill="white",width=1)
    cnv.draw_point(l.closest_pt_from_origin,fill="blue",size=4)
    cnv.draw_arrow(np.array([0,0]), l.closest_pt_from_origin*.6,\
				fill="blue",width=3,arr_bk=.9,arr_per=.1)
    cnv.write_txt(l.closest_pt_from_origin+np.array([.1,.1]),"A","blue")
    arb_pt_1 = pt1*.2+pt2*.8
    arb_pt_2 = pt1*.9+pt2*.1
    cnv.draw_point(arb_pt_1,fill=(3, 252, 53),size=4)
    cnv.draw_point(arb_pt_2,fill=(252, 144, 3),size=4)
    cnv.draw_arrow(np.array([0,0]), arb_pt_1,\
				fill=(3, 252, 53),width=1,arr_bk=.9,arr_per=.1)
    cnv.draw_arrow(np.array([0,0]), arb_pt_2,\
				fill=(252, 144, 3),width=1,arr_bk=.9,arr_per=.1)
    cnv.write_txt(arb_pt_1+np.array([.1,.1]),"B",(3, 252, 53))
    cnv.write_txt(arb_pt_2+np.array([.1,.1]),"C",(252, 144, 3))
    basedir = '.\\images\\RotatingCube\\'
    cnv.im.save(basedir + "im" + str(idx) + ".png")


def proof_perpend_dist(idx, r=planar_rotation(np.pi*3/20.0)):
    mc = MapCoord(im_size=np.array([512,512]),origin=np.array([4,4]))
    cnv = Canvas(mc)
    cnv.draw_grid()
    cnv.draw_2d_arrow(np.array([-4,0]), np.array([4,0]))
    cnv.draw_2d_arrow(np.array([0,4]), np.array([0,-4]))
    cnv.draw_point(np.array([0,0]),fill="yellow",size=5)
    cnv.write_txt(np.array([0,0]),"O",(255,255,0,200))
    pt1=np.array([-1,4])
    pt2=np.array([3,-2])
    l = Line(pt1,pt2)
    cnv.draw_line(pt1, pt2,fill="purple")
    cnv.draw_line(np.array([0,0]), l.closest_pt_from_origin*5,fill="white",width=1)
    cnv.draw_point(l.closest_pt_from_origin,fill="blue",size=4)
    cnv.draw_arrow(np.array([0,0]), l.closest_pt_from_origin*.6,\
				fill="blue",width=3,arr_bk=.9,arr_per=.1)
    cnv.write_txt(l.closest_pt_from_origin+np.array([.1,.1]),"A","blue")
    arb_pt_1 = pt1*.2+pt2*.8+np.array([1,2])
    cnv.draw_point(arb_pt_1,fill=(3, 252, 53),size=4)
    cnv.draw_arrow(np.array([0,0]), arb_pt_1,\
				fill=(3, 252, 53),width=1,arr_bk=.9,arr_per=.1)
    cnv.write_txt(arb_pt_1+np.array([.1,.1]),"B",(3, 252, 53))
    l1 = Line(-arb_pt_1,l.closest_pt_from_origin-arb_pt_1)
    b_to_line = l1.closest_pt_from_origin+arb_pt_1
    cnv.draw_line(arb_pt_1, b_to_line,\
				fill=(3, 252, 53),width=1)
    cnv.write_txt(b_to_line+np.array([.1,.1]),"B'",(3, 252, 53))
    ##
    l2 = Line(pt1-arb_pt_1,pt2-arb_pt_1)
    b_to_main_line = l2.closest_pt_from_origin+arb_pt_1
    cnv.draw_line(arb_pt_1, b_to_main_line,\
				fill=(3, 252, 53),width=1)
    cnv.write_txt(b_to_main_line+np.array([.1,.1]),"B''",(3, 252, 53))
    basedir = '.\\images\\RotatingCube\\'
    cnv.im.save(basedir + "im" + str(idx) + ".png")

