import math
from scipy.spatial import ConvexHull

from pyray.shapes.oned.circle import *
from pyray.axes import *
from pyray.shapes.twod.plane import *
from pyray.shapes.twod.functional import *


def paraboloid_circles_rotatingplane(basepath='.\\', scale=200, shift=np.array([1000,1000,0])):
    im_ind = 0
    for i in (np.concatenate((np.arange(0.5,1,0.01), np.arange(1,3,0.05),np.arange(3,10,0.6)),axis=0) + 1e-4): #Controls the rotation of the plane.
        r2 = general_rotation(np.array([.3, .3, .3]), np.pi/i)
        r1 = np.eye(4)
        orthogonal_vec = np.dot(r2, np.array([0,1,0]))
        orthogonal_vec = orthogonal_vec/sum(orthogonal_vec**2) # Should be unnecessary since rotation doesn't change magnitude.
        for j in range(4,5): # Controls the rotation of the paraboloid.
            r = rotation(3, 2*np.pi*j/30.0)
            r1[:3,:3] = r
            im = Image.new("RGB", (2048, 2048), "black")
            draw = ImageDraw.Draw(im, 'RGBA')
            translate = np.array([0,0,1.5])
            rotated_xz_plane(draw, r, r2, scale, shift, translate)
            render_scene_4d_axis(draw, r1, 4)
            for z in np.arange(0.001, 3.5, 0.01):
                #generalized_circle(draw, np.array([0,0,z]), np.array([0,0,1]), np.sqrt(z), r, rgba = (255,20,147,50))
                #generalized_arc(draw, r, np.array([0,0,z]), np.array([0,0,1]), np.array([np.sqrt(z),0,z]), np.sqrt(z), 0.5, (255,20,147,50))
                #generalized_arc(draw, r, np.array([0,0,z]), np.array([0,0,1]), np.array([-np.sqrt(z),0,z]), np.sqrt(z), 0.5, (255,20,147,10))
                pt1 = np.dot(r, np.array([-np.sqrt(z),0,z]))
                theta = np.pi * 2.0 / 180.0
                rot = general_rotation(np.dot(r,np.array([0,0,1])),theta)
                for j in range(0,180):
                    pt2 = np.dot(rot, pt1)
                    pt2Orig = np.dot(np.transpose(r),pt2)
                    if sum(pt2Orig * orthogonal_vec) - 1.5*orthogonal_vec[2] > 0:
                        draw.line((pt1[0]*scale + shift[0], pt1[1]*scale+shift[1], pt2[0]*scale+shift[0], pt2[1]*scale+shift[1]),\
                             fill=(255,20,147,100), width=5)
                    else:
                        draw.line((pt1[0]*scale + shift[0], pt1[1]*scale+shift[1], pt2[0]*scale+shift[0], pt2[1]*scale+shift[1]),\
                             fill=(255,20,147,40), width=5)
                    pt1 = pt2
            three_d_parabola(draw, r, r2)
            im.save(basepath + 'im' + str(im_ind) + '.png')
            im_ind = im_ind + 1


def paraboloid_circles(basepath='.\\', scale=200, shift=np.array([1000,1000,0])):
    r2=general_rotation(np.array([0,0,1]),np.pi/2)
    orthogonal_vec = np.dot(r2, np.array([0,1,0]))
    r = rotation(3, 2*np.pi*4/30.0)
    r1 = np.eye(4)
    r1[:3,:3] = r
    im = Image.new("RGB", (2048, 2048), "black")
    draw = ImageDraw.Draw(im, 'RGBA')
    translate = np.array([0,1.5,0])

    #rotated_xz_plane(draw, r, r2, scale, shift, translate=translate)
    render_scene_4d_axis(draw, r1, 4)
    for z in np.arange(0.001, 3.5, 0.01):
        generalized_arc(draw, r, np.array([0,0,z]), np.array([0,0,1]), np.array([np.sqrt(z),0,z]), 
                        np.sqrt(z), 0.5, (255,20,147,50))
        generalized_arc(draw, r, np.array([0,0,z]), np.array([0,0,1]), np.array([-np.sqrt(z),0,z]), 
                        np.sqrt(z), 0.5, (255,20,147,10))
    three_d_parabola(draw, r, r2)
    im.save(basepath + 'im' + str(0) + '.png')


def paraboloid_dirty(im_ind=0, scale=200, shift=np.array([1000,1000,0]), opacity=60,
                    basepath='.\\'):
    #i=1
    #r2 = general_rotation(np.array([.3, .3, .3]), np.pi/i)
    r1 = np.eye(4)
    rot = general_rotation(np.array([0,0,1]), np.pi/20.0 * (8 + im_ind/3.0))
    j=4
    #r = rotation(3, 2 * np.pi* j /30.0)
    r=np.eye(3)
    rr = general_rotation(np.array([0,1,0]), np.pi/20.0 * (im_ind/7.0))
    r = np.dot(r,rr)
    r = np.dot(r, rot)
    r1[:3,:3] = r
    im = Image.new("RGB", (2048, 2048), "black")
    draw = ImageDraw.Draw(im, 'RGBA')
    #translate = np.array([0, 0, 1.5])
    render_scene_4d_axis(draw, r1, 4, scale, shift)
    for z in np.arange(0.001, 3.5, 0.02):
        if z<=1:
            prcnt1=0.0; point1 = np.array([np.sqrt(z),0,z])
            prcnt2=1.0; point2 = np.array([-np.sqrt(z),0,z])
        else:
            angle=2*np.arccos(1/np.sqrt(z))
            prcnt1=-angle/2/np.pi; point1 = np.array([1,np.sqrt(z-1),z])
            prcnt2=-1+prcnt1; point2 = np.array([-np.sqrt(z-1),1,z])
        generalized_arc(draw, r, center=np.array([0,0,z]), vec=np.array([0,0,1]), 
                        point=point1, 
                        radius=np.sqrt(z), prcnt=prcnt1, rgba=(255,20,147,50))
        generalized_arc(draw, r, np.array([0,0,z]), np.array([0,0,1]), point2, 
                        np.sqrt(z), prcnt2, (255,20,147,10))
    ## Highlight axes
    xax1=np.array([-100.0,0,0.0]);xax1=np.dot(r,xax1)*scale+shift
    xax2=np.array([100.0,0,0.0]);xax2=np.dot(r,xax2)*scale+shift
    draw.line((xax1[0], xax1[1], xax2[0], xax2[1]), fill=(235,255,0), width=4)
    xax1=np.array([0.0,-100,0.0]);xax1=np.dot(r,xax1)*scale+shift
    xax2=np.array([0.0,100,0.0]);xax2=np.dot(r,xax2)*scale+shift
    draw.line((xax1[0], xax1[1], xax2[0], xax2[1]), fill=(235,255,0), width=4)
    xzgradients(draw, r, 1.0) # draws the arrows correponding to gradients.
    ## Draw the plane.
    pt1 = np.array([1.0,-1.2,0]); pt2 = np.array([1.0,1.2,0])
    z = 1.2**2+1
    pt3 = np.array([1.0,-1.2,z]); pt4 = np.array([1.0,1.2,z])
    pt1 = np.dot(r,pt1)*scale+shift; pt2 = np.dot(r,pt2)*scale+shift
    pt3 = np.dot(r,pt3)*scale+shift; pt4 = np.dot(r,pt4)*scale+shift
    draw.polygon([(pt1[0], pt1[1]), (pt2[0], pt2[1]), (pt4[0], pt4[1]), (pt3[0], pt3[1])],\
                    (0,102,255,150))
    pt = np.array([1.0,0,1.0]);pt=np.dot(r,pt)*scale+shift
    pt_z = np.array([0.0,0,1.0]); pt_z=np.dot(r,pt_z)*scale+shift
    draw.line((pt[0], pt[1], pt_z[0], pt_z[1]), fill=(255,0,120), width=4)
    pt_y = np.array([1.0,0,0.0]); pt_y=np.dot(r,pt_y)*scale+shift
    #draw.line((pt[0], pt[1], pt_y[0], pt_y[1]), fill=(255,0,120), width=4)
    draw.ellipse((pt[0]-10, pt[1]-10, pt[0]+10, pt[1]+10), fill = (0,255,0))
    pt = shift
    draw.ellipse((pt[0]-10, pt[1]-10, pt[0]+10, pt[1]+10), fill = (255,255,0))
    im.save(basepath + 'im' + str(im_ind) + '.png')


def xzgradients(draw, r, y):
    for x in [-1.2,-0.7,-0.4,0.0,0.4,0.7,1.2]:
        z = x*x + y*y
        #draw_points(draw, r, y, x)
        #arrowV1(draw,r,np.array([y,x,z]), np.array([2.5*y,2.5*x,z]), (204,102,255))
        arrowV1(draw,r,np.array([y,x,z]), np.array([2.5*y,2.5*x,z]), (255,20,147))
        #arrowV1(draw,r,np.array([y,x,z]), np.array([y+1.0,x,z]), (0,102,255))
        arrowV1(draw,r,np.array([y,x,z]), np.array([y-1.0,x,z]), (0,102,255))


def paraboloidTangent(draw, r, x1, y1, d = 1.0, rgba = (120,80,200,150), scale = 200, 
                      shift = np.array([1000,1000,0])):
    '''
    Draws a tangent plane to a paraboloid: x^2+y^2 = z at point given by coordinates (x1, y1)
    '''
    x2 = x1-d
    y2 = y1+d
    pt1 = np.dot(r, np.array([x2, y2, z_plane(x2, y2, x1, y1)])) * scale + shift[:3]
    x2 = x1+d
    y2 = y1+d
    pt2 = np.dot(r, np.array([x2, y2, z_plane(x2, y2, x1, y1)])) * scale + shift[:3]
    x2 = x1+d
    y2 = y1-d
    pt3 = np.dot(r, np.array([x2, y2, z_plane(x2, y2, x1, y1)])) * scale + shift[:3]
    x2 = x1-d
    y2 = y1-d
    pt4 = np.dot(r, np.array([x2, y2, z_plane(x2, y2, x1, y1)])) * scale + shift[:3]
    draw.polygon([(pt1[0], pt1[1]), (pt2[0], pt2[1]), (pt3[0], pt3[1]), (pt4[0], pt4[1])], rgba)


def paraboloid(x, y, coeff=0.1, intercept=0.1):
    '''
    '''
    return coeff*(x**2 + y**2) - intercept


def paraboloid_intersection(draw, r, x1, y1, coeff, intercept, 
    shift=np.array([1000.0, 1000.0, 0.0]), scale=200.0,
    rgba=(250,250,20), start_line=-12, extend=1.7, width=10):
    '''
    Draws the intersection arc of two paraboloids.
    args:
        extend: The amount by which the arc is to extend from its starting point. This parameter was tuned by hit and trial.
    '''
    def parametrized_pt(t, x1, y1, coeff, intercept):
        '''
        See 180225
        '''
        x = t
        y = (x1**2 + y1**2 - 2*t*x1)/(2*y1)
        z = coeff*(x**2+y**2) - intercept
        return np.array([x, y, z])
    t = start_line
    pt1 = np.dot(r, parametrized_pt(t, x1, y1, coeff, intercept)) * scale + shift[:3]
    #for i in range(1, int_line):
    while t <= abs(start_line)*extend:
        t += 1/10.0
        pt2 = np.dot(r, parametrized_pt(t, x1, y1, coeff, intercept)) * scale + shift[:3]
        draw.line((pt1[0], pt1[1], pt2[0], pt2[1]), fill=rgba, width=width)
        pt1 = pt2


def draw_paraboloids(scale=12.5, basedir=".\\"):
    '''
    Draws a pair of flapping paraboloids.
    args:
        scale: How big should the paraboloids be relative to the image.
        basedir:The directory where the images are to be saved.
            In the main pyray repo, basedir is ..\\images\\RotatingCube\\
    '''
    sep = 8
    base_coeff = 0.01
    start_line = -12
    r1 = np.eye(4)
    for j in range(21,22):
        r = rotation(3, np.pi/30*j)
        r1[:3,:3] = r
        for i1 in range(20):
            i = 2.5*np.sin(i1*np.pi/10.0)
            im = Image.new("RGB", (2048, 2048), (1, 1, 1))
            draw = ImageDraw.Draw(im, 'RGBA')
            render_scene_4d_axis(draw, r1, 4)
            fn = lambda x, y : paraboloid(x, y, coeff=i*base_coeff, intercept=i)
            cfn = lambda x, y : 0.0
            #drawFunctionalXYGrid(draw, r, scale=50, fn=cfn, extent=15)
            drawXYGrid(draw, r, meshLen=1.0)
            drawFunctionalXYGrid(draw, r, scale=scale, fn=fn, extent=20, rgba2=(0,255,0,75),
                saperatingPlane=np.array([-1,-1,sep]))
            shift1 = np.dot(r, np.array([sep,sep,0]))*scale + np.array([1000.0, 1000.0, 0])
            drawFunctionalXYGrid(draw, r, scale=scale, fn=fn, shift=shift1, rgba=(202,200,20,150), extent=20,
                rgba2=(202,200,20,75), saperatingPlane=np.array([1,1,sep]))
            draw_circle_x_y(draw, r, center=np.array([0,0]), radius=np.sqrt(1/base_coeff), scale=scale)
            draw_circle_x_y(draw, r, center=np.array([0,0]), radius=np.sqrt(1/base_coeff),
                scale=scale, shift=shift1)
            paraboloid_intersection(draw, r, sep, sep, i*base_coeff, i, scale=scale, start_line=start_line)
            im.save(basedir + "im" + str(i1) + ".png")


def draw_paraboloidsV2(scale=20.0, ind=0):
    sep = 8
    base_coeff = 0.02
    start_line = -12.0
    r1 = np.eye(4)
    j = 21
    r = rotation(3, np.pi/30*j)
    r1[:3,:3] = r
    shift = np.array([1000.0, 1000.0, 0.0])
    for i1 in range(2,3):
        pt_orig = -9.0*np.array([np.cos(np.pi*6.0/15.0), np.sin(np.pi*6.0/15.0), 0])
        for ind in range(15):
            #i = 2.5*np.sin(i1*np.pi/10.0)
            i = 2.0
            c = i*base_coeff
            im = Image.new("RGB", (2048, 2048), (1, 1, 1))
            draw = ImageDraw.Draw(im, 'RGBA')
            fn = lambda x, y : paraboloid(x, y, coeff=i*base_coeff, intercept=i)
            cfn = lambda x, y : 0.0

            drawFunctionalXYGrid(draw, r, scale=scale, fn=fn, extent=30, rgba2=(0,255,0,40),
                saperatingPlane=np.array([-1,-1,sep]))

            shift1 = np.dot(r, np.array([sep,sep,0.0]))*scale + np.array([1000.0, 1000.0, 0.0])

            drawFunctionalXYGrid(draw, r, scale=scale, fn=fn, shift=shift1, rgba=(202,200,20,150),
                extent=30, rgba2=(202,200,20,40), saperatingPlane=np.array([1,1,sep]))

            draw_circle_x_y(draw, r, center=np.array([0,0]), radius=np.sqrt(1/base_coeff),
                scale=scale)

            draw_circle_x_y(draw, r, center=np.array([0,0]), radius=np.sqrt(1/base_coeff),
                scale=scale, shift=shift1)

            paraboloid_intersection(draw, r, sep, sep, i*base_coeff, i, scale=scale,
                start_line=start_line)

            render_scene_4d_axis(draw, r1, 4)

            #pt_orig = 10.0*np.array([np.cos(np.pi*ind/15.0), np.sin(np.pi*ind/15.0), 0])
            pt = pt_orig
            z1 = i*base_coeff*(pt[0]**2 + pt[1]**2) - i
            z2 = i*base_coeff*((pt[0] - sep)**2 + (pt[1] - sep)**2) - i
            pt1 = np.array([pt[0],pt[1],z1])
            pt1 = np.dot(r, pt1)*scale+shift
            pt2 = np.array([pt[0],pt[1],z2])
            pt2 = np.dot(r, pt2)*scale+shift
            pt = np.dot(r, pt)*scale+shift
            draw.ellipse((pt[0]-5, pt[1]-5, pt[0]+5, pt[1]+5), fill = (255,0,120))
            draw.ellipse((pt1[0]-5, pt1[1]-5, pt1[0]+5, pt1[1]+5), fill = (0,255,0))
            draw.ellipse((pt2[0]-5, pt2[1]-5, pt2[0]+5, pt2[1]+5), fill = (202,200,20))
            draw.line((pt[0], pt[1], pt2[0], pt2[1]), fill="white", width=3)

            [x0, y0] = [0, 0]
            [x1, y1] = pt_orig[:2]
            [a1, b1, d1] = [2*c*(x1-x0), 2*c*(y1-y0), c*(x1-x0)**2 + c*(y1-y0)**2 - i -2*c*(x1-x0)*x1 - 2*c*(y1-y0)*y1]

            [x0_1, y0_1] = [sep, sep]
            [a2, b2, d2] = [2*c*(x1-x0_1), 2*c*(y1-y0_1), c*(x1-x0_1)**2 + c*(y1-y0_1)**2 \
                - i -2*c*(x1-x0_1)*x1 - 2*c*(y1-y0_1)*y1]
            [line_pt1, line_pt2] = plane_intersection(draw, r, plane1=[a1, b1, d1], plane2=[a2, b2, d2],
                x_start=pt_orig[0]-7, x_end=pt_orig[0]+7, scale=scale, shift=shift)
            generalizedParaboloidTangent(draw, r, pt_orig[0], pt_orig[1], d=10.0, x0=0, y0=0,
             c=c, i=i , scale=scale, shift=shift, line_pt1=line_pt1, line_pt2=line_pt2, rgba=(153,255,102,150))
            generalizedParaboloidTangent(draw, r, pt_orig[0], pt_orig[1], d=10.0, x0=sep, y0=sep,
             c=c, i=i , scale=scale, shift=shift, line_pt1=line_pt1, line_pt2=line_pt2, rgba=(255,204,102,150))
            mat = np.array([[a1, b1],[a2, b2]])
            rhs = np.array([-d1, -d2])
            pt_orig = np.linalg.solve(mat, rhs)
            pt_orig = np.append(pt_orig, 0)
            pt = np.dot(r, pt_orig)*scale+shift
            draw.line((pt[0], pt[1], line_pt1[0], line_pt1[1]))
            draw.line((pt[0], pt[1], line_pt2[0], line_pt2[1]))
            drawXYGrid(draw, r, meshLen=1.0)
            im.save("Images\\RotatingCube\\im" + str(ind) + ".png")



def three_d_parabola(draw, r, r2, scale = 200, shift = np.array([1000,1000,0])):
    '''
    Draws a curve described by the intersection of a plane with the paraboloid x^2+y^2 = z
    params:
        r: The rotation matrix the whole scene is rotated by
        r2: The rotation matrix that the inetersecting plane is to be rotated by
    '''
    # Assume you start with the x-z plane
    orthogonal_vec = np.array([0,1,0])
    orthogonal_vec = np.dot(r2, orthogonal_vec)
    b = 1.5
    [thetax, thetay, thetaz] = orthogonal_vec
    c1 = -thetax/thetaz/2
    c2 = -thetay/thetaz/2
    c3 = np.sqrt(b + c1**2 + c2**2)
    x_min = max((c1 - abs(c3)),-np.sqrt(3.5))
    x_max = min((c1 + abs(c3)),np.sqrt(3.5))
    y = c2 + np.sqrt(c3*c3 - (x_min-c1)*(x_min-c1))
    pt1 = np.dot(r, [x_min, y, (x_min**2+y**2)]) * scale + shift[:3]
    for x in np.arange(x_min, x_max, 0.01):
        y = c2 + np.sqrt(c3*c3 - (x-c1)*(x-c1))
        pt2 = np.dot(r, [x, y, (x**2 + y**2)]) * scale + shift[:3]
        if x**2 + y**2 < 3.5:
            draw.line((pt1[0], pt1[1], pt2[0], pt2[1]), fill = (204,102,255), width=5)
        pt1 = pt2
    y = c2 + np.sqrt(c3*c3 - (x_min-c1)*(x_min-c1))
    pt1 = np.dot(r, [x_min, y, (x_min**2+y**2)]) * scale + shift[:3]
    for x in np.arange(x_min, x_max, 0.01):
        y = c2 - np.sqrt(c3*c3 - (x-c1)*(x-c1))
        pt2 = np.dot(r, [x, y, (x**2 + y**2)]) * scale + shift[:3]
        if x**2 + y**2 < 3.5:
            draw.line((pt1[0], pt1[1], pt2[0], pt2[1]), fill = (204,102,255), width=5)
        pt1 = pt2


def plane_intersection(draw, r, plane1=[0,0,0], plane2=[0,0,0], x_start=0, x_end=0, scale=200,
    shift=np.array([1000,1000,0])):
    [a1,b1,d1] = plane1
    [a2,b2,d2] = plane2
    x = x_start
    y = ((d2-d1) + (a2-a1)*x)/(b1-b2)
    z = a1*x+b1*y+d1
    pt1 = np.dot(r, np.array([x, y, z])) * scale + shift[:3]
    init_pt = pt1
    while x <= x_end:
        x += 1/10.0
        y = ((d2-d1) + (a2-a1)*x)/(b1-b2)
        z = a1*x+b1*y+d1
        pt2 = np.dot(r, np.array([x, y, z])) * scale + shift[:3]
        #draw.line((pt1[0], pt1[1], pt2[0], pt2[1]), fill = "white", width=3)
        pt1 = pt2
    fin_pt = pt1
    return [init_pt, fin_pt]


def paraboloidTangentV2(draw, r, x1, y1, c=1.0, d = 1.0, rgba = (120,80,200,150), scale = 200,
    shift = np.array([1000,1000,0]), line_pt1=None, line_pt2=None):
    '''
    Draws a tangent plane to a paraboloid: x^2+y^2 = z at point given by coordinates (x1, y1)
    '''
    x2 = x1-d
    y2 = y1+d
    pt1 = np.dot(r, np.array([x2, y2, c*z_plane(x2, y2, x1, y1)])) * scale + shift[:3]
    x2 = x1+d
    y2 = y1+d
    pt2 = np.dot(r, np.array([x2, y2, c*z_plane(x2, y2, x1, y1)])) * scale + shift[:3]
    x2 = x1+d
    y2 = y1-d
    pt3 = np.dot(r, np.array([x2, y2, c*z_plane(x2, y2, x1, y1)])) * scale + shift[:3]
    x2 = x1-d
    y2 = y1-d
    pt4 = np.dot(r, np.array([x2, y2, c*z_plane(x2, y2, x1, y1)])) * scale + shift[:3]
    #draw.polygon([(pt1[0], pt1[1]), (pt2[0], pt2[1]), (pt3[0], pt3[1]), (pt4[0], pt4[1])], rgba)
    sqr1 = [[pt1[0], pt1[1]], [pt2[0], pt2[1]], [pt3[0],pt3[1]], [pt4[0], pt4[1]]]
    if line_pt1 is not None:
        sqr1.append([line_pt1[0], line_pt1[1]])
    if line_pt2 is not None:
        sqr1.append([line_pt2[0], line_pt2[1]])
    hull = ConvexHull([i[:2] for i in sqr1]).vertices
    poly = [(sqr1[i][0], sqr1[i][1]) for i in hull]
    draw.polygon(poly, rgba)


def z_plane(x, y, x1, y1):
    '''
    Returns the z-coordinate of a point on a plane that is tangent to the paraboloid z = x^2 + y^2
    '''
    return 2*x1*x + 2*y1*y - (x1**2 + y1**2)


def generalizedParaboloidTangent(draw, r, x1, y1, d=1.0, x0=0.0, y0=0.0, rgba=(120,80,200,150),
    c=1.0, i=0.0,
    scale=200, shift=np.array([1000,1000,0]),
    line_pt1=None, line_pt2=None, p=1.0):
    '''
    Draws a tangent plane to a paraboloid: x^2+y^2 = z at point given by coordinates (x1, y1)
    '''
    x2 = x1-d
    y2 = y1+d
    pt1 = np.dot(r, np.array([x2, y2, z_plane_generalized(x2, y2, x1, y1, x0, y0, c, i)]))*scale + shift[:3]
    x2 = x1+d
    y2 = y1+d
    pt2 = np.dot(r, np.array([x2, y2, z_plane_generalized(x2, y2, x1, y1, x0, y0, c, i)]))*scale + shift[:3]
    x2 = x1+d
    y2 = y1-d
    pt3 = np.dot(r, np.array([x2, y2, z_plane_generalized(x2, y2, x1, y1, x0, y0, c, i)]))*scale + shift[:3]
    x2 = x1-d
    y2 = y1-d
    pt4 = np.dot(r, np.array([x2, y2, z_plane_generalized(x2, y2, x1, y1, x0, y0, c, i)]))*scale + shift[:3]
    #draw.polygon([(pt1[0], pt1[1]), (pt2[0], pt2[1]), (pt3[0], pt3[1]), (pt4[0], pt4[1])], rgba)
    sqr1 = [[pt1[0], pt1[1]], [pt2[0], pt2[1]], [pt3[0],pt3[1]], [pt4[0], pt4[1]]]
    if line_pt1 is not None:
        sqr1.append([line_pt1[0], line_pt1[1]])
    if line_pt2 is not None:
        sqr1.append([line_pt2[0], line_pt2[1]])
    try:
        hull = ConvexHull([i[:2] for i in sqr1]).vertices
    except:
        hull = range(4)
    orig_pt = np.dot(r, np.array([x1,y1,z_plane_generalized(x1, y1, x1, y1, x0, y0, c, i)]))*scale+shift[:3]
    poly = [(sqr1[i][0]*p+orig_pt[0]*(1-p), sqr1[i][1]*p+orig_pt[1]*(1-p)) for i in hull]
    draw.polygon(poly, rgba)


def z_plane_generalized(x, y, x1, y1, x0, y0, c=1.0, i=0.0):
    d = c*(x1-x0)**2 + c*(y1-y0)**2 - i -2*c*(x1-x0)*x1 - 2*c*(y1-y0)*y1
    return 2*c*(x1-x0)*x + 2*c*(y1-y0)*y + d



