import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageMath
from pyray.shapes.solid.polyhedron import *
from pyray.axes import *
from pyray.rotation import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


#############################################################################
## Scene 1 - Platonic solids popping up.
basedir = '..\\images\\RotatingCube\\'
txt = "This is a Tetrahedron"
tt = Tetartoid(0.33,0)

for i in range(0, 31):
    r = general_rotation(np.array([0.5,0.5,0.5]),2*np.pi*i/30)
    #r = rotation(3,np.pi/15*i)
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    tt.render_solid_planes(draw, r, shift=np.array([1000, 1000, 0]), scale=150*i/10.0)
    writeStaggeredText(txt, draw, i, speed=2)
    im.save(basedir + "im" + str(i) + ".png")



#############################################################################
## Scene 2 - It has 12 symmetries.
basedir = '..\\images\\RotatingCube\\'
txt = "It can be slowly converted to this solid"

for i in range(0, 31):
    tt = Tetartoid(0.4,0.1*i/30)
    r = general_rotation(np.array([0.5,0.5,0.5]),2*np.pi*i/30)
    #r = rotation(3,np.pi/15*i)
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    tt.render_solid_planes(draw, r, shift=np.array([1000, 1000, 0]), scale=450*(1+i/60))
    writeStaggeredText(txt, draw, i, speed=2)
    im.save(basedir + "im" + str(i) + ".png")


#############################################################################
## Scene a - Step by step tetartoid face
## Confirms that the tetartoid face given by wikipedia traces out a pentagon.
basedir = '..\\images\\RotatingCube\\'
pts = tetartoid_face(1,2,3)
w=10
im = Image.new("RGB", (2048, 2048), (1,1,1))
draw = ImageDraw.Draw(im,'RGBA')

for i in range(5):
    j1 = pts[i]
    j = j1*30+1000
    draw.ellipse((j[0]-w,j[1]-w,j[0]+w,j[1]+w),fill=(255,255,255))
    render_solid_planes(faces,draw,r,scale=150)
    im.save(basedir + "im" + str(i) + ".png")


#############################################################################
## Scene b - Draws out tetartoid faces via tetrahedral rotations.
## Confirms that once we draw a face, we can rotate it by the tetrahedral 
## rotation group to form a tetartoid.
basedir = '..\\images\\RotatingCube\\'
pts = tetartoid_face(1,2,3)
rots = tetrahedral_rotations()
r = general_rotation(np.array([0.5,0.5,0.5]),2*np.pi*10/30)
w=10

faces = []
faces.append(pts)

for i in range(len(rots)):
    faces.append(np.dot(pts,rots[i]))
    #render_solid_planes(faces,draw,r,scale=150)
    #im.save(basedir + "im" + str(i) + ".png")

for i in range(31):
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    r = general_rotation(np.array([0.5,0.5,0.5]),2*np.pi*i/30)
    render_solid_planes(faces,draw,r,scale=150)
    im.save(basedir + "im" + str(i) + ".png")


#############################################################################
## Scene c - teserract that is shaded.
basedir = '..\\images\\RotatingCube\\'
cu = Cube(4)

for i in range(0,31):
    r = rotation(4, 2*np.pi*i/30)
    faces = [orient_face(np.dot(j.face_matrix-np.array([.5,.5,.5,.5]),r)[[0,1,3,2]][:,:-1]) for j in cu.faces]
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    render_solid_planes(faces,draw,np.eye(3),scale=350)
    im.save(basedir + "im" + str(i) + ".png")


#############################################################################
## Scene d - Quadrilateral flap rotating about hinge.
basedir = '..\\images\\RotatingCube\\'
a = np.random.uniform(size=2)
b = np.random.uniform(size=2)
midd = (a+b)/2

perpend = (a-b)*np.array([-1,1])
p = 0.8
c = midd + p*perpend

p0 = 0.45
pt1 = p0*a+(1-p0)*b
p1=1.3
pt1 = pt1 - perpend*p1

plane = np.array([a,c,b,pt1])
plane = np.append(plane,np.zeros(4)[...,None],1)
plane = np.append(plane,np.ones(4)[...,None],1)

for i in range(0,10):
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    r = axis_rotation(plane[1],plane[0],2*np.pi*i/30)
    plane1 = np.dot(r,plane.T).T
    plane1 = plane1[:,np.array([0,1,2])]
    render_solid_planes([plane1],draw,np.eye(3),cut_back_face=False)
    im.save(basedir + "im" + str(i) + ".png")


#############################################################################
## Scene e - Forming half mesh for trigonal trapezohedron.
basedir = '..\\images\\RotatingCube\\'
a = np.array([1,0])
b = np.array([-1,0])
midd = (a+b)/2

perpend = np.dot(planar_rotation(np.pi/2),(a-b))
p = 0.8
c = midd + p*perpend

perpendicular = np.sqrt(sum((c-midd)**2))
base = np.sqrt(sum((a-midd)**2))

## The two equal angles of the isocoloes triangle used to form the quadrilateral.
theta = np.arctan(perpendicular/base)

## The angle between the two equal sides of the quadrilateral.
theta1 = 2*(np.pi/2-theta)
vec1 = plane[3]-plane[0]
vec1 = vec1/np.sqrt(sum(vec1*vec1))
vec2 = plane[3]-plane[2]
vec2 = vec2/np.sqrt(sum(vec2*vec2))
theta2 = np.arccos(np.dot(vec1,vec2))

## The rotation needed to convert mesh plot to solid.
phi = np.arccos((np.cos(theta1)**2-np.cos(theta1))/np.sin(theta1)**2)
phi2 = -np.arccos((np.cos(theta2)**2-np.cos(theta2))/np.sin(theta2)**2)

p0 = 0.3
pt1 = p0*a+(1-p0)*b
p1=0.75
pt1 = pt1 - perpend*p1

plane = np.array([a,c,b,pt1])
r = rotation(3,np.pi/5*0)
plane = np.append(plane,np.zeros(4)[...,None],1)
plane = np.dot(plane, r)
plane_per = np.cross(plane[0]-plane[1], plane[1]-plane[2])

plane = np.append(plane,np.ones(4)[...,None],1)
plane_per = -1*np.concatenate((plane_per,[0]),axis=0) ## The sign here seems to matter. Need to understand how.
#plane_per = np.array([0,0,3.2,0])

for i in range(0,31):
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    r = axis_rotation(plane[1], plane[1]+plane_per, theta1*i/30)
    r1 = axis_rotation(plane[1], plane[1]+plane_per, -theta1*i/30)
    side_mid = (plane[0]+plane[3])/2
    r2 = axis_rotation(side_mid, side_mid+plane_per, -np.pi*i/30)
    plane2 = np.dot(r,plane.T).T
    plane2 = plane2[:,np.array([0,1,2])]
    plane3 = np.dot(r1,plane.T).T
    plane3 = plane3[:,np.array([0,1,2])]
    plane4 = np.dot(r2,plane.T).T
    plane4 = plane4[:,np.array([0,1,2])]
    plane1 = plane[:,np.array([0,1,2])]
    render_solid_planes([plane1,plane2,plane3,plane4],draw,np.eye(3),cut_back_face=False, scale=150, make_edges=True)
    im.save(basedir + "im" + str(i) + ".png")
    im.close()

for i in range(0,31):
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    r = axis_rotation(plane[1],plane[1]+plane_per, theta1)
    rr = axis_rotation(plane[1],plane[2], i/30*phi)
    r = np.dot(rr,r)
    r1 = axis_rotation(plane[1],plane[1]+plane_per, -theta1)
    rr1 = axis_rotation(plane[1],plane[0], -i/30*phi) ## Need to understand how sign works here.
    r1 = np.dot(rr1,r1)
    r2 = axis_rotation(side_mid, side_mid+plane_per, -np.pi)
    rr2 = axis_rotation(plane[3], plane[0], i/30*np.pi/3)
    r2 = np.dot(rr2,r2)

    plane2 = np.dot(r,plane.T).T
    plane2 = plane2[:,np.array([0,1,2])]
    plane3 = np.dot(r1,plane.T).T
    plane3 = plane3[:,np.array([0,1,2])]
    plane4 = np.dot(r2,plane.T).T
    plane4 = plane4[:,np.array([0,1,2])]

    plane1 = plane[:,np.array([0,1,2])]
    render_solid_planes([plane1,plane2,plane3,plane4],draw,np.eye(3),cut_back_face=False, scale=150)
    im.save(basedir + "im" + str(31+i) + ".png")
    im.close()


#############################################################################
## Scene e.1 - Forming trigonal trapezohedron with rotations.
m1= np.array([[1,0,0], [0,-1,0], [0,0,-1]])
t=2*np.pi/3
c=np.cos(t)
s=np.sin(t)
m2= np.array([ [c,s,0], [-s,c,0], [0,0,1]])
x0=2
y0=0.5
z0=1
z = z0*(-s*x0+(c-1)*y0)*x0/((c-1)*x0+s*y0)/y0
p = np.zeros((3,8))
p[:,0] = [x0,y0,z0]
p[:,1] = np.dot(m2,p[:,0])
p[:,2] = np.dot(m2,p[:,1])
p[:,3] = np.dot(m1,p[:,0])
p[:,4] = np.dot(m2,p[:,3])
p[:,5] = np.dot(m2,p[:,4])
p[:,6] = [0,0,z]
p[:,7] = [0,0,-z]

#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#ax.scatter(p[0,:], p[1,:], p[2,:], c='r', marker='o')
#plt.show()
colors = ['red','green','blue','yellow','orange','white','grey','purple']
basedir = '..\\images\\RotatingCube\\'

def draw_pts():
    for j in range(30):
        im = Image.new("RGB", (2048, 2048), (1,1,1))
        draw = ImageDraw.Draw(im,'RGBA')
        r = rotation(3,np.pi/30*j)
        p1 = np.dot(r,p)
        p1 = p1*200+1000.0
        for i in range(p1.shape[1]):
            v = p1[:,i]
            draw.ellipse((v[0]-5, v[1]-5, v[0]+5, v[1]+5),fill=colors[i], outline=colors[i])
        im.save(basedir + "im" + str(j) + ".png")

plane1 = np.array([p[:,i] for i in [0,3,1,6]])
plane2 = np.array([p[:,i] for i in [4,7,5,2]])
plane3 = np.array([p[:,i] for i in [0,3,7,5]])
plane4 = np.array([p[:,i] for i in [1,6,2,4]])
plane5 = np.array([p[:,i] for i in [2,5,0,6]])
plane6 = np.array([p[:,i] for i in [1,3,7,4]])
planes = np.array([plane1,plane2,plane3,plane4,plane5,plane6])

def draw_planes():
    for j in range(31):
        im = Image.new("RGB", (2048, 2048), (1,1,1))
        draw = ImageDraw.Draw(im,'RGBA')
        r = rotation(3,np.pi/30*j)
        #r = general_rotation(np.array([0.0,0.0,1.0]),2*np.pi*j/30)
        render_solid_planes(planes,draw,r,cut_back_face=True, scale=200)
        im.save(basedir + "im" + str(j) + ".png")
        im.close()


#############################################################################
## Scene f - Visualize dual planes of tetartoid.
basedir = '..\\images\\RotatingCube\\'
tt = Tetartoid(s=0.45,t=0.14)

dual_faces = []
for j in range(20):
    dual_face = np.array([np.mean(tt.planes[i],axis=0) for i in tt.dual_face_indices[j]])
    dual_face = orient_face(dual_face)
    dual_faces.append(dual_face)

for i in range(0, 31):
    r = general_rotation(np.array([0.5,0.5,0.5]),2*np.pi*i/30)
    #r = rotation(3,np.pi/15*i)
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    tt.render_solid_planes(draw, r, shift=np.array([1000, 1000, 0]), scale=1000, trnsp=120, make_edges=True)
    render_solid_planes(dual_faces,draw,r,scale=1000, trnsp=200)
    im.save(basedir + "im" + str(i) + ".png")


#############################################################################
## Scene x - All platonic solids.
basedir = '..\\images\\RotatingCube\\'
ic = Icosahedron()
dd = Dodecahedron()
tt = Tetrahedron()
oc = Octahedron()
tr = Tetartoid(0.4,0.1)

for i in range(0, 31):
    r = general_rotation(np.array([0.5,0.5,0.5]),2*np.pi*i/30)
    #r = rotation(3,np.pi/15*i)
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    ic.render_solid_planes(draw, r, shift=np.array([500, 500, 0]), scale=150)
    dd.render_solid_planes(draw, r, shift=np.array([1500, 1500, 0]), scale=150)
    tt.render_solid_planes(draw, r, shift=np.array([1500, 500, 0]), scale=150)
    oc.render_solid_planes(draw, r, shift=np.array([500, 1500, 0]), scale=300)
    tr.render_solid_planes(draw, r, shift=np.array([1000, 1000, 0]), scale=450)
    im.save(basedir + "im" + str(i) + ".png")


#############################################################################
## Scene y - Icosahedron morphing.
basedir = '..\\images\\RotatingCube\\'

for i in range(0, 31):
    tr = Tetartoid(s=0.333, t=0.2*i/30)
    r = general_rotation(np.array([0.5,0.5,0.5]),2*np.pi*i/30)
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im,'RGBA')
    tr.render_solid_planes(draw, r, shift=np.array([1000, 1000, 0]), scale=650)
    im.save(basedir + "im" + str(i) + ".png")


def tetartoid(draw, r, s=0.3, t=0.04, scale=500, shift=np.array([1000.0, 1000.0, 0])):
    '''
    Draws a tetartoid. Based on the answer by Arentino here -
    https://math.stackexchange.com/questions/1393370/what-are-the-rules-for-a-tetartoid-pentagon
    args:
        s: 0 <= s <= 0.5.
    '''
    tet_orig = np.array([
            [1,1,1],
            [-1,-1,1],
            [1,-1,-1],
            [-1,1,-1]
        ])
    # Make it a tetrahedron with unit edges.
    tet_orig = tet_orig/2/np.sqrt(2)
    r1 = rotation(3, np.pi/10)
    tet_orig = np.dot(tet_orig, r1)
    v = np.dot(r, np.transpose(tet_orig)) * scale
    v = np.transpose(v) + shift[:3]
    # For each edge V_i V_j, construct two points P_ij and P_ji having a fixed distance s from V_i and V_j.
    p = np.zeros((4,4,3))
    for i in range(4):
        for j in range(i+1, 4):
            p[i, j] = (1-s)*v[i] + s*v[j]
            p[j, i] = s*v[i] + (1-s)*v[j]
    # Join the center C_ijk of every face V_i V_j V_k with P_ij, P_jk and P_ik.
    # First, let's just obtain the centers.
    c = np.zeros((4, 3))
    for i in range(4):
        face = [f for f in range(4) if f != i] #TODO: Is there a better way to exclude indices?
        c[i] = sum(v[face]) / 3
    # Now let o be the tetartoid center.
    o = shift
    # Consider the six planes o v_i v_j passing through the center and each edge.
    # From point p_ij, draw the perpendicular line to o v_i v_j and take on it
    # a point q_ij such that p_ij q_ij = t.
    q = np.zeros((4, 4, 3))
    for i in range(4):
        for j in range(i+1, 4):
            directn = np.cross(v[i]-o, v[j]-o)
            directn = directn / np.sqrt(sum(directn**2))
            q[i, j] = p[i, j] + directn * t * scale
            q[j, i] = p[j, i] - directn * t * scale

    planes = [
        [c[3], q[2,0], q[0,2], v[0], q[0,1]],
        [c[3], q[1,2], q[2,1], v[2], q[2,0]],
        [c[3], q[0,1], q[1,0], v[1], q[1,2]],

        [c[1], q[0,2], q[2,0], v[2], q[2,3]],
        [c[1], q[2,3], q[3,2], v[3], q[3,0]],
        [c[1], q[3,0], q[0,3], v[0], q[0,2]],

        [c[2], q[1,0], q[0,1], v[0], q[0,3]],
        [c[2], q[3,1], q[1,3], v[1], q[1,0]],
        [c[2], q[0,3], q[3,0], v[3], q[3,1]],

        [c[0], q[2,1], q[1,2], v[1], q[1,3]],
        [c[0], q[1,3], q[3,1], v[3], q[3,2]],
        [c[0], q[3,2], q[2,3], v[2], q[2,1]]
    ]
    planes = np.array(planes)
    for plane in planes:
        is_outwards = plane[0][2]>o[2]
        cprime = line_plane_intersection(o, plane[0], plane[1], plane[2], plane[4])
        vprime = line_plane_intersection(o, plane[3], plane[1], plane[2], plane[4])
        plane[0] = cprime
        plane[3] = vprime
        smat = sum(plane - o)
        cross_pdt = np.cross(plane[0]-plane[1], plane[0]-plane[2])
        cross_pdt = cross_pdt/np.sqrt(sum(cross_pdt**2))
        face_angle = np.dot(cross_pdt, np.array([0,0.01,0.99]))    
        if not np.isnan(face_angle) and face_angle>0:
            rgba = colorFromAngle2(face_angle,h=153,s=120,maxx=1.0)
            poly = [(i[0], i[1]) for i in plane]
            draw.polygon(poly, fill=rgba)



def tetrahedron(draw, r, shift=np.array([1000,1000,0]), scale=300):
    tet_orig = np.array([
            [1,1,1],
            [-1,-1,1],
            [1,-1,-1],
            [-1,1,-1]
        ])
    # Make it a tetrahedron with unit edges.
    tet_orig = tet_orig/2/np.sqrt(2)
    planes = np.dot(r, np.transpose(tet_orig)) * scale
    planes = planes.T
    for i in range(len(planes)):
        excl_pt = planes[i]
        plane = planes[[j for j in range(4) if j!=i]]
        smat = sum(plane)
        face_angle = np.dot(smat/np.sqrt(sum(smat**2)), np.array([0,0.01,0.99]))
        if face_angle>0:
            rgba = colorFromAngle2(face_angle,h=153,s=120,maxx=0.60)
            poly = [(i[0]+shift[0], i[1]+shift[1]) for i in plane]
            draw.polygon(poly, fill=rgba)


