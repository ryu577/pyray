import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageMath
from pyray.rotation import general_rotation, planar_rotation, axis_rotation,\
    rotate_point_about_axis
from pyray.shapes.twod.plot import Canvas
from pyray.axes import ZigZagPath
import pyray.grid as grd


def basic_grid():
    im=Image.new("RGB", (512, 512), (0,0,0))
    draw = ImageDraw.Draw(im,'RGBA')
    gg=grd.Grid(end=np.array([6.0,6.0]),\
                    center=np.array([0,0]),origin=np.array([40,256]),
                    rot=planar_rotation(-np.pi/4),scale=32)
    gg.draw(draw,width=3)
    ## Draw horizontal line corresponding to the main diagonal.
    pt1=gg.get_grid_pt(0,0)
    pt2=gg.get_grid_pt(6,6)
    draw.line((pt1[0],pt1[1],pt2[0],pt2[1]), fill="purple", width=3)
    draw.ellipse((pt1[0]-5, pt1[1]-5, pt1[0]+5, \
                    pt1[1]+5),fill='blue')
    draw.ellipse((pt2[0]-5, pt2[1]-5, pt2[0]+5, \
                    pt2[1]+5),fill='red')    
    ## Draw horizontal line corresponding to one above the main diagonal.
    pt1=gg.get_grid_pt(0,1)
    pt2=gg.get_grid_pt(5,6)
    draw.line((pt1[0],pt1[1],pt2[0],pt2[1]), fill="orange", width=2)

    return im, draw, gg

basedir = '.\\Images\\RotatingCube\\'

### Grid path 0
for i in range(6):
    im,draw,gg=basic_grid()
    pt1=gg.get_grid_pt(0,1)
    pt2=gg.get_grid_pt(5,6)
    pts=[gg.get_grid_pt(a,b) for a,b in [(0,0),(5,0),(5,6)]]
    zg=ZigZagPath(pts)
    zg.draw_lines(draw,prop_dist=i/5.0)
    im.save(basedir + "im" + str(i) + ".png")


### Grid path 1
for i in range(6):
    im,draw,gg=basic_grid()
    pt1=gg.get_grid_pt(0,1)
    pt2=gg.get_grid_pt(5,6)
    pts=[gg.get_grid_pt(a,b) for a,b in [(0,0),(5,0),(5,6)]]
    pts1=[rotate_point_about_axis(np.concatenate((pts[j],[0])),
                            np.concatenate((pt1,[0])),\
                            np.concatenate((pt2,[0])),np.pi*i/5.0) \
                            for j in range(len(pts))]
    zg=ZigZagPath(pts1)
    zg.draw_lines(draw,prop_dist=1.0)
    draw.ellipse((pts1[0][0]-5, pts1[0][1]-5, pts1[0][0]+5, \
                    pts1[0][1]+5),fill='blue')
    im.save(basedir + "im" + str(5+i) + ".png")


### Grid path 2
for i in range(6):
    im,draw,gg=basic_grid()
    pt1=gg.get_grid_pt(0,1)
    pt2=gg.get_grid_pt(5,6)
    pts=[gg.get_grid_pt(a,b) for a,b in [(0,0),(5,0),(5,6)]]
    pts1=[rotate_point_about_axis(np.concatenate((pts[j],[0])),
                            np.concatenate((pt1,[0])),\
                            np.concatenate((pt2,[0])),np.pi*5.0/5.0) \
                            for j in range(len(pts))]
    zg=ZigZagPath(pts1)
    zg.draw_lines(draw,prop_dist=1.0)
    draw.ellipse((pts1[0][0]-5, pts1[0][1]-5, pts1[0][0]+5, \
                    pts1[0][1]+5),fill='blue')
    pts=[gg.get_grid_pt(a,b) for a,b in [(0,0),(0,1)]]
    pts1=[rotate_point_about_axis(np.concatenate((pts[j],[0])),
                            np.concatenate((pt1,[0])),\
                            np.concatenate((pt2,[0])),np.pi*i/5.0) \
                            for j in range(len(pts))]
    zg=ZigZagPath(pts1)
    zg.draw_lines(draw,prop_dist=1.0)
    draw.ellipse((pts1[0][0]-5, pts1[0][1]-5, pts1[0][0]+5, \
                    pts1[0][1]+5),fill='blue')
    im.save(basedir + "im" + str(10+i) + ".png")


### Grid path 3
for i in range(6):
    im,draw,gg=basic_grid()
    pt1=gg.get_grid_pt(0,1)
    pt2=gg.get_grid_pt(5,6)
    pts=[gg.get_grid_pt(a,b) for a,b in [(0,0),(5,0),(5,6)]]
    pts1=[rotate_point_about_axis(np.concatenate((pts[j],[0])),
                            np.concatenate((pt1,[0])),\
                            np.concatenate((pt2,[0])),np.pi*5.0/5.0) \
                            for j in range(len(pts))]
    zg=ZigZagPath(pts1)
    zg.draw_lines(draw,prop_dist=1.0)
    draw.ellipse((pts1[0][0]-5, pts1[0][1]-5, pts1[0][0]+5, \
                    pts1[0][1]+5),fill='blue')
    pts=[gg.get_grid_pt(a,b) for a,b in [(0,0),(0,1)]]
    pts1=[rotate_point_about_axis(np.concatenate((pts[j],[0])),
                            np.concatenate((pt1,[0])),\
                            np.concatenate((pt2,[0])),np.pi*5.0/5.0) \
                            for j in range(len(pts))]
    zg=ZigZagPath(pts1)
    zg.draw_lines(draw,prop_dist=1.0)
    draw.ellipse((pts1[0][0]-5, pts1[0][1]-5, pts1[0][0]+5, \
                    pts1[0][1]+5),fill='blue')

    pts=[gg.get_grid_pt(a,b) for a,b in [(0,0),(1,0),(1,2)]]
    pts1=[rotate_point_about_axis(np.concatenate((pts[j],[0])),
                            np.concatenate((pt1,[0])),\
                            np.concatenate((pt2,[0])),np.pi*i/5.0) \
                            for j in range(len(pts))]
    zg=ZigZagPath(pts1)
    zg.draw_lines(draw,prop_dist=1.0)
    draw.ellipse((pts1[0][0]-5, pts1[0][1]-5, pts1[0][0]+5, \
                    pts1[0][1]+5),fill='blue')
    im.save(basedir + "im" + str(15+i) + ".png")



### Grid path 4
for i in range(6):
    im,draw,gg=basic_grid()
    pt1=gg.get_grid_pt(0,1)
    pt2=gg.get_grid_pt(5,6)
    pts=[gg.get_grid_pt(a,b) for a,b in [(0,0),(5,0),(5,6)]]
    pts1=[rotate_point_about_axis(np.concatenate((pts[j],[0])),
                            np.concatenate((pt1,[0])),\
                            np.concatenate((pt2,[0])),np.pi*5.0/5.0) \
                            for j in range(len(pts))]
    zg=ZigZagPath(pts1)
    zg.draw_lines(draw,prop_dist=1.0)
    draw.ellipse((pts1[0][0]-5, pts1[0][1]-5, pts1[0][0]+5, \
                    pts1[0][1]+5),fill='blue')
    pts=[gg.get_grid_pt(a,b) for a,b in [(0,0),(0,1)]]
    pts1=[rotate_point_about_axis(np.concatenate((pts[j],[0])),
                            np.concatenate((pt1,[0])),\
                            np.concatenate((pt2,[0])),np.pi*5.0/5.0) \
                            for j in range(len(pts))]
    zg=ZigZagPath(pts1)
    zg.draw_lines(draw,prop_dist=1.0)
    pts=[gg.get_grid_pt(a,b) for a,b in [(0,0),(1,0),(1,2)]]
    pts1=[rotate_point_about_axis(np.concatenate((pts[j],[0])),
                            np.concatenate((pt1,[0])),\
                            np.concatenate((pt2,[0])),np.pi*5.0/5.0) \
                            for j in range(len(pts))]
    zg=ZigZagPath(pts1)
    zg.draw_lines(draw,prop_dist=1.0)
    pts=[gg.get_grid_pt(a,b) for a,b in [(0,0),(3,0),(3,4)]]
    pts1=[rotate_point_about_axis(np.concatenate((pts[j],[0])),
                            np.concatenate((pt1,[0])),\
                            np.concatenate((pt2,[0])),np.pi*i/5.0) \
                            for j in range(len(pts))]
    zg=ZigZagPath(pts1)
    zg.draw_lines(draw,prop_dist=1.0)
    im.save(basedir + "im" + str(20+i) + ".png")


### Wrap around grid
for i in range(6):
    im,draw,gg=basic_grid()
    pt1=gg.get_grid_pt(0,1)
    pt2=gg.get_grid_pt(5,6)
    pts=[gg.get_grid_pt(a,b) for a,b in [(0,0),(5,0),(5,6)]]
    pts1=[rotate_point_about_axis(np.concatenate((pts[j],[0])),
                            np.concatenate((pt1,[0])),\
                            np.concatenate((pt2,[0])),np.pi*5.0/5.0) \
                            for j in range(len(pts))]
    zg=ZigZagPath(pts1)
    zg.draw_lines(draw,prop_dist=1.0)
    draw.ellipse((pts1[0][0]-5, pts1[0][1]-5, pts1[0][0]+5, \
                    pts1[0][1]+5),fill='blue')
    pts=[gg.get_grid_pt(a,b) for a,b in [(0,0),(0,1)]]
    pts1=[rotate_point_about_axis(np.concatenate((pts[j],[0])),
                            np.concatenate((pt1,[0])),\
                            np.concatenate((pt2,[0])),np.pi*5.0/5.0) \
                            for j in range(len(pts))]
    zg=ZigZagPath(pts1)
    zg.draw_lines(draw,prop_dist=1.0)
    draw.ellipse((pts1[0][0]-5, pts1[0][1]-5, pts1[0][0]+5, \
                    pts1[0][1]+5),fill='blue')

    pts=[gg.get_grid_pt(a,b) for a,b in [(0,0),(1,0),(1,2)]]
    pts1=[rotate_point_about_axis(np.concatenate((pts[j],[0])),
                            np.concatenate((pt1,[0])),\
                            np.concatenate((pt2,[0])),np.pi*5/5.0) \
                            for j in range(len(pts))]
    zg=ZigZagPath(pts1)
    zg.draw_lines(draw,prop_dist=1.0)
    draw.ellipse((pts1[0][0]-5, pts1[0][1]-5, pts1[0][0]+5, \
                    pts1[0][1]+5),fill='blue')

    pts=[gg.get_grid_pt(a,b) for a,b in [(0,0),(3,0),(3,4)]]
    pts1=[rotate_point_about_axis(np.concatenate((pts[j],[0])),
                            np.concatenate((pt1,[0])),\
                            np.concatenate((pt2,[0])),np.pi*5.0/5.0) \
                            for j in range(len(pts))]
    zg=ZigZagPath(pts1)
    zg.draw_lines(draw,prop_dist=1.0)
    
    pts=[gg.get_grid_pt(a,b) for a,b in [(0,1),(6,1)]]
    zg=ZigZagPath(pts)
    zg.draw_lines(draw,prop_dist=i/5.0)
    
    pts=[gg.get_grid_pt(a,b) for a,b in [(5,6),(6,6),(6,1)]]
    zg=ZigZagPath(pts)
    zg.draw_lines(draw,prop_dist=i/5.0)    
    im.save(basedir + "im" + str(25+i) + ".png")



##### How to create videos from the images.
#ffmpeg -framerate 10 -f image2 -i im%d.png -vb 20M vid.avi
#ffmpeg -i vid.avi -pix_fmt rgb24 -loop 0 out.gif

