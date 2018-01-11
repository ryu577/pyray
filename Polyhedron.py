'''
All kinds of polyhedra. Like Platonic solids, Archimedean solids, Tetartoids, etc.
'''

import numpy as np
from Misc import *
from Rotation import *

'''
Plots the vertices of an Icosahedron and the faces along with edges.
'''
def icosahedron(draw, r, shift = [1000,1000,0], scale = 300):
    phi = (1+np.sqrt(5))/2
    tet_orig = []
    for i in [-1, 1]:
        for j in [-1, 1]:
            tet_orig.append(np.array([0,i,j*phi]))
            tet_orig.append(np.array([j*phi,0,i]))
            tet_orig.append(np.array([i,j*phi,0]))
    #plot_polyhedron(draw, tet_orig, r, offset, scale, thresh = 2.01)
    icosahedron_planes(draw, r, scale, shift)

'''
Draws the planes (or faces) of an Icosahedron.
'''
def icosahedron_planes(draw, r, scale = 300, shift = np.array([1000,1000,0])):
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
                    rgba = colorFromAngle2(face_angle,h=215,s=128,maxx=0.25)
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
                    rgba = colorFromAngle2(face_angle,h=215,s=128,maxx=0.25)
                    draw.polygon(poly, rgba)
                    #uncomment if you want to plot edges.
                    #for line in range(len(mat1)):
                    #    draw.line((mat1[line][0],mat1[line][1],mat1[(line+1)%3][0],mat1[(line+1)%3][1]), fill = (0,255,0,255), width = 5)
                #else:
                #    for line in range(len(mat1)):
                #        draw.line((mat1[line][0],mat1[line][1],mat1[(line+1)%3][0],mat1[(line+1)%3][1]), fill = (0,255,0,255), width = 3)




