import numpy as np
from pyray.shapes.twod.paraboloid import *
from pyray.shapes.twod.functional import *
from pyray.rotation import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib as mpl


basedir = '.\\images\\RotatingCube\\'

def draw_cubic():
    fn = lambda x,y: x**3+y**3
    for i in range(20):
        im = Image.new("RGB", (2048, 2048), "black")
        draw = ImageDraw.Draw(im, 'RGBA')
        r = general_rotation(np.array([1,0,0]),np.pi/120*i)
        #drawFunctionalXYGridInCircle(draw, r, fn=fn, scale=10.0)
        im.save(basedir + 'im' + str(i) + '.png')


def three_d_grid():
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    # Make data.
    X = np.arange(-5, 5, 0.25)
    Y = np.arange(-5, 5, 0.25)
    X, Y = np.meshgrid(X, Y)
    R = (X**3 + Y**3)
    Z = R

    # Plot the surface.
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                        linewidth=0, antialiased=False)

    # Customize the z axis.
    #ax.set_zlim(-1.01, 1.01)
    #ax.zaxis.set_major_locator(LinearLocator(10))
    #ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()


mpl.rcParams['legend.fontsize'] = 10

fig = plt.figure()
ax = fig.gca(projection='3d')
theta = np.linspace(0, 2 * np.pi, 100)

for r in np.arange(0.1,1.0,0.1):
    #r = 1.0
    x = r * np.sin(theta)
    y = r * np.cos(theta)
    z = x**3+y**3
    ax.plot(x, y, z, label='parametric curve')
    #ax.legend()

plt.show()


def paraboloid_w_grad(im_ind=0, scale=200, shift=np.array([1000,1000,0]), opacity=60,
                    basepath='.\\'):
    r1 = np.eye(4)
    rot = general_rotation(np.array([0,0,1]), np.pi/20.0 * (8 + im_ind/3.0))
    j=4
    r = rotation(3, 2 * np.pi* j /30.0)
    rr = general_rotation(np.array([0,1,0]), np.pi/20.0 * (im_ind/7.0))
    r = np.dot(r,rr)
    r = np.dot(r, rot)
    r1[:3,:3] = r
    im = Image.new("RGB", (2048, 2048), "black")
    draw = ImageDraw.Draw(im, 'RGBA')
    render_scene_4d_axis(draw, r1, 4, scale, shift)
    for z in np.arange(0.001, 3.5, 0.02):
        point1 = np.array([np.sqrt(z),0,z])
        generalized_arc(draw, r, center=np.array([0,0,z]), vec=np.array([0,0,1]), 
                        point=point1, radius=np.sqrt(z), prcnt=1.0, 
                        rgba=(255,20,147,50))
    xax1=np.array([-100.0,0,0.0]);xax1=np.dot(r,xax1)*scale+shift
    xax2=np.array([100.0,0,0.0]);xax2=np.dot(r,xax2)*scale+shift
    draw.line((xax1[0], xax1[1], xax2[0], xax2[1]), fill=(255,255,0), width=4)
    xax1=np.array([0.0,-100,0.0]);xax1=np.dot(r,xax1)*scale+shift
    xax2=np.array([0.0,100,0.0]);xax2=np.dot(r,xax2)*scale+shift
    draw.line((xax1[0], xax1[1], xax2[0], xax2[1]), fill=(255,255,0), width=4)
    gradients(draw,r)
    pt = shift
    draw.ellipse((pt[0]-10, pt[1]-10, pt[0]+10, pt[1]+10), fill = (0,255,0))
    draw_paraboloid_plane(draw,r,3.3)
    draw_paraboloid_plane(draw,r,2.0,extent=1.4)
    draw_paraboloid_plane(draw,r,1.0,extent=1.0)
    im.save(basepath + 'im' + str(im_ind) + '.png')


def gradients(draw,r):
    #for z in [0.3,1.3,2.3,3.3]:
    for z in [3.3,2.0,1.0]:
        x = np.sqrt(z)
        for x in np.arange(-x,x,x/2):
            y = np.sqrt(z-x*x)
            arrowV1(draw,r,np.array([y,x,z]), np.array([1.5*y,1.5*x,z]), (204,102,255))
            if z>3.0:
                arrowV1(draw,r,np.array([-y,x,z]), np.array([-1.5*y,1.5*x,z]), (204,102,255))


def draw_paraboloid_plane(draw,r,z=3.3,scale=200,shift=np.array([1000,1000,0]),extent=2):
    pt1=np.array([extent,extent,z]);pt1=np.dot(r,pt1)*scale+shift
    pt2=np.array([extent,-extent,z]);pt2=np.dot(r,pt2)*scale+shift
    pt3=np.array([-extent,-extent,z]);pt3=np.dot(r,pt3)*scale+shift
    pt4=np.array([-extent,extent,z]);pt4=np.dot(r,pt4)*scale+shift
    draw.polygon([(pt1[0], pt1[1]), (pt2[0], pt2[1]), (pt3[0], pt3[1]), (pt4[0], pt4[1])],\
                    (0,102,255,50))
    point1 = np.array([np.sqrt(z),0,z])
    generalized_arc(draw, r, center=np.array([0,0,z]), vec=np.array([0,0,1]), 
                        point=point1, radius=np.sqrt(z), prcnt=1.0,scale=scale,
                        rgba=(255,20,10,100),width=10)


def plane_w_arrows(im_ind=0, scale=200,\
                    shift=np.array([824,824,0]),\
                    basepath='.\\'):
    r1 = np.eye(4)
    rot = general_rotation(np.array([0,0,1]), np.pi/20.0*(8 + im_ind/3.0))
    j=4
    r = rotation(3, 2*np.pi*j/30.0)
    rr = general_rotation(np.array([0,1,0]), np.pi/20.0*(im_ind/7.0))
    r = np.dot(r,rr)
    r = np.dot(r, rot)
    r1[:3,:3] = r
    im = Image.new("RGB", (1648, 1648), "black")
    draw = ImageDraw.Draw(im, 'RGBA')
    pt1 = 3*np.array([1.0,-1.0,0]); pt2 = 3*np.array([1.0,1.0,0])
    z = 1.2**2+1
    pt3 = 3*np.array([-1.0,1.0,0]); pt4 = 3*np.array([-1.0,-1.0,0])
    pt1 = np.dot(r,pt1)*scale+shift; pt2 = np.dot(r,pt2)*scale+shift
    pt3 = np.dot(r,pt3)*scale+shift; pt4 = np.dot(r,pt4)*scale+shift
    draw.polygon([(pt1[0], pt1[1]), (pt2[0], pt2[1]), (pt3[0], pt3[1]), (pt4[0], pt4[1])],\
                    (0,102,255,50))
    
    draw_arrows(draw,r,rgba=(255,250,47),shift=shift)
    draw_arrows(draw,r,rot_angl=np.pi/2.0, rgba=(73,200,250),shift=shift)
    draw_arrows(draw,r,rot_angl=np.pi/2.0+np.pi/3, rgba=(255,20,147),shift=shift)

    arrowV1(draw,r,np.array([0,0,0]), np.array([0,0,2.5]), shift=shift,rgb=(20,200,25))
    arrowV1(draw,r,np.array([0,0,0]), np.array([0,0,-2.5]), shift=shift,rgb=(255,20,25))
    im.save(basepath + 'im' + str(im_ind) + '.png')


def draw_arrows(draw,r,rot_angl=np.pi/6.0,rgba=(255,20,147),shift=np.array([1000,1000,0])):
    base = np.array([0,0,1.5])
    for theta in np.arange(0,np.pi*2,2*np.pi/3):
        a = np.array([np.cos(theta),np.sin(theta),0])
        rr = general_rotation(a, rot_angl)
        arrow1 = np.dot(rr,base)
        arrowV1(draw,r,np.array([0,0,0]), arrow1, rgb=rgba,shift=shift)
    rgba = rgba+(150,)
    generalized_arc(draw, r, center=np.array([0,0,1.5*np.cos(rot_angl)]),
                        vec=np.array([0,0,1]),
                        point=1.5*np.array([0,np.sin(rot_angl),np.cos(rot_angl)]), 
                        radius=100, prcnt=1.0,
                        rgba=rgba,shift=shift)


#####################
## Paraboloid with Lagrange visualized.

im = Image.new("RGB", (2048, 2048), (1, 1, 1))
draw = ImageDraw.Draw(im, 'RGBA')

scale=5.0; ind=0; sep = 24; i = 2.0; base_coeff = 0.02; start_line = -12.0
shift = np.array([1000.0, 1000.0, 0.0])

r1 = np.eye(4); j=24
r = rotation(3, np.pi/30*j)
r1[:3,:3] = r

render_scene_4d_axis(draw, r1, 4)

fn = lambda x, y : paraboloid(x, y, coeff=i*base_coeff, intercept=i)

drawFunctionalXYGrid(draw, r, scale=scale, fn=fn, 
                extent=60, rgba2=(255,20,147,80),
                saperatingPlane=np.array([-1,-1,sep]))

three_d_parabola(draw, r, r2)

im.save(basedir + 'im' + str(0) + '.png')


