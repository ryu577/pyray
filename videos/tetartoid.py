import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageMath
from pyray.shapes.polyhedron import *
from pyray.axes import *
from pyray.rotation import *
from pyray.misc import zigzag2
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

basedir = '..\\images\\RotatingCube\\'

'''
Scene 1 - The following figure is a Tetartoid.
'''
txt = "The following figure is a Tetartoid."
tt = Tetartoid(0.45,0.08)
for i in range(0, 39):
    r = general_rotation(np.array([0.5,0.5,0.5]),2*np.pi*i/90)
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    tt.render_solid_planes(draw, r, shift=np.array([1000, 1000, 0]), scale=1200)
    writeStaggeredText(txt, draw, i, speed=2)
    im.save(basedir + "im" + str(i) + ".png")

#ffmpeg -framerate 10 -f image2 -i im%d.png -vb 20M vid.avi

'''
Scene 2 - It has these irregular pentagons as its
faces, which is an element of asymmetry.
'''
txt = "Its faces are irregular pentagons,\n an element of asymmetry."
tt = Tetartoid(0.45,0.08)
for i in range(39, 39+46):
    r = general_rotation(np.array([0.5,0.5,0.5]),2*np.pi*i/90)
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    tt.render_solid_planes(draw, r, shift=np.array([1000, 1000, 0]), scale=1200)
    pl = tt.planes[int((i-39)/5)%12]
    render_solid_planes([pl], draw, r, shift=np.array([1000, 1000, 0]), 
                            scale=1200, h=170,s=100)
    writeStaggeredText(txt, draw, i-39, speed=2)
    im.save(basedir + "im" + str(i-39) + ".png")

#ffmpeg -framerate 9 -f image2 -i im%d.png -vb 20M vid.avi

'''
Scene 3 - But then all its faces are the same
pentagon which is rather symmetric.
'''
txt = "But then each face is the\nsame pentagon, making\nit rather symmetric."
tt = Tetartoid(0.45,0.08)
for i in range(84, 84+46):
    r = general_rotation(np.array([0.5,0.5,0.5]),2*np.pi*i/90)
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    tt.render_solid_planes(draw, r, shift=np.array([1000, 1000, 0]), scale=1200)
    for j in range(min(int((i-84)/2),12)):
        pl = tt.planes[:j]
        render_solid_planes(pl, draw, r, shift=np.array([1000, 1000, 0]), 
                            scale=1200, h=170,s=100)
    writeStaggeredText(txt, draw, i-84, speed=2)
    im.save(basedir + "im" + str(i-84) + ".png")

#ffmpeg -framerate 7 -f image2 -i im%d.png -vb 20M vid.avi

'''
Scene 4 
'''
txt = "It's these element\nof symmetry and asymmetry\ncoexisting that makes\nit fascinating."
tt = Tetartoid(0.45,0.08)
for i in range(129, 129+56):
    r = general_rotation(np.array([0.5,0.5,0.5]),2*np.pi*i/90)
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    #tt.render_solid_planes(draw, r, shift=np.array([1000, 1000, 0]), scale=1200)
    for j in range(12):
        pl = tt.planes[:j]
        render_solid_planes(pl, draw, r, shift=np.array([1000, 1000, 0]), 
                            scale=1200, h=170,s=100)
    for j in range(min(int((i-129)/2),12)):
        pl = tt.planes[:j]
        render_solid_planes(pl, draw, r, shift=np.array([1000, 1000, 0]), 
                            scale=1200)
    writeStaggeredText(txt, draw, i-129, speed=2)
    im.save(basedir + "im" + str(i-129) + ".png")

#ffmpeg -framerate 6 -f image2 -i im%d.png -vb 20M vid.avi


'''
Scene 5
'''
txt = "This is not one solid\nbut a whole\nfamily of them."

for i in range(184, 184+56):
    s = zigzag2((i-184)*.033, .45, .49, .13)
    t = 0.08
    if i-184>18:
        t = zigzag2((i-184-18)*.005, .08, .1, .01)
    tt = Tetartoid(s, t)
    r = general_rotation(np.array([0.5,0.5,0.5]),2*np.pi*i/90)
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    tt.render_solid_planes(draw, r, shift=np.array([1000, 1000, 0]), scale=1200)
    writeStaggeredText(txt, draw, i-184, speed=2)
    im.save(basedir + "im" + str(i-184) + ".png")

#ffmpeg -framerate 6 -f image2 -i im%d.png -vb 20M vid.avi

s_old = 0.1549999999999998
t_old = 0.08499999999999998
'''
Scene 6
'''
txt = "One member of the family\nhas all regular pentagons."
for i in range(239, 239+56):
    s = s_old + (0.404508-s_old)*(i-239)/56
    t = t_old + (0.0954913-t_old)*(i-239)/56
    tt = Tetartoid(s, t)
    r = general_rotation(np.array([0.5,0.5,0.5]),2*np.pi*i/90)
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    tt.render_solid_planes(draw, r, shift=np.array([1000, 1000, 0]), scale=1200)
    writeStaggeredText(txt, draw, i-239, speed=2)
    im.save(basedir + "im" + str(i-239) + ".png")

#ffmpeg -framerate 9 -f image2 -i im%d.png -vb 20M vid.avi

'''
Scene 7
'''
txt = "It's called a Dodecahedron"
for i in range(294, 294+31):
    s = 0.404508
    t = 0.0954913
    tt = Tetartoid(s, t)
    r = general_rotation(np.array([0.5,0.5,0.5]),2*np.pi*i/90)
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    tt.render_solid_planes(draw, r, shift=np.array([1000, 1000, 0]), scale=1200)
    writeStaggeredText(txt, draw, i-294, speed=2)
    im.save(basedir + "im" + str(i-294) + ".png")

#ffmpeg -framerate 7 -f image2 -i im%d.png -vb 20M vid.avi

'''
Scene 8
'''
base_i = 324
txt = "To construct it,\nwe start with one of the pentagons."
for i in range(base_i, base_i+51):
    s = 0.404508
    t = 0.0954913
    tt = Tetartoid(s, t)
    r = general_rotation(np.array([0.5,0.5,0.5]),2*np.pi*i/90)
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    #tt.render_solid_planes(draw, r, shift=np.array([1000, 1000, 0]), scale=1200)
    render_solid_planes([tt.planes[0]], draw, r, shift=np.array([1000, 1000, 0]),
                            scale=1200)
    for j in range(1,12):
        pl = np.copy(tt.planes[j])
        pl_center = np.sum(pl,axis=0)
        pl = pl + pl_center*(i-base_i)/40
        render_solid_planes([pl], draw, r, shift=np.array([1000, 1000, 0]),
                            scale=1200)
    writeStaggeredText(txt, draw, i-base_i, speed=2)
    im.save(basedir + "im" + str(i-base_i) + ".png")

#ffmpeg -framerate 7 -f image2 -i im%d.png -vb 20M vid.avi

'''
Scene 9
'''
base_i=374
txt = "Duplicate by rotating\nabout the vertices."
r_base = general_rotation(np.array([0.5,0.5,0.5]),2*np.pi*base_i/90)
plane = np.copy(tt.planes[0])
#plane = np.array([[0,1,0],[np.cos(np.pi/3),-np.sin(np.pi/3),0],[-np.cos(np.pi/3), -np.sin(np.pi/3),0]])
plane = np.dot(plane,r_base)
plane_per = np.cross((plane[0]-plane[1]),(plane[1]-plane[2]))
plane_e = np.append(plane,np.ones(5)[...,None],1)
#plane_e = np.append(plane,np.ones(3)[...,None],1)

for i in range(base_i, base_i+31):
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    #r = axis_rotation(plane_e[1],plane_e[0],2*np.pi*(i-base_i)/30)
    r = axis_rotation(plane[0],plane[0]+plane_per,2*np.pi*min((i-base_i),21)/30)
    plane1 = np.dot(r,plane_e.T).T
    plane1 = plane1[:,np.array([0,1,2])]
    render_solid_planes([plane],draw, np.eye(3),cut_back_face=False,
                        scale=1200)
    render_solid_planes([plane1],draw, np.eye(3),cut_back_face=False,
                        scale=1200)
    writeStaggeredText(txt, draw, i-base_i, speed=2)
    im.save(basedir + "im" + str(i-base_i) + ".png")

#ffmpeg -framerate 6 -f image2 -i im%d.png -vb 20M vid.avi

'''
Scene 10
'''
base_i = 404
txt = "Duplicate by rotating\nabout the vertices."
r_base = general_rotation(np.array([0.5,0.5,0.5]),2*np.pi*374/90)
plane = np.copy(tt.planes[0])
plane = np.dot(plane,r_base)
plane_per = np.cross((plane[0]-plane[1]),(plane[1]-plane[2]))
plane_e = np.append(plane,np.ones(5)[...,None],1)
r = axis_rotation(plane[0],plane[0]+plane_per,2*np.pi*21/30)
plane1 = np.dot(r,plane_e.T).T
plane1 = plane1[:,np.array([0,1,2])]

for i in range(base_i, base_i+31):
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    r = axis_rotation(plane[1],plane[1]+plane_per,2*np.pi*min((i-base_i),21)/30)
    plane2 = np.dot(r,plane_e.T).T
    plane2 = plane2[:,np.array([0,1,2])]
    render_solid_planes([plane],draw, np.eye(3),cut_back_face=False,
                        scale=1200,make_edges=True)
    render_solid_planes([plane1],draw, np.eye(3),cut_back_face=False,
                        scale=1200)
    render_solid_planes([plane2],draw, np.eye(3),cut_back_face=False,
                        scale=1200)
    writeStaggeredText(txt, draw, 32, speed=2)
    im.save(basedir + "im" + str(i-base_i) + ".png")

#ffmpeg -framerate 8 -f image2 -i im%d.png -vb 20M vid.avi


'''
Scene 11
'''
base_i = 434
txt = "Duplicate by rotating\nabout the vertices."
r_base = general_rotation(np.array([0.5,0.5,0.5]),2*np.pi*374/90)
plane = np.copy(tt.planes[0])
plane = np.dot(plane,r_base)
plane_per = np.cross((plane[0]-plane[1]),(plane[1]-plane[2]))
plane_e = np.append(plane,np.ones(5)[...,None],1)
r = axis_rotation(plane[0],plane[0]+plane_per,2*np.pi*21/30)
plane1 = np.dot(r,plane_e.T).T
plane1 = plane1[:,np.array([0,1,2])]

r = axis_rotation(plane[1],plane[1]+plane_per,2*np.pi*21/30)
plane2 = np.dot(r,plane_e.T).T
plane2 = plane2[:,np.array([0,1,2])]

for i in range(base_i, base_i+22):
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    r = axis_rotation(plane[2],plane[2]+plane_per,2*np.pi*min((i-base_i),21)/30)
    plane3 = np.dot(r,plane_e.T).T
    plane3 = plane3[:,np.array([0,1,2])]
    render_solid_planes([plane],draw, np.eye(3),cut_back_face=False,
                        scale=1200,make_edges=True)
    render_solid_planes([plane1],draw, np.eye(3),cut_back_face=False,
                        scale=1200)
    render_solid_planes([plane2],draw, np.eye(3),cut_back_face=False,
                        scale=1200)
    render_solid_planes([plane3],draw, np.eye(3),cut_back_face=False,
                        scale=1200)
    writeStaggeredText(txt, draw, 32, speed=2)
    im.save(basedir + "im" + str(i-base_i) + ".png")

#ffmpeg -framerate 12 -f image2 -i im%d.png -vb 20M vid.avi

'''
Scene 12
'''
base_i = 455
txt = "Duplicate by rotating\nabout the vertices."
r_base = general_rotation(np.array([0.5,0.5,0.5]),2*np.pi*374/90)
plane = np.copy(tt.planes[0])
plane = np.dot(plane,r_base)
plane_per = np.cross((plane[0]-plane[1]),(plane[1]-plane[2]))
plane_e = np.append(plane,np.ones(5)[...,None],1)
r = axis_rotation(plane[0],plane[0]+plane_per,2*np.pi*21/30)
plane1 = np.dot(r,plane_e.T).T
plane1 = plane1[:,np.array([0,1,2])]

r = axis_rotation(plane[1],plane[1]+plane_per,2*np.pi*21/30)
plane2 = np.dot(r,plane_e.T).T
plane2 = plane2[:,np.array([0,1,2])]

r = axis_rotation(plane[2],plane[2]+plane_per,2*np.pi*21/30)
plane3 = np.dot(r,plane_e.T).T
plane3 = plane3[:,np.array([0,1,2])]

for i in range(base_i, base_i+22):
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    r = axis_rotation(plane[3],plane[3]+plane_per,2*np.pi*min((i-base_i),21)/30)
    plane4 = np.dot(r,plane_e.T).T
    plane4 = plane4[:,np.array([0,1,2])]
    render_solid_planes([plane],draw, np.eye(3),cut_back_face=False,
                        scale=1200,make_edges=True)
    render_solid_planes([plane1],draw, np.eye(3),cut_back_face=False,
                        scale=1200)
    render_solid_planes([plane2],draw, np.eye(3),cut_back_face=False,
                        scale=1200)
    render_solid_planes([plane3],draw, np.eye(3),cut_back_face=False,
                        scale=1200)
    render_solid_planes([plane4],draw, np.eye(3),cut_back_face=False,
                        scale=1200)
    writeStaggeredText(txt, draw, 32, speed=2)
    im.save(basedir + "im" + str(i-base_i) + ".png")

#ffmpeg -framerate 20 -f image2 -i im%d.png -vb 20M vid.avi

'''
Scene 13
'''
base_i = 476
txt = "Duplicate by rotating\nabout the vertices."
r_base = general_rotation(np.array([0.5,0.5,0.5]),2*np.pi*374/90)
plane = np.copy(tt.planes[0])
plane = np.dot(plane,r_base)
plane_per = np.cross((plane[0]-plane[1]),(plane[1]-plane[2]))
plane_e = np.append(plane,np.ones(5)[...,None],1)
r = axis_rotation(plane[0],plane[0]+plane_per,2*np.pi*21/30)
plane1 = np.dot(r,plane_e.T).T
plane1 = plane1[:,np.array([0,1,2])]

r = axis_rotation(plane[1],plane[1]+plane_per,2*np.pi*21/30)
plane2 = np.dot(r,plane_e.T).T
plane2 = plane2[:,np.array([0,1,2])]

r = axis_rotation(plane[2],plane[2]+plane_per,2*np.pi*21/30)
plane3 = np.dot(r,plane_e.T).T
plane3 = plane3[:,np.array([0,1,2])]

r = axis_rotation(plane[3],plane[3]+plane_per,2*np.pi*21/30)
plane4 = np.dot(r,plane_e.T).T
plane4 = plane4[:,np.array([0,1,2])]

for i in range(base_i, base_i+22):
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    r = axis_rotation(plane[4],plane[4]+plane_per,2*np.pi*min((i-base_i),21)/30)
    plane5 = np.dot(r,plane_e.T).T
    plane5 = plane5[:,np.array([0,1,2])]
    render_solid_planes([plane],draw, np.eye(3),cut_back_face=False,
                        scale=1200,make_edges=True)
    render_solid_planes([plane1],draw, np.eye(3),cut_back_face=False,
                        scale=1200)
    render_solid_planes([plane2],draw, np.eye(3),cut_back_face=False,
                        scale=1200)
    render_solid_planes([plane3],draw, np.eye(3),cut_back_face=False,
                        scale=1200)
    render_solid_planes([plane4],draw, np.eye(3),cut_back_face=False,
                        scale=1200)
    render_solid_planes([plane5],draw, np.eye(3),cut_back_face=False,
                        scale=1200)
    writeStaggeredText(txt, draw, 32, speed=2)
    im.save(basedir + "im" + str(i-base_i) + ".png")

#ffmpeg -framerate 25 -f image2 -i im%d.png -vb 20M vid.avi


'''
Scene 14
'''
base_i = 497
txt = "Then rotate them in\nto form a bowl."
r_base = general_rotation(np.array([0.5,0.5,0.5]),2*np.pi*374/90)
plane = np.copy(tt.planes[0])
plane = np.dot(plane,r_base)
plane_per = np.cross((plane[0]-plane[1]),(plane[1]-plane[2]))
plane_e = np.append(plane,np.ones(5)[...,None],1)

r = axis_rotation(plane[0],plane[0]+plane_per,2*np.pi*21/30)
plane1 = np.dot(r,plane_e.T).T
#plane1 = plane1[:,np.array([0,1,2])]

r = axis_rotation(plane[1],plane[1]+plane_per,2*np.pi*21/30)
plane2 = np.dot(r,plane_e.T).T
#plane2 = plane2[:,np.array([0,1,2])]

r = axis_rotation(plane[2],plane[2]+plane_per,2*np.pi*21/30)
plane3 = np.dot(r,plane_e.T).T
#plane3 = plane3[:,np.array([0,1,2])]

r = axis_rotation(plane[3],plane[3]+plane_per,2*np.pi*21/30)
plane4 = np.dot(r,plane_e.T).T
#plane4 = plane4[:,np.array([0,1,2])]

r = axis_rotation(plane[4],plane[4]+plane_per,2*np.pi*21/30)
plane5 = np.dot(r,plane_e.T).T
#plane5 = plane5[:,np.array([0,1,2])]

for i in range(base_i, base_i+31):
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    render_solid_planes([plane],draw, np.eye(3),cut_back_face=False,
                        scale=1200,make_edges=True)
    r = axis_rotation(plane1[0],plane1[4],108/180*np.pi*min((i-base_i),18)/30)
    plane1_dr = np.dot(r,plane1.T).T
    plane1_dr = plane1_dr[:,np.array([0,1,2])]
    render_solid_planes([plane1_dr],draw, np.eye(3),cut_back_face=False,
                        scale=1200)
    r = axis_rotation(plane2[1],plane2[0],108/180*np.pi*min((i-base_i),18)/30)
    plane2_dr = np.dot(r,plane2.T).T
    plane2_dr = plane2_dr[:,np.array([0,1,2])]
    render_solid_planes([plane2_dr],draw, np.eye(3),cut_back_face=False,
                        scale=1200)
    r = axis_rotation(plane3[2],plane3[1],108/180*np.pi*min((i-base_i),18)/30)
    plane3_dr = np.dot(r,plane3.T).T
    plane3_dr = plane3_dr[:,np.array([0,1,2])]
    render_solid_planes([plane3_dr],draw, np.eye(3),cut_back_face=False,
                        scale=1200)
    r = axis_rotation(plane4[3],plane4[2],108/180*np.pi*min((i-base_i),18)/30)
    plane4_dr = np.dot(r,plane4.T).T
    plane4_dr = plane4_dr[:,np.array([0,1,2])]
    render_solid_planes([plane4_dr],draw, np.eye(3),cut_back_face=False,
                        scale=1200)
    r = axis_rotation(plane5[4],plane5[3],108/180*np.pi*min((i-base_i),18)/30)
    plane5_dr = np.dot(r,plane5.T).T
    plane5_dr = plane5_dr[:,np.array([0,1,2])]
    render_solid_planes([plane5_dr],draw, np.eye(3),cut_back_face=False,
                        scale=1200)
    writeStaggeredText(txt, draw, 2*(i-base_i), speed=2)
    im.save(basedir + "im" + str(i-base_i) + ".png")


'''
Scene 15
'''
txt = "Duplicate the bowl."
r_base = general_rotation(np.array([0.5,0.5,0.5]),2*np.pi*374/90)
plane = np.copy(tt.planes[0])
#plane = np.dot(plane,r_base)
plane_per = np.cross((plane[0]-plane[1]),(plane[1]-plane[2]))

for i in range(21):
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    nu_planes = np.copy(tt.planes[[0,1,2,3,5,6]])
    nu_planes -= plane_per*min(i,10)*3
    render_solid_planes(nu_planes, draw, r_base, cut_back_face=False,
                        scale=1200-i*24)
    render_solid_planes(tt.planes[[0,1,2,3,5,6]], draw, r_base, cut_back_face=False,
                        scale=1200-i*24)
    writeStaggeredText(txt, draw, 2*i, speed=2)
    im.save(basedir + "im" + str(i) + ".png")

#ffmpeg -framerate 5.5 -f image2 -i im%d.png -vb 20M vid.avi

'''
Scene 16
'''
## First, we need to fine the angle between adjacent faces of a Dodecahedron.
angle = angle_btw_planes(tt.planes[0], tt.planes[1])
txt = "Turn the second one\ninside out."
r_base = general_rotation(np.array([0.5,0.5,0.5]),2*np.pi*374/90)
plane = np.copy(tt.planes[0])
plane_per = np.cross((plane[0]-plane[1]),(plane[1]-plane[2]))

for i in range(21):
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    nu_planes = np.copy(tt.planes[[0,1,2,3,5,6]])
    nu_planes -= plane_per*30
    nu_planes[1] = rotate_plane(nu_planes[1],nu_planes[1][0], nu_planes[1][4],-2*angle*i/20)
    nu_planes[2] = rotate_plane(nu_planes[2],nu_planes[2][1], nu_planes[2][0],-2*angle*i/20)
    nu_planes[3] = rotate_plane(nu_planes[3],nu_planes[3][2], nu_planes[3][1],-2*angle*i/20)
    nu_planes[4] = rotate_plane(nu_planes[4],nu_planes[4][4], nu_planes[4][3],-2*angle*i/20)
    nu_planes[5] = rotate_plane(nu_planes[5],nu_planes[5][3], nu_planes[5][2],-2*angle*i/20)
    render_solid_planes(nu_planes, draw, r_base, cut_back_face=False,
                        scale=720)
    render_solid_planes(tt.planes[[0,1,2,3,5,6]], draw, r_base, cut_back_face=False,
                        scale=720)
    writeStaggeredText(txt, draw, 2*i, speed=2)
    im.save(basedir + "im" + str(i) + ".png")

#ffmpeg -framerate 5.5 -f image2 -i im%d.png -vb 20M vid.avi


'''
Scene 17
'''
angle = angle_btw_planes(tt.planes[0], tt.planes[1])
txt = "And then connect the two."

plane = np.copy(tt.planes[0])
plane_per = np.cross((plane[0]-plane[1]),(plane[1]-plane[2]))

for i in range(58):
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    r_base = general_rotation(np.array([0.5,0.5,0.5]),2*np.pi*(374-i)/90)
    nu_planes = np.copy(tt.planes[[0,1,2,3,5,6]])
    nu_planes -= plane_per*(30-i/3)
    nu_planes[1] = rotate_plane(nu_planes[1],nu_planes[1][0], nu_planes[1][4],-2*angle)
    nu_planes[2] = rotate_plane(nu_planes[2],nu_planes[2][1], nu_planes[2][0],-2*angle)
    nu_planes[3] = rotate_plane(nu_planes[3],nu_planes[3][2], nu_planes[3][1],-2*angle)
    nu_planes[4] = rotate_plane(nu_planes[4],nu_planes[4][4], nu_planes[4][3],-2*angle)
    nu_planes[5] = rotate_plane(nu_planes[5],nu_planes[5][3], nu_planes[5][2],-2*angle)
    render_solid_planes_back_first(nu_planes, draw, r_base, cut_back_face=False,
                        scale=720)
    render_solid_planes_back_first(tt.planes[[0,1,2,3,5,6]], draw, r_base, cut_back_face=True,
                        scale=720)
    writeStaggeredText(txt, draw, 2*i, speed=2)
    im.save(basedir + "im" + str(i) + ".png")

#ffmpeg -framerate 12 -f image2 -i im%d.png -vb 20M vid.avi


'''
Scene 18
'''
angle = angle_btw_planes(tt.planes[0], tt.planes[1])
txt = "And then connect the two."

plane = np.copy(tt.planes[0])
plane_per = np.cross((plane[0]-plane[1]),(plane[1]-plane[2]))
plane_cen = np.mean(plane,axis=0)

for i in range(21):
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    r_base = general_rotation(np.array([0.5,0.5,0.5]),2*np.pi*(374-57)/90)
    nu_planes = np.copy(tt.planes[[0,1,2,3,5,6]])
    nu_planes -= plane_per*(30-57/3-float(i)/9.0)
    nu_planes[0] = rotate_plane(nu_planes[0],plane_cen, plane_cen+plane_per,i*np.pi/5/20)
    nu_planes[1] = rotate_plane(nu_planes[1],nu_planes[1][0], nu_planes[1][4],-2*angle)
    nu_planes[1] = rotate_plane(nu_planes[1],plane_cen, plane_cen+plane_per,i*np.pi/5/20)
    nu_planes[2] = rotate_plane(nu_planes[2],nu_planes[2][1], nu_planes[2][0],-2*angle)
    nu_planes[2] = rotate_plane(nu_planes[2],plane_cen, plane_cen+plane_per,i*np.pi/5/20)
    nu_planes[3] = rotate_plane(nu_planes[3],nu_planes[3][2], nu_planes[3][1],-2*angle)
    nu_planes[3] = rotate_plane(nu_planes[3],plane_cen, plane_cen+plane_per,i*np.pi/5/20)
    nu_planes[4] = rotate_plane(nu_planes[4],nu_planes[4][4], nu_planes[4][3],-2*angle)
    nu_planes[4] = rotate_plane(nu_planes[4],plane_cen, plane_cen+plane_per,i*np.pi/5/20)
    nu_planes[5] = rotate_plane(nu_planes[5],nu_planes[5][3], nu_planes[5][2],-2*angle)
    nu_planes[5] = rotate_plane(nu_planes[5],plane_cen, plane_cen+plane_per,i*np.pi/5/20)
    render_solid_planes_back_first(nu_planes, draw, r_base, cut_back_face=False,
                        scale=720+i/20*(1200-720))
    render_solid_planes_back_first(tt.planes[[0,1,2,3,5,6]], draw, r_base, cut_back_face=False,
                        scale=720+i/20*(1200-720))
    writeStaggeredText(txt, draw, 23, speed=2)
    im.save(basedir + "im" + str(i) + ".png")

for i in range(21,27):
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    tt.render_solid_planes(draw, r_base, shift=np.array([1000, 1000, 0]), scale=1200)
    im.save(basedir + "im" + str(i) + ".png")



'''
Scene 19
'''
txt = "The Tetartoid can be\nconstructed in a similar manner\nbut here we will start with\na Tetrahedron."

for i in range(51):
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    s = 0.404508
    t = 0.0954913*max((1-i/20),0)
    tt = Tetartoid(s, t)
    r_base = general_rotation(np.array([0.5,0.5,0.5]),2*np.pi*(317+i)/90)
    tt.render_solid_planes(draw, r_base, shift=np.array([1000, 1000, 0]), scale=1200)
    writeStaggeredText(txt, draw, i, speed=3)
    im.save(basedir + "im" + str(i) + ".png")

#ffmpeg -framerate 7 -f image2 -i im%d.png -vb 20M vid.avi


'''
Scene 20
'''
txt = "The Tetartoid can be\nconstructed in a similar manner\nbut here we will start with\na Tetrahedron."

for i in range(51):
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    s = 0.404508
    t = 0.0954913*0
    tt = Tetartoid(s, t)
    tet = Tetrahedron()
    r_base = general_rotation(np.array([0.5,0.5,0.5]),2*np.pi*(367+i)/90)
    #tt.render_solid_planes(draw, r_base, shift=np.array([1000, 1000, 0]),\
    #                scale=1200, make_edges=True,trnsp=int(255*(1-i/50)))
    render_solid_planes(tt.planes, draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=False,trnsp=int(255*(1-i/50)))
    render_solid_planes(tet.planes, draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=True,trnsp=int(255*(1-i/50)))
    writeStaggeredText(txt, draw, 60, speed=3)
    im.save(basedir + "im" + str(i) + ".png")

#ffmpeg -framerate 8 -f image2 -i im%d.png -vb 20M vid.avi


'''
Scene 21
'''
txt = "First, we take two points\non each side, at distance s\nfrom the end-points."

for i in range(51):
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    s = 0.404508*(i/50)
    t = 0.0954913
    tt = Tetartoid(s, t)
    tet = Tetrahedron()
    r_base = general_rotation(np.array([0.5,0.5,0.5]),2*np.pi*(367+50)/90)
    #render_solid_planes(tt.planes, draw, r_base, shift=np.array([1000, 1000, 0]),\
    #                scale=1200, make_edges=False,trnsp=125)
    render_solid_planes(tet.planes, draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=True,trnsp=0)
    for ed in tet.edges:
        pt1 = ed[0]*s+ed[1]*(1-s)
        pt2 = ed[1]*s+ed[0]*(1-s)
        pt1 = np.dot(r_base.T,pt1)*1200+np.array([1000,1000,0])
        pt2 = np.dot(r_base.T,pt2)*1200+np.array([1000,1000,0])
        draw.ellipse((pt1[0]-5, pt1[1]-5, pt1[0]+5, pt1[1]+5),fill='yellow', outline='yellow')
        draw.ellipse((pt2[0]-5, pt2[1]-5, pt2[0]+5, pt2[1]+5),fill='yellow', outline='yellow')
    writeStaggeredText(txt, draw, i, speed=2)
    im.save(basedir + "im" + str(i) + ".png")


'''
Scene 22
'''
txt = "Consider the plane joining the\nedge to the center"

for i in range(31):
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    s = 0.404508
    t = 0.0954913
    tt = Tetartoid(s, 0)
    tet = Tetrahedron()
    r_base = general_rotation(np.array([0.5,0.5,0.5]),2*np.pi*(367+50)/90)
    r_base_2 = general_rotation(np.dot(r_base.T,tet.vertices[3]), 2*np.pi*min(i,27)/90)
    r_base = np.dot(r_base, r_base_2)
    #render_solid_planes(tt.planes, draw, r_base, shift=np.array([1000, 1000, 0]),\
    #                scale=1200, make_edges=False,trnsp=125)
    render_solid_planes(tet.planes, draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=True,trnsp=0)
    for i1 in range(4):
        for j1 in range(i1+1,4):
            pt1_fin = np.dot(r_base.T,tt.qs[i1,j1])*1200+np.array([1000,1000,0])
            pt2_fin = np.dot(r_base.T,tt.qs[j1,i1])*1200+np.array([1000,1000,0])
            draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='yellow', outline='yellow')
            draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='yellow', outline='yellow')
    p = 0.05 + i/30.0*0.95
    cent_pt = (tet.vertices[0]+tet.vertices[3])/2*(1-p) + np.array([0,0,0])*p
    #cent_pt = np.array([0,0,0])
    face1 = np.array([cent_pt, tet.vertices[0], tet.vertices[3]])
    render_solid_planes([face1], draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=True,cut_back_face=False,trnsp=180)
    writeStaggeredText(txt, draw, i, speed=2)
    im.save(basedir + "im" + str(i) + ".png")


'''
Scene 23
'''
txt = "Move the two points\nperpendicular to the plane\na distance t on either side."

for i in range(51):
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    s = 0.404508
    t = 0.0954913*min(1,i/30)
    tt = Tetartoid(s, 0)
    tt1 = Tetartoid(s, t)
    tet = Tetrahedron()
    r_base = general_rotation(np.array([0.5,0.5,0.5]),2*np.pi*(367+50)/90)
    r_base_2 = general_rotation(np.dot(r_base.T,tet.vertices[3]), 2*np.pi*max(0,27-i)/90)
    r_base = np.dot(r_base, r_base_2)
    #render_solid_planes(tt.planes, draw, r_base, shift=np.array([1000, 1000, 0]),\
    #                scale=1200, make_edges=False,trnsp=125)
    render_solid_planes(tet.planes, draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=True,trnsp=0)
    p = 1.0
    cent_pt = (tet.vertices[0]+tet.vertices[3])/2*(1-p) + np.array([0,0,0])*p
    #cent_pt = np.array([0,0,0])
    face1 = np.array([cent_pt, tet.vertices[0], tet.vertices[3]])
    render_solid_planes([face1], draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=True,cut_back_face=False,trnsp=180)
    for i1 in range(4):
        for j1 in range(i1+1,4):
            if i1 == 0 and j1 == 3:
                pt1_fin = np.dot(r_base.T,tt1.qs[i1,j1])*1200+np.array([1000,1000,0])
                pt2_fin = np.dot(r_base.T,tt1.qs[j1,i1])*1200+np.array([1000,1000,0])
                draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='red', outline='yellow')
                draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='red', outline='yellow')
            pt1_fin = np.dot(r_base.T,tt.qs[i1,j1])*1200+np.array([1000,1000,0])
            pt2_fin = np.dot(r_base.T,tt.qs[j1,i1])*1200+np.array([1000,1000,0])
            draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='yellow', outline='yellow')
            draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='yellow', outline='yellow')
    writeStaggeredText(txt, draw, i, speed=2)
    im.save(basedir + "im" + str(i) + ".png")


'''
Scene 24
'''
txt = "Similarly, move the points\nfor the bottom edge."

for i in range(35):
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    s = 0.404508
    t = 0.0954913*min(1,i/30)
    tt = Tetartoid(s, 0)
    tt1 = Tetartoid(s, 0.0954913)
    tt2 = Tetartoid(s, t)
    tet = Tetrahedron()
    r_base = general_rotation(np.array([0.5,0.5,0.5]),2*np.pi*(367+50)/90)
    r_base_2 = general_rotation(np.dot(r_base.T,tet.vertices[2]), 2*np.pi*zigzag2(i,0,17,0)/90)
    r_base = np.dot(r_base, r_base_2)
    #render_solid_planes(tt2.planes, draw, r_base, shift=np.array([1000, 1000, 0]),\
    #                scale=1200, make_edges=False,trnsp=125)
    render_solid_planes(tet.planes, draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=True,trnsp=0)
    p = 1.0
    cent_pt = (tet.vertices[0]+tet.vertices[2])/2*(1-p) + np.array([0,0,0])*p
    face1 = np.array([cent_pt, tet.vertices[0], tet.vertices[2]])
    render_solid_planes([face1], draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=True,cut_back_face=False,trnsp=180)
    for i1 in range(4):
        for j1 in range(i1+1,4):
            if i1 == 0 and j1 == 3:
                pt1_fin = np.dot(r_base.T,tt1.qs[i1,j1])*1200+np.array([1000,1000,0])
                pt2_fin = np.dot(r_base.T,tt1.qs[j1,i1])*1200+np.array([1000,1000,0])
                draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='red', outline='yellow')
                draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='red', outline='yellow')
            if i1 == 0 and j1 == 2:
                pt1_fin = np.dot(r_base.T,tt2.qs[i1,j1])*1200+np.array([1000,1000,0])
                pt2_fin = np.dot(r_base.T,tt2.qs[j1,i1])*1200+np.array([1000,1000,0])
                draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='red', outline='yellow')
                draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='red', outline='yellow')
            pt1_fin = np.dot(r_base.T,tt.qs[i1,j1])*1200+np.array([1000,1000,0])
            pt2_fin = np.dot(r_base.T,tt.qs[j1,i1])*1200+np.array([1000,1000,0])
            draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='yellow', outline='yellow')
            draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='yellow', outline='yellow')
    writeStaggeredText(txt, draw, i, speed=2)
    im.save(basedir + "im" + str(i) + ".png")

###############
## And join the three closest red points - missing.

'''
Scene 26
'''
txt = "Join the left edge\nto center of\nfront face of Tetrahedron."

for i in range(41):
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    s = 0.404508
    t = 0.0954913*min(1,i/30)
    tt = Tetartoid(s, 0)
    tt1 = Tetartoid(s, 0.0954913)
    tt2 = Tetartoid(s, t)
    tet = Tetrahedron()
    r_base = general_rotation(np.array([0.5,0.5,0.5]),2*np.pi*(367+50)/90)
    r_base_2 = general_rotation(np.dot(r_base.T,tet.vertices[3]), 2*np.pi*min(i,13)/90)
    r_base = np.dot(r_base, r_base_2)
    face1 = tet.planes[1]
    face1_cen = sum(tet.planes[1])/3
    p1 = min(1,(i+3)/34)
    p2 = min(1,(i+1)/34)
    face1_1 = face1*p1 + face1_cen*(1-p1)
    face1_2 = face1*p2 + face1_cen*(1-p2)
    render_solid_planes([face1_1], draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=False,trnsp=70,cut_back_face=False)
    render_solid_planes([face1_2], draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=False,trnsp=70,h=0,s=0,cut_back_face=False,rgb=(0,0,0))
    render_solid_planes([tet.planes[0]], draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=True,trnsp=0)
    #render_solid_planes(tt2.planes, draw, r_base, shift=np.array([1000, 1000, 0]),\
    #                scale=1200, make_edges=False,trnsp=125)
    render_solid_planes(tet.planes, draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=True,trnsp=0)
    p = 1.0
    cent_pt = (tet.vertices[0]+tet.vertices[2])/2*(1-p) + np.array([0,0,0])*p
    face2 = [tt1.qs[0,3], tt1.qs[3,0], tt1.qs[0,2]]
    render_solid_planes([face2], draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=True,cut_back_face=False,trnsp=int(200*34/34))
    face_cent = (tet.vertices[0]+tet.vertices[2]+tet.vertices[3])/3
    face3 = [tt1.qs[3,0], tt1.qs[0,2], face_cent]
    render_solid_planes([face3], draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=False,cut_back_face=False,trnsp=int(200*i/34))
    p = min(1,i/34)
    for i1 in range(3):
        pt1 = np.dot(r_base.T,face3[i1])*1200+np.array([1000,1000,0])
        pt2 = np.dot(r_base.T,face3[(i1+1)%3])*1200+np.array([1000,1000,0])
        pt2 = p*pt2+(1-p)*pt1
        draw.line((pt1[0],pt1[1],pt2[0],pt2[1]), fill = (0,0,255), width = 5)
    for i1 in range(4):
        for j1 in range(i1+1,4):
            if i1 == 0 and j1 == 3:
                pt1_fin = np.dot(r_base.T,tt1.qs[i1,j1])*1200+np.array([1000,1000,0])
                pt2_fin = np.dot(r_base.T,tt1.qs[j1,i1])*1200+np.array([1000,1000,0])
                draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='red', outline='yellow')
                draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='red', outline='yellow')
            if i1 == 0 and j1 == 2:
                pt1_fin = np.dot(r_base.T,tt1.qs[i1,j1])*1200+np.array([1000,1000,0])
                pt2_fin = np.dot(r_base.T,tt1.qs[j1,i1])*1200+np.array([1000,1000,0])
                draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='red', outline='yellow')
                draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='red', outline='yellow')
            pt1_fin = np.dot(r_base.T,tt.qs[i1,j1])*1200+np.array([1000,1000,0])
            pt2_fin = np.dot(r_base.T,tt.qs[j1,i1])*1200+np.array([1000,1000,0])
            draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='yellow', outline='yellow')
            draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='yellow', outline='yellow')
    writeStaggeredText(txt, draw, i, speed=2)
    im.save(basedir + "im" + str(i) + ".png")


'''
Scene 27
'''
txt = "Extend a line from body center to face center\nuntil the two planes become one."

for i in range(51):
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    s = 0.404508
    t = 0.0954913*min(1,i/30)
    tt = Tetartoid(s, 0)
    tt1 = Tetartoid(s, 0.0954913)
    tt2 = Tetartoid(s, t)
    tet = Tetrahedron()
    r_base = general_rotation(np.array([0.5,0.5,0.5]),2*np.pi*(367+50)/90)
    r_base_2 = general_rotation(np.dot(r_base.T,tet.vertices[3]), 2*np.pi*13/90)
    r_base = np.dot(r_base, r_base_2)
    render_solid_planes([tet.planes[0]], draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=True,trnsp=0)
    #render_solid_planes(tt1.planes, draw, r_base, shift=np.array([1000, 1000, 0]),\
    #                scale=1200, make_edges=False,trnsp=125)
    render_solid_planes(tet.planes, draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=True,trnsp=0)
    p = 1.0
    cent_pt = (tet.vertices[0]+tet.vertices[2])/2*(1-p) + np.array([0,0,0])*p
    face2 = [tt1.qs[0,3], tt1.qs[3,0], tt1.qs[0,2]]
    render_solid_planes([face2], draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=(i<30),cut_back_face=False,trnsp=int(200*34/34))
    face_cent = (tet.vertices[0]+tet.vertices[2]+tet.vertices[3])/3
    p = min(1,i/30)
    face_cent = face_cent*(1-p) + tt1.cs[1]*p
    face3 = [tt1.qs[3,0], tt1.qs[0,2], face_cent]
    render_solid_planes([face3], draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=(i<30),cut_back_face=False,trnsp=int(200*(0.5+0.5*min(i/30,1))))
    pt = np.dot(r_base.T,face_cent)*1200+np.array([1000,1000,0])
    draw.line((1000,1000,pt[0],pt[1]), fill = (255,255,255), width = 5)
    draw.ellipse((1000-10,1000-10,1000+10,1000+10),fill='purple', outline='blue')
    for i1 in range(4):
        for j1 in range(i1+1,4):
            if i1 == 0 and j1 == 3:
                pt1_fin = np.dot(r_base.T,tt1.qs[i1,j1])*1200+np.array([1000,1000,0])
                pt2_fin = np.dot(r_base.T,tt1.qs[j1,i1])*1200+np.array([1000,1000,0])
                draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='red', outline='yellow')
                draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='red', outline='yellow')
            if i1 == 0 and j1 == 2:
                pt1_fin = np.dot(r_base.T,tt1.qs[i1,j1])*1200+np.array([1000,1000,0])
                pt2_fin = np.dot(r_base.T,tt1.qs[j1,i1])*1200+np.array([1000,1000,0])
                draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='red', outline='yellow')
                draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='red', outline='yellow')
            pt1_fin = np.dot(r_base.T,tt.qs[i1,j1])*1200+np.array([1000,1000,0])
            pt2_fin = np.dot(r_base.T,tt.qs[j1,i1])*1200+np.array([1000,1000,0])
            draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='yellow', outline='yellow')
            draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='yellow', outline='yellow')
    writeStaggeredText(txt, draw, i, speed=2)
    im.save(basedir + "im" + str(i) + ".png")


'''
Scene 28
'''
txt = "And do the same thing with the bottom vertex."

for i in range(51):
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    s = 0.404508
    t = 0.0954913*min(1,i/30)
    tt = Tetartoid(s, 0)
    tt1 = Tetartoid(s, 0.0954913)
    tt2 = Tetartoid(s, t)
    tet = Tetrahedron()
    r_base = general_rotation(np.array([0.5,0.5,0.5]),2*np.pi*(367+50)/90)
    r_base_2 = general_rotation(np.dot(r_base.T,tet.vertices[3]), 2*np.pi*13/90)
    r_base = np.dot(r_base, r_base_2)
    render_solid_planes([tet.planes[0]], draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=True,trnsp=0)
    #render_solid_planes(tt1.planes, draw, r_base, shift=np.array([1000, 1000, 0]),\
    #                scale=1200, make_edges=False,trnsp=125)
    render_solid_planes(tet.planes, draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=True,trnsp=0)
    p = 1.0
    cent_pt = (tet.vertices[0]+tet.vertices[2])/2*(1-p) + np.array([0,0,0])*p
    face2 = [tt1.qs[0,3], tt1.qs[3,0], tt1.cs[1], tt1.qs[0,2]]
    render_solid_planes([face2], draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=False,cut_back_face=False,trnsp=int(200*34/34))
    vert = tet.vertices[0]
    p = min(1,i/40)
    vert = vert*(1-p) + tt1.vs[0]*p
    face3 = [tt1.qs[0,3], tt1.qs[0,2], vert]
    render_solid_planes([face3], draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=(i<30),cut_back_face=False,trnsp=int(200*(0.5+0.5*min(i/30,1))))
    pt = np.dot(r_base.T,vert)*1200+np.array([1000,1000,0])
    draw.line((1000,1000,pt[0],pt[1]), fill = (255,255,255), width = 5)
    draw.ellipse((1000-10,1000-10,1000+10,1000+10),fill='purple', outline='blue')
    for i1 in range(4):
        for j1 in range(i1+1,4):
            if i1 == 0 and j1 == 3:
                pt1_fin = np.dot(r_base.T,tt1.qs[i1,j1])*1200+np.array([1000,1000,0])
                pt2_fin = np.dot(r_base.T,tt1.qs[j1,i1])*1200+np.array([1000,1000,0])
                draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='red', outline='yellow')
                draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='red', outline='yellow')
            if i1 == 0 and j1 == 2:
                pt1_fin = np.dot(r_base.T,tt1.qs[i1,j1])*1200+np.array([1000,1000,0])
                pt2_fin = np.dot(r_base.T,tt1.qs[j1,i1])*1200+np.array([1000,1000,0])
                draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='red', outline='yellow')
                draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='red', outline='yellow')
            pt1_fin = np.dot(r_base.T,tt.qs[i1,j1])*1200+np.array([1000,1000,0])
            pt2_fin = np.dot(r_base.T,tt.qs[j1,i1])*1200+np.array([1000,1000,0])
            draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='yellow', outline='yellow')
            draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='yellow', outline='yellow')
    writeStaggeredText(txt, draw, i, speed=2)
    im.save(basedir + "im" + str(i) + ".png")


'''
Scene 29
'''
txt = "The pentagon here is regular."

for i in range(21):
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    s = 0.404508
    t = 0.0954913*min(1,i/30)
    tt = Tetartoid(s, 0)
    tt1 = Tetartoid(s, 0.0954913)
    tt2 = Tetartoid(s, t)
    tet = Tetrahedron()
    r_base = general_rotation(np.array([0.5,0.5,0.5]),2*np.pi*(367+50)/90)
    r_base_2 = general_rotation(np.dot(r_base.T,tet.vertices[3]), 2*np.pi*(13-min(i,11))/90)
    r_base = np.dot(r_base, r_base_2)
    render_solid_planes([tet.planes[0]], draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=True,trnsp=0)
    #render_solid_planes(tt1.planes, draw, r_base, shift=np.array([1000, 1000, 0]),\
    #                scale=1200, make_edges=False,trnsp=125)
    render_solid_planes(tet.planes, draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=True,trnsp=0)
    p = 1.0
    cent_pt = (tet.vertices[0]+tet.vertices[2])/2*(1-p) + np.array([0,0,0])*p
    face2 = [tt1.qs[0,3], tt1.qs[3,0], tt1.cs[1], tt1.qs[0,2], tt1.vs[0]]
    render_solid_planes([face2], draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=True,cut_back_face=False,trnsp=int(200*34/34))
    for i1 in range(4):
        for j1 in range(i1+1,4):
            if i1 == 0 and j1 == 3:
                pt1_fin = np.dot(r_base.T,tt1.qs[i1,j1])*1200+np.array([1000,1000,0])
                pt2_fin = np.dot(r_base.T,tt1.qs[j1,i1])*1200+np.array([1000,1000,0])
                draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='red', outline='yellow')
                draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='red', outline='yellow')
            if i1 == 0 and j1 == 2:
                pt1_fin = np.dot(r_base.T,tt1.qs[i1,j1])*1200+np.array([1000,1000,0])
                pt2_fin = np.dot(r_base.T,tt1.qs[j1,i1])*1200+np.array([1000,1000,0])
                draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='red', outline='yellow')
                draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='red', outline='yellow')
            pt1_fin = np.dot(r_base.T,tt.qs[i1,j1])*1200+np.array([1000,1000,0])
            pt2_fin = np.dot(r_base.T,tt.qs[j1,i1])*1200+np.array([1000,1000,0])
            draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='yellow', outline='yellow')
            draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='yellow', outline='yellow')
    writeStaggeredText(txt, draw, i, speed=2)
    writeStaggeredText("s = 0.404\nt = 0.095", draw, 100, speed=2,pos=(50,1000))
    im.save(basedir + "im" + str(i) + ".png")


'''
Scene 30
'''
txt = "But other values of s and t\ngive a wide range of pentagons."

for i in range(61):
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    if i < 40:
        s = 0.404508*zigzag2(i,100,120,70)/100.0
    else:
        s = 0.404508
    if i < 40:
        t = 0.0954913
    else:
        t = 0.0954913*(1-(i-40)/30)
    tt = Tetartoid(s, 0)
    tt1 = Tetartoid(s, t)
    tet = Tetrahedron()
    r_base = general_rotation(np.array([0.5,0.5,0.5]),2*np.pi*(367+50)/90)
    r_base_2 = general_rotation(np.dot(r_base.T,tet.vertices[3]), 2*np.pi*(13-11)/90)
    r_base = np.dot(r_base, r_base_2)
    render_solid_planes([tet.planes[0]], draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=True,trnsp=0)
    #render_solid_planes(tt1.planes, draw, r_base, shift=np.array([1000, 1000, 0]),\
    #                scale=1200, make_edges=False,trnsp=125)
    render_solid_planes(tet.planes, draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=True,trnsp=0)
    p = 1.0
    cent_pt = (tet.vertices[0]+tet.vertices[2])/2*(1-p) + np.array([0,0,0])*p
    face2 = [tt1.qs[0,3], tt1.qs[3,0], tt1.cs[1], tt1.qs[0,2], tt1.vs[0]]
    render_solid_planes([face2], draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=True,cut_back_face=False,trnsp=int(200*34/34))
    for i1 in range(4):
        for j1 in range(i1+1,4):
            if i1 == 0 and j1 == 3:
                pt1_fin = np.dot(r_base.T,tt1.qs[i1,j1])*1200+np.array([1000,1000,0])
                pt2_fin = np.dot(r_base.T,tt1.qs[j1,i1])*1200+np.array([1000,1000,0])
                draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='red', outline='yellow')
                draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='red', outline='yellow')
            if i1 == 0 and j1 == 2:
                pt1_fin = np.dot(r_base.T,tt1.qs[i1,j1])*1200+np.array([1000,1000,0])
                pt2_fin = np.dot(r_base.T,tt1.qs[j1,i1])*1200+np.array([1000,1000,0])
                draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='red', outline='yellow')
                draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='red', outline='yellow')
            pt1_fin = np.dot(r_base.T,tt.qs[i1,j1])*1200+np.array([1000,1000,0])
            pt2_fin = np.dot(r_base.T,tt.qs[j1,i1])*1200+np.array([1000,1000,0])
            draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='yellow', outline='yellow')
            draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='yellow', outline='yellow')
    writeStaggeredText(txt, draw, i, speed=2)
    writeStaggeredText("s = " +"%.4f" % round(s,4)+ "\nt = "+ "%.4f" % round(t,4), draw, 100, speed=2,pos=(50,1000))
    im.save(basedir + "im" + str(i) + ".png")


'''
Scene 31
'''
txt = "We could construct the other faces\nin a similar manner\nbut lets use rotational symmetry."

for i in range(63):
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    s = 0.404508
    t = 0.0954913/3
    tt = Tetartoid(s, 0)
    tt1 = Tetartoid(s, t)
    tet = Tetrahedron()
    r_base = general_rotation(np.array([0.5,0.5,0.5]),2*np.pi*(367+50-min(i,57) )/90)
    r_base_2 = general_rotation(np.dot(r_base.T,tet.vertices[3]), 2*np.pi*(2-min(i/10,2))/90)
    #rot = tetrahedral_rotations(i/40)[0]
    r_base_old = np.dot(r_base, r_base_2)
    r_base = r_base_old
    #r_base = np.dot(r_base_old, rot)
    #render_solid_planes(tt1.planes, draw, r_base, shift=np.array([1000, 1000, 0]),\
    #                scale=1200, make_edges=False,trnsp=125)
    render_solid_planes(tet.planes, draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=True,trnsp=0)
    p = 1.0
    cent_pt = (tet.vertices[0]+tet.vertices[2])/2*(1-p) + np.array([0,0,0])*p
    face2 = [tt1.qs[0,3], tt1.qs[3,0], tt1.cs[1], tt1.qs[0,2], tt1.vs[0]]
    render_solid_planes([face2], draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=True,cut_back_face=False,trnsp=int(200*34/34))
    #render_solid_planes([face2], draw, r_base_old, shift=np.array([1000, 1000, 0]),\
    #                scale=1200, make_edges=True,cut_back_face=False,trnsp=int(200*34/34))
    for i1 in range(4):
        for j1 in range(i1+1,4):
            if i1 == 0 and j1 == 3:
                pt1_fin = np.dot(r_base.T,tt1.qs[i1,j1])*1200+np.array([1000,1000,0])
                pt2_fin = np.dot(r_base.T,tt1.qs[j1,i1])*1200+np.array([1000,1000,0])
                draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='red', outline='yellow')
                draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='red', outline='yellow')
            if i1 == 0 and j1 == 2:
                pt1_fin = np.dot(r_base.T,tt1.qs[i1,j1])*1200+np.array([1000,1000,0])
                pt2_fin = np.dot(r_base.T,tt1.qs[j1,i1])*1200+np.array([1000,1000,0])
                draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='red', outline='yellow')
                draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='red', outline='yellow')
            pt1_fin = np.dot(r_base.T,tt.qs[i1,j1])*1200+np.array([1000,1000,0])
            pt2_fin = np.dot(r_base.T,tt.qs[j1,i1])*1200+np.array([1000,1000,0])
            draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='yellow', outline='yellow')
            draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='yellow', outline='yellow')
    writeStaggeredText(txt, draw, i, speed=2)
    writeStaggeredText("s = " +"%.4f" % round(s,4)+ "\nt = "+ "%.4f" % round(t,4), draw, 100, speed=2,pos=(50,1000))
    im.save(basedir + "im" + str(i) + ".png")


'''
Scene 32
'''
txt = "Certain rotations preserve the orientation\nof the Tetrahedron."

for i in range(26):
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    s = 0.404508
    t = 0.0954913/3
    tt = Tetartoid(s, 0)
    tt1 = Tetartoid(s, t)
    tet = Tetrahedron()
    rot = tetrahedral_rotations(min(1,i/20))[0]
    r_base_old = np.eye(3)
    r_base = np.dot(r_base_old, rot)
    #render_solid_planes(tt1.planes, draw, r_base, shift=np.array([1000, 1000, 0]),\
    #                scale=1200, make_edges=False,trnsp=125)
    render_solid_planes(tet.planes, draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=True,trnsp=0)
    p = 1.0
    cent_pt = (tet.vertices[0]+tet.vertices[2])/2*(1-p) + np.array([0,0,0])*p
    face2 = [tt1.qs[0,3], tt1.qs[3,0], tt1.cs[1], tt1.qs[0,2], tt1.vs[0]]
    render_solid_planes([face2], draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=True,cut_back_face=False,trnsp=int(200*34/34))
    #render_solid_planes([face2], draw, r_base_old, shift=np.array([1000, 1000, 0]),\
    #                scale=1200, make_edges=True,cut_back_face=False,trnsp=int(200*34/34))
    for i1 in range(4):
        for j1 in range(i1+1,4):
            if i1 == 0 and j1 == 3:
                pt1_fin = np.dot(r_base.T,tt1.qs[i1,j1])*1200+np.array([1000,1000,0])
                pt2_fin = np.dot(r_base.T,tt1.qs[j1,i1])*1200+np.array([1000,1000,0])
                draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='red', outline='yellow')
                draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='red', outline='yellow')
            if i1 == 0 and j1 == 2:
                pt1_fin = np.dot(r_base.T,tt1.qs[i1,j1])*1200+np.array([1000,1000,0])
                pt2_fin = np.dot(r_base.T,tt1.qs[j1,i1])*1200+np.array([1000,1000,0])
                draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='red', outline='yellow')
                draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='red', outline='yellow')
            pt1_fin = np.dot(r_base.T,tt.qs[i1,j1])*1200+np.array([1000,1000,0])
            pt2_fin = np.dot(r_base.T,tt.qs[j1,i1])*1200+np.array([1000,1000,0])
            draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='yellow', outline='yellow')
            draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='yellow', outline='yellow')
    writeStaggeredText(txt, draw, i, speed=2)
    #writeStaggeredText("s = " +"%.4f" % round(s,4)+ "\nt = "+ "%.4f" % round(t,4), draw, 100, speed=2,pos=(50,1000))
    im.save(basedir + "im" + str(i) + ".png")


'''
Scene 33
'''
txt = "Certain rotations preserve the orientation\nof the Tetrahedron."

for i in range(26):
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    s = 0.404508
    t = 0.0954913/3
    tt = Tetartoid(s, 0)
    tt1 = Tetartoid(s, t)
    tet = Tetrahedron()
    rot = tetrahedral_rotations(max(0,1-i/20))[0]
    r_base_old = np.eye(3)
    r_base = np.dot(r_base_old, rot)
    #render_solid_planes(tt1.planes, draw, r_base, shift=np.array([1000, 1000, 0]),\
    #                scale=1200, make_edges=False,trnsp=125)
    render_solid_planes(tet.planes, draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=True,trnsp=0)
    p = 1.0
    cent_pt = (tet.vertices[0]+tet.vertices[2])/2*(1-p) + np.array([0,0,0])*p
    face2 = [tt1.qs[0,3], tt1.qs[3,0], tt1.cs[1], tt1.qs[0,2], tt1.vs[0]]
    render_solid_planes([face2], draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=True,cut_back_face=False,trnsp=int(200*34/34))
    #render_solid_planes([face2], draw, r_base_old, shift=np.array([1000, 1000, 0]),\
    #                scale=1200, make_edges=True,cut_back_face=False,trnsp=int(200*34/34))
    for i1 in range(4):
        for j1 in range(i1+1,4):
            if i1 == 0 and j1 == 3:
                pt1_fin = np.dot(r_base.T,tt1.qs[i1,j1])*1200+np.array([1000,1000,0])
                pt2_fin = np.dot(r_base.T,tt1.qs[j1,i1])*1200+np.array([1000,1000,0])
                draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='red', outline='yellow')
                draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='red', outline='yellow')
            if i1 == 0 and j1 == 2:
                pt1_fin = np.dot(r_base.T,tt1.qs[i1,j1])*1200+np.array([1000,1000,0])
                pt2_fin = np.dot(r_base.T,tt1.qs[j1,i1])*1200+np.array([1000,1000,0])
                draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='red', outline='yellow')
                draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='red', outline='yellow')
            pt1_fin = np.dot(r_base.T,tt.qs[i1,j1])*1200+np.array([1000,1000,0])
            pt2_fin = np.dot(r_base.T,tt.qs[j1,i1])*1200+np.array([1000,1000,0])
            draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='yellow', outline='yellow')
            draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='yellow', outline='yellow')
    writeStaggeredText(txt, draw, 100, speed=2)
    #writeStaggeredText("s = " +"%.4f" % round(s,4)+ "\nt = "+ "%.4f" % round(t,4), draw, 100, speed=2,pos=(50,1000))
    im.save(basedir + "im" + str(i) + ".png")



'''
Scene 34
'''
txt = "If we duplicate the pentagons\nwe start getting the other\nfaces of the Tetartoid."

for j in range(11):
    for i in range(11):
        im = Image.new("RGB", (2048, 2048), (1,1,1))
        draw = ImageDraw.Draw(im,'RGBA')
        s = 0.404508
        t = 0.0954913/3
        tt = Tetartoid(s, 0)
        tt1 = Tetartoid(s, t)
        tet = Tetrahedron()
        rot = tetrahedral_rotations(min(1,i/10))[j]
        r_base_old = np.eye(3)
        r_base = np.dot(r_base_old, rot)
        #render_solid_planes(tt1.planes, draw, r_base, shift=np.array([1000, 1000, 0]),\
        #                scale=1200, make_edges=False,trnsp=125)
        render_solid_planes(tet.planes, draw, r_base, shift=np.array([1000, 1000, 0]),\
                        scale=1200, make_edges=True,trnsp=0)
        p = 1.0
        cent_pt = (tet.vertices[0]+tet.vertices[2])/2*(1-p) + np.array([0,0,0])*p
        face2 = [tt1.qs[0,3], tt1.qs[3,0], tt1.cs[1], tt1.qs[0,2], tt1.vs[0]]
        render_solid_planes([face2], draw, r_base, shift=np.array([1000, 1000, 0]),\
                        scale=1200, make_edges=True,cut_back_face=False,trnsp=int(200*34/34))
        render_solid_planes([face2], draw, r_base_old, shift=np.array([1000, 1000, 0]),\
                        scale=1200, make_edges=True,cut_back_face=False,trnsp=200)
        for k in range(j):
            rot1 = tetrahedral_rotations()[k]
            render_solid_planes([face2], draw, rot1, shift=np.array([1000, 1000, 0]),\
                        scale=1200, make_edges=True,cut_back_face=False,trnsp=200)
        for i1 in range(4):
            for j1 in range(i1+1,4):
                if i1 == 0 and j1 == 3:
                    pt1_fin = np.dot(r_base.T,tt1.qs[i1,j1])*1200+np.array([1000,1000,0])
                    pt2_fin = np.dot(r_base.T,tt1.qs[j1,i1])*1200+np.array([1000,1000,0])
                    draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='red', outline='yellow')
                    draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='red', outline='yellow')
                if i1 == 0 and j1 == 2:
                    pt1_fin = np.dot(r_base.T,tt1.qs[i1,j1])*1200+np.array([1000,1000,0])
                    pt2_fin = np.dot(r_base.T,tt1.qs[j1,i1])*1200+np.array([1000,1000,0])
                    draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='red', outline='yellow')
                    draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='red', outline='yellow')
                pt1_fin = np.dot(r_base.T,tt.qs[i1,j1])*1200+np.array([1000,1000,0])
                pt2_fin = np.dot(r_base.T,tt.qs[j1,i1])*1200+np.array([1000,1000,0])
                draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='yellow', outline='yellow')
                draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='yellow', outline='yellow')
        writeStaggeredText(txt, draw, j*11+i, speed=2)
        im.save(basedir + "im" + str(j*11+i) + ".png")

'''
Scene 35
'''
txt = "We already saw how t=0\ngives back the Tetrahedron."

for i in range(35):
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    s = 0.404508
    t = 0.0954913/3*(1-min(i,20)/20)
    tt = Tetartoid(s, 0)
    tt1 = Tetartoid(s, t)
    tet = Tetrahedron()
    r_base = general_rotation(tet.vertices[3], 2*np.pi*(i+30)/90)
    render_solid_planes(tt1.planes, draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=False,trnsp=200)
    render_solid_planes(tet.planes, draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=True,trnsp=0)
    for i1 in range(4):
        for j1 in range(i1+1,4):
            if i1 == 0 and j1 == 3:
                pt1_fin = np.dot(r_base.T,tt1.qs[i1,j1])*1200+np.array([1000,1000,0])
                pt2_fin = np.dot(r_base.T,tt1.qs[j1,i1])*1200+np.array([1000,1000,0])
                draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='red', outline='yellow')
                draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='red', outline='yellow')
            if i1 == 0 and j1 == 2:
                pt1_fin = np.dot(r_base.T,tt1.qs[i1,j1])*1200+np.array([1000,1000,0])
                pt2_fin = np.dot(r_base.T,tt1.qs[j1,i1])*1200+np.array([1000,1000,0])
                draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='red', outline='yellow')
                draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='red', outline='yellow')
            pt1_fin = np.dot(r_base.T,tt.qs[i1,j1])*1200+np.array([1000,1000,0])
            pt2_fin = np.dot(r_base.T,tt.qs[j1,i1])*1200+np.array([1000,1000,0])
            draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='yellow', outline='yellow')
            draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='yellow', outline='yellow')
    writeStaggeredText(txt, draw, i, speed=2)
    writeStaggeredText("s = " +"%.4f" % round(s,4)+ "\nt = "+ "%.4f" % round(t,4), draw, 100, speed=2,pos=(50,1000))
    im.save(basedir + "im" + str(i) + ".png")



'''
Scene 36
'''
txt = "And these special values\ngive us the Dodecahedron."

for i in range(35):
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    s = 0.404508
    t = 0.0954913*(min(i,20)/20)
    tt = Tetartoid(s, 0)
    tt1 = Tetartoid(s, t)
    tet = Tetrahedron()
    r_base = general_rotation(tet.vertices[3], 2*np.pi*(i+30+27)/90)
    render_solid_planes(tt1.planes, draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=False,trnsp=200)
    render_solid_planes(tet.planes, draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=True,trnsp=0)
    for i1 in range(4):
        for j1 in range(i1+1,4):
            if i1 == 0 and j1 == 3:
                pt1_fin = np.dot(r_base.T,tt1.qs[i1,j1])*1200+np.array([1000,1000,0])
                pt2_fin = np.dot(r_base.T,tt1.qs[j1,i1])*1200+np.array([1000,1000,0])
                draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='red', outline='yellow')
                draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='red', outline='yellow')
            if i1 == 0 and j1 == 2:
                pt1_fin = np.dot(r_base.T,tt1.qs[i1,j1])*1200+np.array([1000,1000,0])
                pt2_fin = np.dot(r_base.T,tt1.qs[j1,i1])*1200+np.array([1000,1000,0])
                draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='red', outline='yellow')
                draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='red', outline='yellow')
            pt1_fin = np.dot(r_base.T,tt.qs[i1,j1])*1200+np.array([1000,1000,0])
            pt2_fin = np.dot(r_base.T,tt.qs[j1,i1])*1200+np.array([1000,1000,0])
            draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='yellow', outline='yellow')
            draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='yellow', outline='yellow')
    writeStaggeredText(txt, draw, i, speed=2)
    writeStaggeredText("s = " +"%.4f" % round(s,4)+ "\nt = "+ "%.4f" % round(t,4), draw, 100, speed=2,pos=(50,1000))
    im.save(basedir + "im" + str(i) + ".png")



'''
Scene 37
'''
txt = "s = 0.33 and t = 0.33 gives us the cube."

for i in range(45):
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    p = min(1,i/30)
    s = 0.404508*(1-p)+0.33*p
    t = 0.0954913*(1-p)+0.33*p
    tt = Tetartoid(s, 0)
    tt1 = Tetartoid(s, t)
    tet = Tetrahedron()
    r_base = general_rotation(tet.vertices[3], 2*np.pi*(i+30+27+34)/90)
    render_solid_planes(tt1.planes, draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=True,trnsp=200)
    render_solid_planes(tet.planes, draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=True,trnsp=0)
    for i1 in range(4):
        for j1 in range(i1+1,4):
            if i1 == 0 and j1 == 3:
                pt1_fin = np.dot(r_base.T,tt1.qs[i1,j1])*1200+np.array([1000,1000,0])
                pt2_fin = np.dot(r_base.T,tt1.qs[j1,i1])*1200+np.array([1000,1000,0])
                draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='red', outline='yellow')
                draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='red', outline='yellow')
            if i1 == 0 and j1 == 2:
                pt1_fin = np.dot(r_base.T,tt1.qs[i1,j1])*1200+np.array([1000,1000,0])
                pt2_fin = np.dot(r_base.T,tt1.qs[j1,i1])*1200+np.array([1000,1000,0])
                draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='red', outline='yellow')
                draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='red', outline='yellow')
            pt1_fin = np.dot(r_base.T,tt.qs[i1,j1])*1200+np.array([1000,1000,0])
            pt2_fin = np.dot(r_base.T,tt.qs[j1,i1])*1200+np.array([1000,1000,0])
            draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='yellow', outline='yellow')
            draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='yellow', outline='yellow')
    writeStaggeredText(txt, draw, i, speed=2)
    writeStaggeredText("s = " +"%.4f" % round(s,4)+ "\nt = "+ "%.4f" % round(t,4), draw, 100, speed=2,pos=(50,1000))
    im.save(basedir + "im" + str(i) + ".png")


'''
Scene 38
'''
txt = "Stays a cube"

for i in range(45):
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    s = zigzag2(i,33,45,20)/100
    t = zigzag2(i,33,45,20)/100
    tt = Tetartoid(s, 0)
    tt1 = Tetartoid(s, t)
    tet = Tetrahedron()
    r_base = general_rotation(tet.vertices[3], 2*np.pi*(i+30+27+34+34+44)/90)
    render_solid_planes(tt1.planes, draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=True,trnsp=200)
    render_solid_planes(tet.planes, draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=True,trnsp=0)
    for i1 in range(4):
        for j1 in range(i1+1,4):
            if i1 == 0 and j1 == 3:
                pt1_fin = np.dot(r_base.T,tt1.qs[i1,j1])*1200+np.array([1000,1000,0])
                pt2_fin = np.dot(r_base.T,tt1.qs[j1,i1])*1200+np.array([1000,1000,0])
                draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='red', outline='yellow')
                draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='red', outline='yellow')
            if i1 == 0 and j1 == 2:
                pt1_fin = np.dot(r_base.T,tt1.qs[i1,j1])*1200+np.array([1000,1000,0])
                pt2_fin = np.dot(r_base.T,tt1.qs[j1,i1])*1200+np.array([1000,1000,0])
                draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='red', outline='yellow')
                draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='red', outline='yellow')
            pt1_fin = np.dot(r_base.T,tt.qs[i1,j1])*1200+np.array([1000,1000,0])
            pt2_fin = np.dot(r_base.T,tt.qs[j1,i1])*1200+np.array([1000,1000,0])
            draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='yellow', outline='yellow')
            draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='yellow', outline='yellow')
    writeStaggeredText(txt, draw, i, speed=2)
    writeStaggeredText("s = " +"%.4f" % round(s,4)+ "\nt = "+ "%.4f" % round(t,4), draw, 100, speed=2,pos=(50,1000))
    im.save(basedir + "im" + str(i) + ".png")



'''
Scene 39
'''
txt = "Subscribe for more :)"

for i in range(45):
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    s = zigzag2(i,33,45,20)/100
    t = zigzag2(-i,33,45,20)/100
    tt = Tetartoid(s, 0)
    tt1 = Tetartoid(s, t)
    tet = Tetrahedron()
    r_base = general_rotation(tet.vertices[3], 2*np.pi*(i+30+27+34+34+44+44)/90)
    render_solid_planes(tt1.planes, draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=True,trnsp=200)
    render_solid_planes(tet.planes, draw, r_base, shift=np.array([1000, 1000, 0]),\
                    scale=1200, make_edges=True,trnsp=0)
    for i1 in range(4):
        for j1 in range(i1+1,4):
            if i1 == 0 and j1 == 3:
                pt1_fin = np.dot(r_base.T,tt1.qs[i1,j1])*1200+np.array([1000,1000,0])
                pt2_fin = np.dot(r_base.T,tt1.qs[j1,i1])*1200+np.array([1000,1000,0])
                draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='red', outline='yellow')
                draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='red', outline='yellow')
            if i1 == 0 and j1 == 2:
                pt1_fin = np.dot(r_base.T,tt1.qs[i1,j1])*1200+np.array([1000,1000,0])
                pt2_fin = np.dot(r_base.T,tt1.qs[j1,i1])*1200+np.array([1000,1000,0])
                draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='red', outline='yellow')
                draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='red', outline='yellow')
            pt1_fin = np.dot(r_base.T,tt.qs[i1,j1])*1200+np.array([1000,1000,0])
            pt2_fin = np.dot(r_base.T,tt.qs[j1,i1])*1200+np.array([1000,1000,0])
            draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='yellow', outline='yellow')
            draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='yellow', outline='yellow')
    writeStaggeredText(txt, draw, i, speed=2)
    #writeStaggeredText("s = " +"%.4f" % round(s,4)+ "\nt = "+ "%.4f" % round(t,4), draw, 100, speed=2,pos=(50,1000))
    im.save(basedir + "im" + str(i) + ".png")



# Convert to video and gif.
#ffmpeg -framerate 10 -f image2 -i im%d.png -vb 20M vid.avi
#ffmpeg -i vid.avi -pix_fmt rgb24 -loop 0 out.gif

for i in range(51):
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    s = 0.4
    t = 0.33
    tt = Tetartoid(s, t)
    r_base = general_rotation(np.array([0.5,0.5,0.5]),2*np.pi*(317+i)/90)
    tt.render_solid_planes(draw, r_base, shift=np.array([1000, 1000, 0]), scale=1200)
    im.save(basedir + "im" + str(i) + ".png")


for ed in tet.edges:
        pt1 = ed[0]*s+ed[1]*(1-s)
        pt2 = ed[1]*s+ed[0]*(1-s)
        pt1_fin = np.dot(r_base.T,pt1)*1200+np.array([1000,1000,0])
        pt2_fin = np.dot(r_base.T,pt2)*1200+np.array([1000,1000,0])
        draw.ellipse((pt1_fin[0]-5, pt1_fin[1]-5, pt1_fin[0]+5, pt1_fin[1]+5),fill='yellow', outline='yellow')
        draw.ellipse((pt2_fin[0]-5, pt2_fin[1]-5, pt2_fin[0]+5, pt2_fin[1]+5),fill='yellow', outline='yellow')


