import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageMath
from pyray.rotation import general_rotation, planar_rotation, axis_rotation,\
    rotate_point_about_axis
from pyray.shapes.twod.plot import Canvas
from pyray.axes import ZigZagPath
import pyray.grid as grd

def tst(basedir=".\\"):
    for i in range(11):
        im=Image.new("RGB", (512, 512), (0,0,0))
        draw = ImageDraw.Draw(im,'RGBA')
        end1=np.array([6.0,6.0])
        end2=np.array([4.0,8.0])
        end=end1*(1-i/10.0)+end2*(i/10.0)
        gg=grd.Grid(end=end,\
                        center=np.array([0,0]),origin=np.array([40,256]),
                        rot=planar_rotation(-np.pi/4),scale=32)
        pt2=gg.get_grid_pt(end[0],end[1])
        gg.draw(draw,width=3)
        ## Draw horizontal line corresponding to the main diagonal.
        pt1=gg.get_grid_pt(0,0)
        pt2=gg.get_grid_pt(6,6)
        draw.ellipse((pt2[0]-5, pt2[1]-5, pt2[0]+5, \
                        pt2[1]+5),fill='red') 
        draw.line((0,pt2[1],512,pt2[1]), fill="orange", width=3)
        draw.line((0,pt1[1],512,pt1[1]), fill="purple", width=3)
        draw.ellipse((pt1[0]-5, pt1[1]-5, pt1[0]+5, \
                        pt1[1]+5),fill='blue')
        
        ## Draw horizontal line corresponding to one above the main diagonal.
        pt1=gg.get_grid_pt(0,1)
        pt2=gg.get_grid_pt(5,6)
        #draw.line((pt1[0],pt1[1],pt2[0],pt2[1]), fill="orange", width=2)
        im.save(basedir + "im" + str(i) + ".png")

#######
for i in range(13):
    im=Image.new("RGB", (512, 512), (0,0,0))
    draw = ImageDraw.Draw(im,'RGBA')
    end2=np.array([4.0,8.0])
    gg=grd.Grid(end=end2,\
                    center=np.array([2,-4]),origin=np.array([90,280]),
                    rot=planar_rotation(-np.pi/4-np.pi*(i/12.0)),scale=32)
    gg.draw(draw,width=3)
    pt2=gg.get_grid_pt(end2[0],end2[1])
    draw.ellipse((pt2[0]-5, pt2[1]-5, pt2[0]+5, \
                    pt2[1]+5),fill='red') 
    draw.line((0,pt2[1],512,pt2[1]), fill="orange", width=3)
    ## Draw horizontal line corresponding to the main diagonal.
    pt1=gg.get_grid_pt(0,0)
    pt2=gg.get_grid_pt(6,6)    
    draw.line((0,pt1[1],512,pt1[1]), fill="purple", width=3)
    draw.ellipse((pt1[0]-5, pt1[1]-5, pt1[0]+5, \
                    pt1[1]+5),fill='blue')
        
    ## Draw horizontal line corresponding to one above the main diagonal.
    pt1=gg.get_grid_pt(0,1)
    pt2=gg.get_grid_pt(5,6)
    #draw.line((pt1[0],pt1[1],pt2[0],pt2[1]), fill="orange", width=2)
    pts=[gg.get_grid_pt(a,b) for a,b in [(0,0),(0,3),(2,3),(2,8),(4,8)]]
    zg=ZigZagPath(pts)
    zg.draw_lines(draw,prop_dist=1.0)
    im.save(basedir + "im" + str(i) + ".png")

