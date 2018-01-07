'''
To render 3d scenes (or even high dimensional), the first thing we need is the ability to rotate the objects we render 
and view them from different angles. This can be done with rotation matrices or quaternions. I favor the former since 
they are simpler and can be used in spaces of arbitrary dimensionality.
Rotation matrices are simply collections of orthonormal vectors that form a basis of the space we are in.
In this module are provided methods to generate various kinds of rotation matrices.
'''

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageMath
import sys


'''
Returns a simple planar rotation matrix that rotates vectors around the x-axis.
args:
    theta: The angle by which we will perform the rotation.
'''
def yzrotation(theta = np.pi*3/20.0):
    r = np.eye(3)
    r[1,1] = np.cos(theta)
    r[1,2] = -np.sin(theta)
    r[2,1] = np.sin(theta)
    r[2,2] = np.cos(theta)
    return r

'''
Returns a three dimensional rotation matrix given the axis to rotate about and the angle to rotate by.
args:
    a: The axis to rotate about
    theta: The angle to rotate by.
'''
def general_rotation(a, theta):
    c = np.cos(theta)
    s = np.sin(theta)
    a = a/sum(a**2)**0.5
    [ax,ay,az] = a[:3]
    return np.array(
        [
            [c + ax**2 * (1-c), ax*ay*(1-c) - az*s, ax*az*(1-c) + ay*s],
            [ay*ax*(1-c)+az*s, c + ay**2*(1-c), ay*az*(1-c)-ax*s],
            [az*ax*(1-c)-ay*s, az*ay*(1-c) + ax*s, c+az**2*(1-c)]
        ])

'''
A wrapper to general_rotation named more appropriately. Returns a rotation matrix that rotates about an axis by an angle.
args:
    a: The axis to rotate about
    theta: The angle to rotate by. 
'''
def axisangle(a, theta):
    return general_rotation(a,theta)


'''
For a rotation matrix in 3 dimensions (rotations about the origin), we need 4 parameters. 
An axis about which we are going to rotate and an angle which is the extent of rotation.
This method takes the rotation matrix in as input and returns an axis and angle combination that would generate that matrix.
args:
    m: The rotation matrix (collection of orthonormal vectors in a matrix).
'''
def matrix_to_axisangle(m):
    theta = np.arccos(( m[0,0] + m[1,1] + m[2,2] - 1)/2)
    x = (m[2,1] - m[1,2])/np.sqrt((m[2,1] - m[1,2])**2+(m[0,2] - m[2,0])**2+(m[1,0] - m[0,1])**2)
    y = (m[0,2] - m[2,0])/np.sqrt((m[2,1] - m[1,2])**2+(m[0,2] - m[2,0])**2+(m[1,0] - m[0,1])**2)
    z = (m[1,0] - m[0,1])/np.sqrt((m[2,1] - m[1,2])**2+(m[0,2] - m[2,0])**2+(m[1,0] - m[0,1])**2)
    return (theta, np.array([x,y,z]))

'''
Returns an general rotation matrix of any dimensionality. This is acheived by a sequence of succesive 2d rotations.
args:
    n : The dimensionality of the space in which we are going to rotate things.
    theta: The angle of rotation for each of the planar 2-d rotation matrices.
'''
def rotation(n, theta = np.pi/3):
    r = np.eye(n)
    for i in range(n):
        for j in range(i+1,n):
            rij = np.eye(n)
            rij[i,i] = np.cos(theta)
            rij[i,j] = -np.sin(theta)
            rij[j,i] = np.sin(theta)
            rij[j,j] = np.cos(theta)
            r = np.dot(r,rij)
    return r

'''
A sequence of intermediate rotations that take the system from an initial rotated state (oldr) to a final one (newr).
args:
    i: 1 means complete rotation to new coordinates, 0 means old rotation.
    oldr: Old rotation matrix.
    newr: New rotation matrix.
'''
def rotation_transition(i = 0, oldr = general_rotation(np.array([1,0,0]),np.pi/2), newr = rotation(3,2*np.pi*4/30.0)):
    transn = np.dot(newr,np.transpose(oldr))
    (theta, vec) = matrix_to_axisangle(transn)
    r = general_rotation(vec, i*theta)
    return np.dot(r, oldr)

'''
What rotation matrix is needed to rotate an old vector to a new vector.
args:
    oldvec: The vector we are starting with.
    newvec: The vector to which we are rotating.
'''
def rotate_vec2vec(oldvec, newvec):
    axis = np.cross(oldvec, newvec)
    oldvec1 = oldvec / np.sqrt(sum(oldvec**2))
    newvec1 = newvec / np.sqrt(sum(newvec**2))
    theta = np.arccos(sum(oldvec1*newvec1))
    return axisangle(axis, theta)

