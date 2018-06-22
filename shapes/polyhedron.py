'''
All kinds of polyhedra. Like Platonic solids, Archimedean solids, Tetartoids, etc.
'''

import numpy as np
from scipy.spatial import ConvexHull
from misc import *
from rotation.rotation import *
from utils.color import *

# A global variable used for investigating the angles the faces of polyhedons make with a light source. This is later used to shade them appropriately.
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
    icosahedron_planes(draw, r, scale, shift)


def icosahedron_planes(draw, r, scale = 300, shift = np.array([1000,1000,0])):
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
    dodecahedron_planes(draw, r, tet_orig, scale, shift)


def dodecahedron_planes(draw, r, tet_orig, scale = 300, shift = np.array([1000,1000,0])):
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
                hull = ConvexHull([i[:2] for i in penta]).vertices
                sqr1 = penta * scale + shift[:3]
                poly = [(sqr1[i][0],sqr1[i][1]) for i in hull]
                smat = sum(penta)
                face_angle = np.dot(smat/np.sqrt(sum(smat**2)), np.array([0,0.01,0.99]))
                forward_face = np.dot(sum(penta), np.array([0,0,1])) > -1e-3
                angles.append(face_angle)
                rgba = colorFromAngle2(face_angle,h=134,s=144,maxx=0.95)
                if forward_face: #Meaning the plane is facing forward.
                    draw.polygon(poly, rgba)
                    ## Uncomment if you want to draw the edges.
                    #for i in range(len(poly)):
                    #    vv1 = poly[i]
                    #    vv2 = poly[(i+1)%5]
                    #    if forward_face:
                    #        draw.line((vv1[0],vv1[1],vv2[0],vv2[1]), fill = (0,255,0,255), width = 3)
                    #    else:
                    #        draw.line((vv1[0],vv1[1],vv2[0],vv2[1]), fill = (0,255,0,255), width = 3)


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
        [c[0], q[1,3], q[1,3], v[3], q[3,2]],
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
        #dodecahedron(draw, r, shift = np.array([370, 1270, 0]), scale = 150)
        #icosahedron(draw, r, shift = np.array([1470, 1270, 0]), scale = 150)
        tetartoid(draw, r, t=0.1)
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

