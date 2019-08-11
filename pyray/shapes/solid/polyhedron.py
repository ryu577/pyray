'''
All kinds of polyhedra. Like Platonic solids, Archimedean solids, Tetartoids, etc.
'''
import numpy as np
from scipy.spatial import ConvexHull
from pyray.misc import *
from pyray.rotation import *
from pyray.color import *
from pyray.shapes.solid.cube import *
import abc


def render_solid_planes(planes, draw, r, scale=300, shift=np.array([1000,1000,0]),
                        debug=False, trnsp=255, make_edges=False, cut_back_face=True,
                        h=153, s=120, rgb=None):
    """
    Given the plnes that make up the faces of a polyhedron,
    draw all of them with colors representing light
    shading.
    args:
        planes: An array of the collections of points constituting the planes.
        draw: The draw object of Image class.
        r: The rotation matrix.
        scale: How much to scale the figure.
        shift: The center of the figure.
        debug: If true, draws the text of the coordinates at the points.
        trnsp: The transparency of the faces.
        make_edges: Weather or not to draw the edges with the faces.
        cut_back_face: Only show the faces facing the camera. Want
            to set this to true in most cases.
    """
    face_num = -1
    for plane in planes:
        plane1 = np.array(plane)
        plane1 = np.dot(plane1,r)
        plane1 = orient_face(plane1)
        plane_center = sum(plane1)/len(plane1)
        cross_pdt = np.cross(plane1[0]-plane1[1], plane1[0]-plane1[2])
        cross_pdt = cross_pdt/np.sqrt(sum(cross_pdt**2))
        face_angle = abs(np.dot(cross_pdt, np.array([0,0,1.0])))
        plane1 = plane1*scale+shift[:3]
        #if not np.isnan(face_angle) and face_angle>0:
        # The z-coordinate of the face center is positive means the plane
        # is facing towards us.
        face_num+=1
        if rgb is None:
            rgba = colorFromAngle2(face_angle,h=h,s=s,maxx=1.0)
        else:
            rgba = rgb
        rgba1 = rgba+(trnsp,)
        if not cut_back_face or cross_pdt[2]>0:            
            poly = [(i[0], i[1]) for i in plane1]
            draw.polygon(poly, fill=rgba1)
            if debug:
                plane_center = sum(plane1)/len(plane1)
                pos = (plane_center[0], plane_center[1])
                font = ImageFont.truetype("arial.ttf", 78)
                draw.text(pos, str(face_num), (255,255,255), font=font)
        if make_edges:
            for idx in range(len(plane1)):
                draw.line((plane1[idx][0],plane1[idx][1],
                    plane1[(idx+1)%len(plane1)][0],plane1[(idx+1)%len(plane1)][1]), 
                    fill = rgba, width = 5)


def render_solid_planes_back_first(planes, draw, r, scale=300, shift=np.array([1000,1000,0]),
                        debug=False, trnsp=255, make_edges=False, cut_back_face=True,
                        h=153, s=120):
    face_angles = []
    for plane in planes:
        plane1 = np.array(plane)
        plane1 = np.dot(plane1,r)
        plane1 = orient_face(plane1)
        cross_pdt = np.cross(plane1[0]-plane1[1], plane1[0]-plane1[2])
        cross_pdt = cross_pdt/np.sqrt(sum(cross_pdt**2))
        face_angles.append(cross_pdt[2])
    face_angles = np.array(face_angles)
    if sum(face_angles<0) > 0:
        render_solid_planes(planes[face_angles<0], draw, r, scale, shift,
                        debug, trnsp, make_edges, cut_back_face, h, s)
    if sum(face_angles>0) > 0:
        render_solid_planes(planes[face_angles>0], draw, r, scale, shift,
                        debug, trnsp, make_edges, cut_back_face, h, s)


def plane_face_intersection(a,b,c,d,face):
    """
    Finds the intersection line of a plane with 
    the face of a solid. Returns the two points 
    that make up the line of intersection. a,b,c,d are 
    the coefficients of the plane ax+by+cz=d while face
    is a sequence of points which form the plane.
    args:
        a: The coefficient of x in eqn of plane.
        b: The coefficient of y in eqn of plane.
        c: The coefficient of z in eqn of plane.
        d: The constant term in eqn of plane.
        plane: Sequence of points that enclose the face.
    """
    face_coefficients = np.cross(face[0]-face[1], face[1]-face[2])
    d_plane = np.dot(face_coefficients, face[0])
    return None


def line_plane_intersection(pt1, pt2, pl1, pl2, pl3):
    '''
    In 3d space, finds the intersection of line given by two points
    with a plane given by three points.
    args:
        pt1: The first point of the line.
        pt2: The second point of the line.
        pl1: The first of three points from the plane.
        pl2: The second of three points from the plane.
        pl3: The third of three points from the plane.
    '''
    avec = np.cross((pl1 - pl2), (pl1 - pl3))
    d = np.dot(avec, pl1)
    if np.dot(avec, (pt2 - pt1)) > 1e-4:
        p = (d - np.dot(avec, pt1)) / (np.dot(avec, (pt2 - pt1)))
    else:
        p = 0.0
    return (1-p)*pt1 + p*pt2


def orient_face(poly):
    """
    When looking at the polygon from outside it,
    we need to ensure the vertices are in clockwise
    order. If the order is not correct, we use this method
    to flip the order of vertices. Used to identify back
    faces so that we don't have to render them.
    """
    cross_pdt = np.cross(poly[0]-poly[1], poly[1]-poly[2])
    # Assumes center of solid is at origin.
    out_vec = sum(poly)
    if np.dot(out_vec, cross_pdt) < 0:
        return np.flip(poly,axis=0)
    else:
        return poly


def draw_cube():
    """
    Draws a cube using only the vertices.
    Obtains faces using the scipy convex hull
    method.
    """
    c = Cube(3)
    verts = np.array([i.binary for i in c.vertices])-np.array([.5,.5,.5])
    hull = ConvexHull(verts)
    simps = hull.simplices
    planes = np.array([[verts[j] for j in i] for i in simps])
    for i in range(20):
        im = Image.new("RGB", (2048, 2048), (1,1,1))
        draw = ImageDraw.Draw(im,'RGBA')
        r = np.transpose(rotation(3,np.pi*(9+i)/15)) #i=9
        planes = [orient_face(pl) for pl in planes]
        render_solid_planes(planes, draw, r)
        im.save(".\\im" + str(i) + ".png")


class Polyhedron(object):
    __metaclass__ = abc.ABCMeta

    def render_solid_planes(self, draw, r, scale=300, shift=np.array([1000,1000,0]), 
                            debug=False, trnsp=255, make_edges=False, cut_back_face=True):
        render_solid_planes(self.planes, draw, r, scale, shift, debug, trnsp, make_edges)


class Dodecahedron(Polyhedron):
    def __init__(self):
        self.planes = self.get_planes()
        self.faces = self.planes

    def get_planes(self):
        """
        Returns the planes corresponding to all the faces of a Dodecahedron.
        Edges based on Cartesian coordinates section here: 
        https://en.wikipedia.org/wiki/Regular_dodecahedron
        """
        phi = (1+np.sqrt(5)) / 2
        tet_orig = []
        for i in [-1,1]:
            for j in [-1,1]:
                for k in [-1,1]:
                    tet_orig.append(np.array([i,j,k]))
        for i in [-1,1]:
            for j in [-1,1]:
                tet_orig.append(np.array([0,i*phi,j/phi]))
                tet_orig.append(np.array([i/phi,0,j*phi]))
                tet_orig.append(np.array([i*phi,j/phi,0]))
        tet_orig = np.array(tet_orig)
        r = rotation(3,np.pi/20.0)
        faces = []
        for pm1 in [-1,1]:
            coeff1 = np.array([1, pm1 * phi, 0])
            for i1 in range(3):
                for pm2 in [-1,1]:
                    coeff = np.array([coeff1[ (i1+jj)%3] for jj in range(3)])
                    penta = np.array([i for i in tet_orig \
                        if (np.dot(i, coeff ) + pm2*phi*phi == 0)])
                    #Rotate the pentagon slightly so that it's visible from the front.
                    #TODO: Need to rotate only when convex hull throws error.
                    penta_r = np.dot(penta,r)
                    penta_r_2d = [i[:2] for i in penta_r]
                    hull = ConvexHull(penta_r_2d).vertices
                    poly = np.array([penta[i] for i in hull])
                    #Does the cross product point outside?
                    poly = orient_face(poly)
                    faces.append(poly)
        return np.array(faces)


class Icosahedron(Polyhedron):
    def __init__(self):
        self.planes = self.get_planes()
        self.faces = self.planes

    def get_planes(self):
        """
        Returns the planes (or faces) of an Icosahedron.
        Based on (section on Cartesian coordinates) - 
        https://en.wikipedia.org/wiki/Regular_icosahedron
        """    
        phi = (1 + np.sqrt(5)) / 2.0
        mat_orig = np.array([
                [1, phi, 0],
                [0, 1, phi],
                [phi, 0, 1]
            ])
        faces = []
        for ii in [1, -1]:
            for jj in [1, -1]:
                for kk in [1, -1]:                
                    mat = np.copy(mat_orig)
                    mat[0,0] = mat[0,0] * ii
                    mat[1,0] = mat[1,0] * ii
                    mat[2,0] = mat[2,0] * ii
                    mat[0,1] = mat[0,1] * jj
                    mat[1,1] = mat[1,1] * jj
                    mat[2,1] = mat[2,1] * jj
                    mat[0,2] = mat[0,2] * kk
                    mat[1,2] = mat[1,2] * kk
                    mat[2,2] = mat[2,2] * kk
                    poly = mat
                    poly = orient_face(poly)
                    faces.append(poly)

        for ii in range(3):
            for kk in [1, -1]:
                for ll in [1, -1]:
                    mat = np.copy(mat_orig)
                    mat[0, ii] = kk * mat[0, ii]
                    mat[1, ii] = kk * mat[1, ii]
                    mat[2, ii] = kk * mat[2, ii]
                    mat[0, (ii+2)%3] = ll * mat[0, (ii+2)%3]
                    mat[1, (ii+2)%3] = ll * mat[1, (ii+2)%3]
                    mat[2, (ii+2)%3] = ll * mat[2, (ii+2)%3]
                    for jj in range(3):
                        mat[ii,jj] = mat[(ii+1)%3,jj]
                    mat[ii, (ii+1)%3] = -1 * mat[ii, (ii+1)%3]
                    poly = mat
                    poly = orient_face(poly)
                    faces.append(poly)
        return np.array(faces)


class Tetrahedron(Polyhedron):
    def __init__(self):
        v = np.array([
            [1,1,1],
            [-1,-1,1],
            [1,-1,-1],
            [-1,1,-1]
        ])
        self.vertices = v/2/np.sqrt(2)
        self.planes = self.get_planes()
        self.faces = self.planes
        self.edges = self.get_edges()

    def get_planes(self):
        faces = []
        for i in range(4):
            face_ind = [f for f in range(4) if f != i] #TODO: Is there a better way to exclude indices?
            face = orient_face(self.vertices[face_ind])
            faces.append(face)
        return np.array(faces)

    def get_edges(self):
        edges = []
        for i in range(4):
            for j in range(i+1,4):
                edges.append([self.vertices[i],self.vertices[j]])
        return np.array(edges)


class Octahedron(Polyhedron):
    def __init__(self):
        self.vertices = np.array([
            [0,0,0],
            [1,0,0],
            [0,1,0],
            [1,1,0],
            [0.5,0.5,0.7071],
            [0.5,0.5,-0.7071]
        ])
        self.vertices = self.vertices - sum(self.vertices)/6.0
        self.planes = self.get_planes()
        self.faces = self.planes

    def get_planes(self):
        ver_top1 = self.vertices[4]
        ver_top2 = self.vertices[5]
        indxs = [0,1,3,2]
        faces = []
        for i in range(4):
            k = indxs[(i) % 4]
            l = indxs[(i+1) % 4]
            ver1 = self.vertices[k]
            ver2 = self.vertices[l]
            face1 = np.array([ver1,ver2,ver_top1])
            face2 = np.array([ver1,ver2,ver_top2])
            faces.append(orient_face(face1))
            faces.append(orient_face(face2))
        return np.array(faces)



def tetartoid_face(a,b,c):
    """
    Based on section on Tetartoid presented here - 
    https://en.wikipedia.org/wiki/Dodecahedron
    TODO: Include this in the class.
    """
    if a>b or b>c or a>c:
        print("This method requires a<b<c.")
        return
    n = a**2*c-b*c**2
    d1 = a**2-a*b+b**2+a*c-2*b*c
    d2 = a**2+a*b+b**2-a*c-2*b*c
    if n*d1*d2 == 0:
        print("Something is wrong with the arguments")
        return
    return np.array([
                    [a,b,c],
                    [-a,-b,c],
                    [-n/d1,-n/d1,n/d1],
                    [-c,-a,b],
                    [-n/d2,n/d2,n/d2]
                ])


class Tetartoid(Polyhedron):
    """
    A tetartoid is an intermediate solid betweeen a tetrahedron and dodecahedron.
    The construction is based on - https://math.stackexchange.com/a/1396300/155881
    For s=0.33, t=0.33 we get a cube.
    For s=0.404508, t=0.0954913 produce a Dodecahedron.
    For t=0, we get a Tetrahedron.
    """
    def __init__(self,s=0.3,t=0.04):
        self.planes = self.get_planes(s, t)

        self.dual_face_indices = np.array([
            [0,1,2],
            [3,4,5],
            [6,7,8],
            [9,10,11],
            [0,1,3],
            [0,3,5],
            [0,5,6],
            [0,2,6],
            [1,2,10],
            [1,9,11],
            [1,3,11],
            [2,6,7],
            [2,7,9],
            [3,4,11],
            [4,5,8],
            [5,6,8],
            [7,9,10],
            [7,8,10],
            [4,10,11],
            [1,2,9]
        ])

        ## The side lengths of the pentagon.
        bsq = ((1 + 3* (-1 + s)* s + (-1 + t)* t)* (3* (1 - 2* s)**2 *s**2 + \
            2* (1 - 2* s)* s* t + (3 + 4* s* (-3 + 4* s))* t**2 - 4* t**3 + \
            4* t**4)) / (-3* s + 6* s**2 + t* (-1 + 2* t))**2
        self.b = np.sqrt(bsq)

        csq = ((s**2 + 3* t**2)* (-4* s**3 + 4* s**4 + 2* s* (1 - 6* t)* t + \
            t**2* (5 + 12* (-1 + t)* t) + \
            s**2* (1 + 4* t* (-1 + 4* t))))/(s* (-1 + 2* s) - 3* t + 6* t**2)**2
        self.c = np.sqrt(csq)

        asq = 1 - 4* s + 4* s**2 + 4 *t**2
        self.a = np.sqrt(asq)
        
    
    def get_planes(self, s=0.3, t=0.04):
        # We start with the tetrahedron vertices.
        v = np.array([
            [1,1,1],
            [-1,-1,1],
            [1,-1,-1],
            [-1,1,-1]
        ])
        # Make it a tetrahedron with unit edges.
        v = v/2/np.sqrt(2)
        # For each edge V_i V_j, construct two points P_ij and P_ji having a fixed distance s from V_i and V_j.
        p = np.zeros((4,4,3))
        for i in range(4):
            for j in range(i+1, 4):
                p[i, j] = (1-s)*v[i] + s*v[j]
                p[j, i] = s*v[i] + (1-s)*v[j]
        # Join the center C_ijk of every face V_i V_j V_k with P_ij, P_jk and P_ik.
        c = np.zeros((4, 3))
        for i in range(4):
            face = [f for f in range(4) if f != i] #TODO: Is there a better way to exclude indices?
            c[i] = sum(v[face]) / 3
        # Now let o be the tetartoid center.
        o = np.array([0,0,0])
        # Consider the six planes o v_i v_j passing through the center and each edge.
        # From point p_ij, draw the perpendicular line to o v_i v_j and take on it
        # a point q_ij such that p_ij q_ij = t.
        q = np.zeros((4, 4, 3))
        for i in range(4):
            for j in range(i+1, 4):
                directn = np.cross(v[i]-o, v[j]-o)
                directn = directn / np.sqrt(sum(directn**2))
                q[i, j] = p[i, j] + directn * t
                q[j, i] = p[j, i] - directn * t

        planes = [
            [c[3], q[2,0], q[0,2], v[0], q[0,1]],
            [c[3], q[1,2], q[2,1], v[2], q[2,0]],#
            [c[3], q[0,1], q[1,0], v[1], q[1,2]],#

            [c[1], q[0,2], q[2,0], v[2], q[2,3]],#
            [c[1], q[2,3], q[3,2], v[3], q[3,0]],
            [c[1], q[3,0], q[0,3], v[0], q[0,2]],#

            [c[2], q[1,0], q[0,1], v[0], q[0,3]],#
            [c[2], q[3,1], q[1,3], v[1], q[1,0]],
            [c[2], q[0,3], q[3,0], v[3], q[3,1]],

            [c[0], q[2,1], q[1,2], v[1], q[1,3]],
            [c[0], q[1,3], q[3,1], v[3], q[3,2]],
            [c[0], q[3,2], q[2,3], v[2], q[2,1]]
        ]
        planes = np.array(planes)
        for plane in planes:
            cprime = line_plane_intersection(o, plane[0], plane[1], plane[2], plane[4])
            vprime = line_plane_intersection(o, plane[3], plane[1], plane[2], plane[4])
            plane[0] = cprime
            plane[3] = vprime
        vertices = []
        for i in range(4):
            for j in range(i+1,4):
                vertices.append(q[i,j])
                vertices.append(q[j,i])
        for i in range(4):
            vertices.append(c[i])
        for i in range(4):
            vertices.append(v[i])
        self.vertices = np.array(vertices)
        self.qs = q
        self.cs = np.array([planes[9,0],planes[3,0],planes[6,0],planes[0,0]])
        self.vs = np.array([planes[0,3],planes[2,3],planes[1,3],planes[4,3]])
        return np.array(planes)


def draw_coin(basedir = '.\\images\\RotatingCube\\'):
	verts = 15
	width= 2
	polygon = np.array([[3*np.cos(2*np.pi/verts*n), 3*np.sin(2*np.pi/verts*n),1] \
						for n in np.arange(1,verts+1)])
	planes = [polygon]
	for j in range(verts):
		poly = [polygon[j], polygon[(j+1)%verts], \
			polygon[(j+1)%verts]-np.array([0,0,width]), polygon[(j)]-np.array([0,0,width])]
		planes.append(poly)
	planes.append(polygon+np.array([0,0,-width]))
	for ii in range(20):
		im = Image.new("RGB", (1024, 1024), (1,1,1))
		draw = ImageDraw.Draw(im,'RGBA')
		r = general_rotation(np.array([0,1,0]),2*np.pi/20*ii)
		render_solid_planes(planes, draw, r, shift=np.array([512, 512, 0]), scale=75)
		im.save(basedir + "im" + str(ii) + ".png")


########################################################################
## Everything below this is old, outdated code kept here for legacy reasons.
########################################################################

# A global variable used for investigating the angles the 
# faces of polyhedons make with a light source. 
# This is later used to shade them appropriately.
angles = []

def plot_polyhedron(draw, tet_orig, r, shift, scale = 300, thresh = 1.24):
    """
    Plots all the vertices of a polyhedron.
    """
    font = ImageFont.truetype("arial.ttf", 25)
    tet = np.dot(tet_orig, r)
    j = 0
    for i in tet:
        ver = i * scale + shift
        draw.ellipse((ver[0]-9,ver[1]-9,ver[0]+9,ver[1]+9), fill = (255,183,31))
        # For debugging - in case one wants to see how vertices at various coordinates relate to each other.
        #draw.text((ver[0],ver[1]), str(round(tet_orig[j][0],2) ) + "," + str(round(tet_orig[j][1],2 )) + "," + str(round(tet_orig[j][2],2)), font=font, fill = (255,255,255))
        j = j + 1


def octahedron(draw, r, shift = [1000,1000,0], scale = 300):
    """
    Draws the vertices, edges and faces of an Octahedron.
    """
    tet_orig = np.array([
            [0,0,0],
            [1,0,0],
            [0,1,0],
            [1,1,0],
            [0.5,0.5,0.7071],
            [0.5,0.5,-0.7071]
        ])
    tet_orig = tet_orig - sum(tet_orig)/6.0
    tet = np.dot(tet_orig, np.transpose(r)) * scale + shift
    ver_top1 = tet[4]
    ver_top2 = tet[5]
    indxs = [0,1,3,2]
    for i in range(4):
        k = indxs[(i) % 4]
        l = indxs[(i+1) % 4]
        ver1 = tet[k]
        ver2 = tet[l]
        face1 = np.array([ver1,ver2,ver_top1])
        face2 = np.array([ver1,ver2,ver_top2])
        for face in [face1, face2]:
            smat = sum(face)
            face_angle = np.dot(smat/np.sqrt(sum(smat**2)), np.array([0,0.01,0.99]))
            #angles.append(face_angle)
            forward_face = np.dot(smat, np.array([0,0,1])) > -1e-3
            poly = [(ver[0], ver[1]) for ver in face]
            if forward_face:
                rgba = colorFromAngle2(face_angle,h=155,s=143,maxx=0.1)
                draw.polygon(poly, rgba)


def tetrahedron(draw, r, im, theta = np.pi/12, shift = np.array([1000,1000,0]), scale = 150, rgb = (216,52,52), ind = 0):
    """
    Draws the vertices, edges and faces of a Tetrahedron.
    """
    im_sun = Image.open('C:\\Users\\rohit\\Documents\\GitHub\\base\\numerical\\python\\visualization\\Animation\\Images\\Misc\\Sun' + str(ind%2) + '.jpg')
    im_sun.thumbnail((150,150), Image.ANTIALIAS)
    tet_orig = np.array([
            [1,1,1],
            [-1,-1,1],
            [1,-1,-1],
            [-1,1,-1]
        ])
    rgba = rgb + (100,)
    tet = np.dot(tet_orig,r)
    for i in tet:
        ver = i * scale + shift
        draw.ellipse((ver[0]-5,ver[1]-5,ver[0]+5,ver[1]+5), fill = rgb)
    bulb = np.array([-2.5,0,0,]) * scale + shift[:3]
    draw.ellipse((bulb[0]-5,bulb[1]-5,bulb[0]+5,bulb[1]+5), fill = rgb)
    pasteImage(im_sun, im, bulb-np.array([50,50,0]))
    for i in range(len(tet)):
        for k in range(i,len(tet)):
            ver1 = tet[i] * scale + shift
            ver2 = tet[k] * scale + shift
            draw.line((ver1[0],ver1[1],ver2[0],ver2[1]), fill = rgb, width = 5)
            ver1prime = project_on_plane(bulb, ver1)
            ver2prime = project_on_plane(bulb, ver2)
            draw.line((ver1prime[0],ver1prime[1],ver2prime[0],ver2prime[1]), fill = rgb, width = 2)
    draw_plane(draw, scale)


def icosahedron(draw, r, shift = [1000,1000,0], scale = 300):
    """
    Plots the vertices of an Icosahedron and the faces along with edges.
    """
    phi = (1+np.sqrt(5))/2
    tet_orig = []
    for i in [-1, 1]:
        for j in [-1, 1]:
            tet_orig.append(np.array([0,i,j*phi]))
            tet_orig.append(np.array([j*phi,0,i]))
            tet_orig.append(np.array([i,j*phi,0]))
    draw_icosahedron_planes(draw, r, scale, shift)


def draw_icosahedron_planes(draw, r, scale = 300, shift = np.array([1000,1000,0])):
    """
    Draws the planes (or faces) of an Icosahedron.
    """
    cind = -1
    phi = (1 + np.sqrt(5)) / 2.0
    mat_orig = np.array([
            [1, phi, 0],
            [0, 1, phi],
            [phi, 0, 1]
        ])
    for ii in [1, -1]:
        for jj in [1, -1]:
            for kk in [1, -1]:
                cind += 1
                mat = np.copy(mat_orig)
                mat[0,0] = mat[0,0] * ii
                mat[1,0] = mat[1,0] * ii
                mat[2,0] = mat[2,0] * ii
                mat[0,1] = mat[0,1] * jj
                mat[1,1] = mat[1,1] * jj
                mat[2,1] = mat[2,1] * jj
                mat[0,2] = mat[0,2] * kk
                mat[1,2] = mat[1,2] * kk
                mat[2,2] = mat[2,2] * kk
                mat1 = np.dot(mat, r) * scale + shift[:3]
                smat = sum(mat1)
                forward_face = np.dot(smat, np.array([0,0,1])) > -1e-3
                face_angle = np.dot(smat/np.sqrt(sum(smat**2)), np.array([0,0.01,0.99]))
                if forward_face:
                    poly = [(mat1[i][0],mat1[i][1]) for i in range(len(mat1))]
                    rgba = colorFromAngle2(face_angle,h=153,s=120,maxx=0.25)
                    draw.polygon(poly, rgba)
                    #uncomment if you want to plot edges
                    #for line in range(len(mat1)):
                    #    draw.line((mat1[line][0],mat1[line][1],mat1[(line+1)%3][0],mat1[(line+1)%3][1]), fill = (0,255,0,255), width = 5)
                #else:
                #    for line in range(len(mat1)):
                #        draw.line((mat1[line][0],mat1[line][1],mat1[(line+1)%3][0],mat1[(line+1)%3][1]), fill = (0,255,0,255), width = 3)
    for ii in range(3):
        for kk in [1, -1]:
            for ll in [1, -1]:
                cind += 1
                mat = np.copy(mat_orig)
                mat[0, ii] = kk * mat[0, ii]
                mat[1, ii] = kk * mat[1, ii]
                mat[2, ii] = kk * mat[2, ii]
                mat[0, (ii+2)%3] = ll * mat[0, (ii+2)%3]
                mat[1, (ii+2)%3] = ll * mat[1, (ii+2)%3]
                mat[2, (ii+2)%3] = ll * mat[2, (ii+2)%3]
                for jj in range(3):
                    mat[ii,jj] = mat[(ii+1)%3,jj]
                mat[ii, (ii+1)%3] = -1 * mat[ii, (ii+1)%3]
                mat1 = np.dot(mat, r) * scale + shift[:3]
                smat = sum(mat1)
                forward_face = np.dot(smat, np.array([0,0,1])) > -1e-3
                face_angle = np.dot(smat/np.sqrt(sum(smat**2)), np.array([0,0.01,0.99]))
                if forward_face:
                    poly = [(mat1[i][0],mat1[i][1]) for i in range(len(mat1))]
                    rgba = colorFromAngle2(face_angle,h=153,s=120,maxx=0.25)
                    draw.polygon(poly, rgba)
                    # Uncomment if you want to plot edges.
                    #for line in range(len(mat1)):
                    #    draw.line((mat1[line][0],mat1[line][1],mat1[(line+1)%3][0],mat1[(line+1)%3][1]), fill = (0,255,0,255), width = 5)
                #else:
                #    for line in range(len(mat1)):
                #        draw.line((mat1[line][0],mat1[line][1],mat1[(line+1)%3][0],mat1[(line+1)%3][1]), fill = (0,255,0,255), width = 3)



def dodecahedron(draw, r, shift = [1000,1000,0], scale = 300):
    """
    Draws the vertices, faces and edges of a dodecahedron.
    """
    phi = (1+np.sqrt(5)) / 2
    tet_orig = []
    for i in [-1,1]:
        for j in [-1,1]:
            for k in [-1,1]:
                tet_orig.append(np.array([i,j,k]))
    phi = (1+np.sqrt(5))/2
    for i in [-1,1]:
        for j in [-1,1]:
            tet_orig.append(np.array([0,i*phi,j/phi]))
            tet_orig.append(np.array([i/phi,0,j*phi]))
            tet_orig.append(np.array([i*phi,j/phi,0]))
    tet_orig = np.array(tet_orig)
    draw_dodecahedron_planes(draw, r, tet_orig, scale, shift)


def draw_dodecahedron_planes(draw, r, tet_orig, scale = 300, shift = np.array([1000,1000,0])):
    """
    Draws all the faces of a Dodecahedron.
    """
    phi = (1+np.sqrt(5)) / 2
    cind = -1
    for pm1 in [-1,1]:
        coeff1 = np.array([1, pm1 * phi, 0])
        for i1 in range(3):
            for pm2 in [-1,1]:
                cind += 1
                coeff = np.array([coeff1[ (i1+jj)%3] for jj in range(3)])
                penta = np.array([i for i in tet_orig if (np.dot(i, coeff ) + pm2*phi*phi == 0)])
                penta = np.dot(penta, r)
                try:
                    hull = ConvexHull([i[:2] for i in penta]).vertices
                    sqr1 = penta * scale + shift[:3]
                    poly = [(sqr1[i][0],sqr1[i][1]) for i in hull]
                    smat = sum(penta)
                    face_angle = np.dot(smat/np.sqrt(sum(smat**2)), np.array([0,0.01,0.99]))
                    forward_face = np.dot(sum(penta), np.array([0,0,1])) > -1e-3
                    angles.append(face_angle)
                    rgba = colorFromAngle2(face_angle,h=134,s=144,maxx=0.95)
                    #if forward_face: #Meaning the plane is facing forward.
                    if True:
                        draw.polygon(poly, rgba)
                        ## Uncomment if you want to draw the edges.
                        #for i in range(len(poly)):
                        #    vv1 = poly[i]
                        #    vv2 = poly[(i+1)%5]
                        #    if forward_face:
                        #        draw.line((vv1[0],vv1[1],vv2[0],vv2[1]), fill = (0,255,0,255), width = 3)
                        #    else:
                        #        draw.line((vv1[0],vv1[1],vv2[0],vv2[1]), fill = (0,255,0,255), width = 3)
                except:
                    pass


def dodecahedron_planes():
    """
    Returns the planes corresponding to all the faces of a Dodecahedron.
    Edges based on Cartesian coordinates section here: https://en.wikipedia.org/wiki/Regular_dodecahedron
    """
    phi = (1+np.sqrt(5)) / 2
    tet_orig = []
    for i in [-1,1]:
        for j in [-1,1]:
            for k in [-1,1]:
                tet_orig.append(np.array([i,j,k]))
    for i in [-1,1]:
        for j in [-1,1]:
            tet_orig.append(np.array([0,i*phi,j/phi]))
            tet_orig.append(np.array([i/phi,0,j*phi]))
            tet_orig.append(np.array([i*phi,j/phi,0]))
    tet_orig = np.array(tet_orig)
    r = rotation(3,np.pi/20.0)
    faces = []
    for pm1 in [-1,1]:
        coeff1 = np.array([1, pm1 * phi, 0])
        for i1 in range(3):
            for pm2 in [-1,1]:
                coeff = np.array([coeff1[ (i1+jj)%3] for jj in range(3)])
                penta = np.array([i for i in tet_orig if (np.dot(i, coeff ) + pm2*phi*phi == 0)])
                #Rotate the pentagon slightly so that it's visible from the front.
                #TODO: Need to rotate only when convex hull throws error.
                penta_r = np.dot(penta,r)
                penta_r_2d = [i[:2] for i in penta_r]
                hull = ConvexHull(penta_r_2d).vertices
                poly = np.array([penta[i] for i in hull])
                #Does the cross product point outside?
                cross_pdt = np.cross(poly[0]-poly[1], poly[1]-poly[2])
                #A vector pointing outside.
                out_vec = sum(poly)
                if np.dot(out_vec, cross_pdt) < 0:
                    poly = np.flip(poly,axis=0)
                faces.append(poly)
    return np.array(faces)



def icosahedron_planes():
    """
    Draws the planes (or faces) of an Icosahedron.
    Based on (section on Cartesian coordinates) - https://en.wikipedia.org/wiki/Regular_icosahedron
    """    
    phi = (1 + np.sqrt(5)) / 2.0
    mat_orig = np.array([
            [1, phi, 0],
            [0, 1, phi],
            [phi, 0, 1]
        ])
    faces = []
    for ii in [1, -1]:
        for jj in [1, -1]:
            for kk in [1, -1]:                
                mat = np.copy(mat_orig)
                mat[0,0] = mat[0,0] * ii
                mat[1,0] = mat[1,0] * ii
                mat[2,0] = mat[2,0] * ii
                mat[0,1] = mat[0,1] * jj
                mat[1,1] = mat[1,1] * jj
                mat[2,1] = mat[2,1] * jj
                mat[0,2] = mat[0,2] * kk
                mat[1,2] = mat[1,2] * kk
                mat[2,2] = mat[2,2] * kk
                poly = mat
                cross_pdt = np.cross(poly[0]-poly[1], poly[1]-poly[2])
                #A vector pointing outside.
                out_vec = sum(poly)
                if np.dot(out_vec, cross_pdt) < 0:
                    poly = np.flip(poly,axis=0)
                faces.append(poly)              

    for ii in range(3):
        for kk in [1, -1]:
            for ll in [1, -1]:
                mat = np.copy(mat_orig)
                mat[0, ii] = kk * mat[0, ii]
                mat[1, ii] = kk * mat[1, ii]
                mat[2, ii] = kk * mat[2, ii]
                mat[0, (ii+2)%3] = ll * mat[0, (ii+2)%3]
                mat[1, (ii+2)%3] = ll * mat[1, (ii+2)%3]
                mat[2, (ii+2)%3] = ll * mat[2, (ii+2)%3]
                for jj in range(3):
                    mat[ii,jj] = mat[(ii+1)%3,jj]
                mat[ii, (ii+1)%3] = -1 * mat[ii, (ii+1)%3]
                poly = mat
                cross_pdt = np.cross(poly[0]-poly[1], poly[1]-poly[2])
                #A vector pointing outside.
                out_vec = sum(poly)
                if np.dot(out_vec, cross_pdt) < 0:
                    poly = np.flip(poly,axis=0)
                faces.append(poly)
    return np.array(faces)


def tetartoid_planes(s=0.3, t=0.04):
    '''
    Draws a tetartoid. Based on the answer by Arentino here -
    https://math.stackexchange.com/questions/1393370/what-are-the-rules-for-a-tetartoid-pentagon
    args:
        s: 0 <= s <= 0.5.
    '''
    v = np.array([
            [1,1,1],
            [-1,-1,1],
            [1,-1,-1],
            [-1,1,-1]
        ])
    # Make it a tetrahedron with unit edges.
    v = v/2/np.sqrt(2)
    # For each edge V_i V_j, construct two points P_ij and P_ji having a fixed distance s from V_i and V_j.
    p = np.zeros((4,4,3))
    for i in range(4):
        for j in range(i+1, 4):
            p[i, j] = (1-s)*v[i] + s*v[j]
            p[j, i] = s*v[i] + (1-s)*v[j]
    # Join the center C_ijk of every face V_i V_j V_k with P_ij, P_jk and P_ik.
    c = np.zeros((4, 3))
    for i in range(4):
        face = [f for f in range(4) if f != i] #TODO: Is there a better way to exclude indices?
        c[i] = sum(v[face]) / 3
    # Now let o be the tetartoid center.
    o = np.array([0,0,0])
    # Consider the six planes o v_i v_j passing through the center and each edge.
    # From point p_ij, draw the perpendicular line to o v_i v_j and take on it
    # a point q_ij such that p_ij q_ij = t.
    q = np.zeros((4, 4, 3))
    for i in range(4):
        for j in range(i+1, 4):
            directn = np.cross(v[i]-o, v[j]-o)
            directn = directn / np.sqrt(sum(directn**2))
            q[i, j] = p[i, j] + directn * t
            q[j, i] = p[j, i] - directn * t

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
        cprime = line_plane_intersection(o, plane[0], plane[1], plane[2], plane[4])
        vprime = line_plane_intersection(o, plane[3], plane[1], plane[2], plane[4])
        plane[0] = cprime
        plane[3] = vprime
    return np.array(planes)


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
    v = np.dot(r, np.transpose(tet_orig)) * scale
    v = np.transpose(v) + shift[:3]
    # For each edge V_i V_j, construct two points P_ij and P_ji having a fixed distance s from V_i and V_j.
    p = np.zeros((4,4,3))
    for i in range(4):
        for j in range(i+1, 4):
            p[i, j] = (1-s)*v[i] + s*v[j]
            p[j, i] = s*v[i] + (1-s)*v[j]
    # Join the center C_ijk of every face V_i V_j V_k with P_ij, P_jk and P_ik.
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
        cprime = line_plane_intersection(o, plane[0], plane[1], plane[2], plane[4])
        vprime = line_plane_intersection(o, plane[3], plane[1], plane[2], plane[4])
        plane[0] = cprime
        plane[3] = vprime
        smat = sum(plane - o)
        face_angle = np.dot(smat/np.sqrt(sum(smat**2)), np.array([0,0.01,0.99]))
        rgba = colorFromAngle2(face_angle,h=153,s=120,maxx=0.60)
        poly = [(i[0], i[1]) for i in plane]
        draw.polygon(poly, fill=rgba)



def platonic_solids(basedir=".\\"):
    """
    @MoneyShot
    Draws out an Icosahedron and Dodecahedron.
    args:
        basedir:The directory where the images are to be saved.
            In the main pyray repo, basedir is ..\\images\\RotatingCube\\
    """
    for i in range(0, 31):
        im = Image.new("RGB", (2048, 2048), (1,1,1))
        draw = ImageDraw.Draw(im,'RGBA')
        r = np.transpose(rotation(3,np.pi*(9+i)/15)) #i=9
        dodecahedron(draw, r, shift = np.array([370, 1270, 0]), scale = 150)
        icosahedron(draw, r, shift = np.array([1470, 1270, 0]), scale = 150)
        tetrahedron(draw, r, shift = np.array([333, 470, 0]), scale = 150)
        octahedron(draw, r, shift = np.array([1477, 470, 0]), scale = 150)
        im.save(basedir + "im" + str(i) + ".png")


def draw_tetartoid(basedir=".\\"):
    """
    @MoneyShot
    Draws out a Tetartoid.
    args:
        basedir:The directory where the images are to be saved.
            In the main pyray repo, basedir is ..\\images\\RotatingCube\\
    """
    for i in range(0, 31):
        im = Image.new("RGB", (2048, 2048), (1,1,1))
        draw = ImageDraw.Draw(im,'RGBA')
        r = np.transpose(rotation(3,np.pi*(9+i)/15)) #i=9
        tetartoid(draw, r, t=0.1)
        im.save(basedir + "im" + str(i) + ".png")

