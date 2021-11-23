import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageMath
from pyray.rotation import general_rotation, planar_rotation, axis_rotation,\
    rotate_point_about_axis
from pyray.shapes.twod.plot import Canvas
from pyray.axes import ZigZagPath
import pyray.grid as grd
#from importlib import reload

###

basedir = '.\\Images\\RotatingCube\\'
gg0=grd.Grid(end=np.array([12.0,12.0]),origin=np.array([256,256]),\
                center=np.array([3,3]),scale=64/np.sqrt(2))
pt = gg0.get_grid_pt(6,0)

for i in range(11):
    im=Image.new("RGB", (1024, 1024), (0,0,0))
    draw = ImageDraw.Draw(im,'RGBA')
    gg=grd.Grid(end=np.array([6.0,6.0]),origin=pt,\
                center=np.array([0,0]),
                rot=planar_rotation(-np.pi*10/10/4))
    gg0.draw(draw,fill=(252,0,0,90),width=1)
    gg.draw(draw)
    im.save(basedir + "im" + str(i) + ".png")

###

basedir = '.\\Images\\RotatingCube\\'
gg=grd.Grid(end=np.array([6.0,6.0]),\
                center=np.array([0,0]),origin=np.array([40,430]))
pts=[gg.get_grid_pt(i,j) for i,j in [(0,0),(0,2),(3,2),(3,6),(6,6)]]
pt1 = gg.get_grid_pt(0,0)
pt2 = gg.get_grid_pt(6,6)

zg = ZigZagPath(pts)

for i in range(11):
    im=Image.new("RGB", (512, 512), (0,0,0))
    draw = ImageDraw.Draw(im,'RGBA')
    gg.draw(draw,width=3)
    zg.draw_lines(draw,prop_dist=i/10.0)
    draw.line((pt1[0],pt1[1],pt2[0],pt2[1]), fill="#EF5B5B", width=2)
    draw.ellipse((pt1[0]-5, pt1[1]-5, pt1[0]+5, pt1[1]+5),fill='yellow')
    draw.ellipse((pt2[0]-5, pt2[1]-5, pt2[0]+5, pt2[1]+5),fill='yellow')
    im.save(basedir + "im" + str(i) + ".png")

###
basedir = '.\\Images\\RotatingCube\\'
for i in range(11):
    gg=grd.Grid(end=np.array([6.0,6.0]),scale=32,\
                center=np.array([0,0]),origin=np.array([40,220]),rot=planar_rotation(-np.pi/4*i/10.0))
    pts=[gg.get_grid_pt(i,j) for i,j in [(0,0),(0,2),(3,2),(3,6),(6,6)]]
    pt1 = gg.get_grid_pt(0,0)
    pt2 = gg.get_grid_pt(6,6)
    zg=ZigZagPath(pts)
    im=Image.new("RGB", (400, 400), (0,0,0))
    draw = ImageDraw.Draw(im,'RGBA')
    gg.draw(draw,width=3)
    zg.draw_lines(draw,prop_dist=10.0/10.0)
    draw.line((pt1[0],pt1[1],pt2[0],pt2[1]), fill="#EF5B5B", width=2)
    draw.ellipse((pt1[0]-5, pt1[1]-5, pt1[0]+5, pt1[1]+5),fill='yellow')
    draw.ellipse((pt2[0]-5, pt2[1]-5, pt2[0]+5, pt2[1]+5),fill='yellow')
    im.save(basedir + "im" + str(i) + ".png")


###
basedir = '.\\Images\\RotatingCube\\'
gg=grd.Grid(end=np.array([6.0,6.0]),\
                center=np.array([0,0]),origin=np.array([40,256]),
                rot=planar_rotation(-np.pi/4),scale=32)
pts=[gg.get_grid_pt(i,j) for i,j in [(0,0),(0,4),(4,4),(4,6),(6,6)]]
pts_ref=[gg.get_grid_pt(i,j) for i,j in [(0,0),(4,0),(4,4),(6,4),(6,6)]]
pt1 = gg.get_grid_pt(0,0)
pt2 = gg.get_grid_pt(6,6)
pt1_pr = pt1+(pt2-pt1)*-50
pt2_pr = pt2+(pt2-pt1)*50

## Rotate pt2 for the purpose of drawing the y-axis.
pt2_rot1=rotate_point_about_axis(np.concatenate((pt2,[0])),np.concatenate((pt1,[0])),\
    np.concatenate((pt1,[1])),-np.pi/2)
pt2_rot2=rotate_point_about_axis(np.concatenate((pt2,[0])),np.concatenate((pt1,[0])),\
    np.concatenate((pt1,[1])),np.pi/2)

zg=ZigZagPath(pts)
zg_ref=ZigZagPath(pts_ref)
for i in range(14):
    im=Image.new("RGB", (512, 512), (0,0,0))
    draw = ImageDraw.Draw(im,'RGBA')
    gg.draw(draw,width=3)
    zg.draw_lines(draw,prop_dist=i/10.0)
    zg_ref.draw_lines(draw,prop_dist=i/10.0,fill="orange")
    ##Draw the axes.
    draw.line((pt1_pr[0],pt1_pr[1],pt2_pr[0],pt2_pr[1]), fill="white", width=2)
    draw.line((pt1[0],pt1[1],pt2_rot1[0],pt2_rot1[1]), fill="white", width=2)
    draw.line((pt1[0],pt1[1],pt2_rot2[0],pt2_rot2[1]), fill="white", width=2)
    draw.line((pt1[0],pt1[1],pt2[0],pt2[1]), fill="red", width=3)
    draw.ellipse((pt1[0]-5, pt1[1]-5, pt1[0]+5, pt1[1]+5),fill='yellow')
    draw.ellipse((pt2[0]-5, pt2[1]-5, pt2[0]+5, pt2[1]+5),fill='yellow')
    im.save(basedir + "im" + str(i) + ".png")


###
basedir = '.\\Images\\RotatingCube\\'

for i in range(6):
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
  
    ## Draw horizontal line corresponding to one above the main diagonal.
    pt1=gg.get_grid_pt(0,1)
    pt2=gg.get_grid_pt(5,6)
    draw.line((pt1[0],pt1[1],pt2[0],pt2[1]), fill="yellow", width=2)

    pts=[gg.get_grid_pt(a,b) for a,b in [(0,0),(5,0),(5,6)]]
    pts1=[rotate_point_about_axis(np.concatenate((pts[j],[0])),
                            np.concatenate((pt1,[0])),\
                            np.concatenate((pt2,[0])),np.pi*i/5.0) \
                            for j in range(len(pts))]
    zg=ZigZagPath(pts1)
    zg.draw_lines(draw,prop_dist=1.0)
    draw.ellipse((pts1[0][0]-5, pts1[0][1]-5, pts1[0][0]+5, pts1[0][1]+5),fill='blue')
    im.save(basedir + "im" + str(i) + ".png")



##### How to create videos from the images.
#ffmpeg -framerate 10 -f image2 -i im%d.png -vb 20M vid.avi
#ffmpeg -i vid.avi -pix_fmt rgb24 -loop 0 out.gif
