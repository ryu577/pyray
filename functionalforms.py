import math
from circle import *
from axes import *


def paraboloid():
    im_ind = 0
    #for i in np.concatenate((np.arange(1.1,20,1),np.arange(-20,-1.1,1)),axis=0):
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
            plane(draw, r, r2, 200, np.array([1000,1000,0]), translate)
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
                        draw.line((pt1[0]*scale + shift[0], pt1[1]*scale+shift[1], pt2[0]*scale+shift[0], pt2[1]*scale+shift[1]), fill=(255,20,147,30), width=5)
                    else:
                        draw.line((pt1[0]*scale + shift[0], pt1[1]*scale+shift[1], pt2[0]*scale+shift[0], pt2[1]*scale+shift[1]), fill=(255,20,147,10), width=5)
                    pt1 = pt2
            #parabola(draw, r)
            curve(draw, r, r2)
            im.save('Images\\RotatingCube\\im' + str(im_ind) + '.png')
            im_ind = im_ind + 1


def drawFunctionalXYGrid(draw, r, shift=np.array([1000.0, 1000.0, 0.0]), 
        scale=200.0, rgba=(0,255,0,120), fn=None, extent=10,
        saperatingPlane=np.array([-1,-1,4]), rgba2=None):
    '''
    args:
        saperatingPlane: Take the dot product of this plane with [x,y,1]. If <0, draw lighter planes.
        rgba2: The color of the lighter portion of the plane.
    '''
    for i in range(-extent, extent, 1):
        for j in range(-extent, extent, 1):
            poly = gridSquarePolygon(i, j, r, shift, scale, fn)
            if np.dot(np.array([i, j, 1]), saperatingPlane) > 0 or rgba2 is None:
                draw.polygon(poly, rgba)
            else:
                draw.polygon(poly, rgba2)


def gridSquarePolygon(i, j, r, shift=np.array([1000.0, 1000.0, 0.0]), scale=200.0, fn=None):
    '''
    '''
    poly = []
    k = fn(i, j)
    pt = np.array([i, j, k])
    poly.append(np.dot(r, pt) * scale + shift[:3])
    k = fn(i+1, j)
    pt = np.array([i+1, j, k])
    poly.append(np.dot(r, pt) * scale + shift[:3])
    k = fn(i+1, j-1)
    pt = np.array([i+1, j-1, k])
    poly.append(np.dot(r, pt) * scale + shift[:3])
    k = fn(i, j-1)
    pt = np.array([i, j-1, k])
    poly.append(np.dot(r, pt) * scale + shift[:3])
    return [(i[0], i[1]) for i in poly]


def paraboloid(x, y, coeff=0.1, intercept=0.1):
    '''
    '''
    return coeff*(x**2 + y**2) - intercept


def paraboloid_intersection(draw, r, x1, y1, coeff, intercept, shift=np.array([1000.0, 1000.0, 0.0]), scale=200.0, 
    rgba=(250,250,20), start_line=-12, extend=1.7):
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
        draw.line((pt1[0], pt1[1], pt2[0], pt2[1]), fill=rgba, width=10)
        pt1 = pt2


def draw_paraboloids(scale=12.5, ind=0):
    sep = 8
    base_coeff = 0.01
    start_line = -12
    r1 = np.eye(4)
    for j in range(21,22):
        r = rot.rotation(3, np.pi/30*j)
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
            drawFunctionalXYGrid(draw, r, scale=scale, fn=fn, extent=20, rgba2=(0,255,0,75), saperatingPlane=np.array([-1,-1,sep]))
            shift1 = np.dot(r, np.array([sep,sep,0]))*scale + np.array([1000.0, 1000.0, 0])
            drawFunctionalXYGrid(draw, r, scale=scale, fn=fn, shift=shift1, rgba=(202,200,20,150), extent=20, 
                rgba2=(202,200,20,75), saperatingPlane=np.array([1,1,sep]))
            draw_circle_x_y(draw, r, center=np.array([0,0]), radius=np.sqrt(1/base_coeff), scale=scale)
            draw_circle_x_y(draw, r, center=np.array([0,0]), radius=np.sqrt(1/base_coeff), scale=scale, shift=shift1)
            paraboloid_intersection(draw, r, sep, sep, i*base_coeff, i, scale=scale, start_line=start_line)
            im.save("Images\\RotatingCube\\im" + str(i1) + ".png")


def draw_paraboloidsV2(scale=12.5, ind=0):
    sep = 8
    base_coeff = 0.02
    start_line = -12.0
    r1 = np.eye(4)
    j = 21
    r = rot.rotation(3, np.pi/30*j)
    r1[:3,:3] = r
    shift = np.array([1000.0, 1000.0, 0.0])
    for i1 in range(2,3):
        i = 2.5*np.sin(i1*np.pi/10.0)
        im = Image.new("RGB", (2048, 2048), (1, 1, 1))
        draw = ImageDraw.Draw(im, 'RGBA')
        render_scene_4d_axis(draw, r1, 4)
        fn = lambda x, y : paraboloid(x, y, coeff=i*base_coeff, intercept=i)
        cfn = lambda x, y : 0.0
        drawXYGrid(draw, r, meshLen=1.0)
        
        drawFunctionalXYGrid(draw, r, scale=scale, fn=fn, extent=20, rgba2=(0,255,0,40),
            saperatingPlane=np.array([-1,-1,sep]))
        
        shift1 = np.dot(r, np.array([sep,sep,0.0]))*scale + np.array([1000.0, 1000.0, 0.0])

        drawFunctionalXYGrid(draw, r, scale=scale, fn=fn, shift=shift1, rgba=(202,200,20,150),
            extent=20, rgba2=(202,200,20,40), saperatingPlane=np.array([1,1,sep]))
        
        draw_circle_x_y(draw, r, center=np.array([0,0]), radius=np.sqrt(1/base_coeff),
            scale=scale)
        
        draw_circle_x_y(draw, r, center=np.array([0,0]), radius=np.sqrt(1/base_coeff),
            scale=scale, shift=shift1)
        
        paraboloid_intersection(draw, r, sep, sep, i*base_coeff, i, scale=scale,
            start_line=start_line)

        pt = np.array([1,1,0])
        pt = np.dot(r, pt)*scale+shift

        draw.ellipse((pt[0]-5, pt[1]-5, pt[0]+5, pt[1]+5), fill = (255,0,120))
        im.save("Images\\RotatingCube\\im" + str(ind) + ".png")


