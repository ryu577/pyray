"""
To render 3d scenes (or even high dimensional), the first thing we need is
the ability to rotate the objects we render and view them from different angles.
This can be done with rotation matrices or quaternions.
We favor the rotation matrix since they are simpler and can be used in spaces of arbitrary dimensionality.
Rotation matrices are simply collections of orthonormal vectors that form a basis of the space we are in.
This module provides methods to generate various kinds of rotation matrices.
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageMath

# from pyquaternion import Quaternion


def planar_rotation(theta=np.pi * 3 / 20.0):
    """
    Returns a simple planar rotation matrix for rotating vectors
    in the 2-d plane about the origin.
    args:
        theta: The angle by which we will perform the rotation.
    """
    r = np.eye(2)
    r[0, 0] = np.cos(theta)
    r[1, 0] = -np.sin(theta)
    r[0, 1] = np.sin(theta)
    r[1, 1] = np.cos(theta)
    return r


def generalized_planar_rotation(pt, center, r):
    """
    Rotates a 2-d point about a central point.
    args:
        pt: The point to rotate.
        center: The point about which to rotate.
        theta: The angle by which we will perform the rotation.
    """
    # First, express the point in the central coordinate system.
    pt_1 = pt - center
    # Now, rotate this point.
    pt_1 = np.dot(r, pt_1)
    # Project back to original coordinate system.
    return pt_1 + center


def yzrotation(theta=np.pi*3/20.0):
    """
    Returns a simple planar rotation matrix that rotates
    vectors around the x-axis.
    args:
        theta: The angle by which we will perform the rotation.
    """
    r = np.eye(3)
    r[1, 1] = np.cos(theta)
    r[1, 2] = -np.sin(theta)
    r[2, 1] = np.sin(theta)
    r[2, 2] = np.cos(theta)
    return r


def general_rotation(a, theta):
    """
    Applies to 3-d space.
    Returns a 3x3 rotation matrix given the
    axis to rotate about and the angle to rotate by.
    Rotations are performed about the origin.
    args:
        a: The axis to rotate about
        theta: The angle to rotate by.
    """
    c = np.cos(theta)
    s = np.sin(theta)
    a = a / sum(a ** 2) ** 0.5
    [ax, ay, az] = a[:3]
    return np.array(
        [
            [
                c + ax ** 2 * (1 - c),
                ax * ay * (1 - c) - az * s,
                ax * az * (1 - c) + ay * s,
            ],
            [
                ay * ax * (1 - c) + az * s,
                c + ay ** 2 * (1 - c),
                ay * az * (1 - c) - ax * s,
            ],
            [
                az * ax * (1 - c) - ay * s,
                az * ay * (1 - c) + ax * s,
                c + az ** 2 * (1 - c),
            ],
        ]
    )


def axis_rotation(pt1, pt2, theta):
    """
    Applies to 3-d space.
    Performs a rotation about an axis given by two points
    not necessarily centered at the origin. Unfortunately,
    we need to return a 4x4 matrix here since translations
    can't be expressed as a 3x3 matrix. So, it is the users
    responsibility to add a 1 to any vector they are applying
    this matrix to so that is is 4 dimensional. Also, unlike
    general_rotation, this will only work for vectors post-multiplied
    to the matrix.
    Refer to:
    http://paulbourke.net/geometry/rotate/
    https://en.wikipedia.org/wiki/Translation_(geometry).
    args:
        pt1: The first point of the axis of rotation.
        pt2: The second point of the axis of rotation.
        theta: The angle by which the rotation will occur.
    """
    tr = np.eye(4)
    tr_inv = np.eye(4)
    tr[0, 3] = -pt1[0]
    tr[1, 3] = -pt1[1]
    tr[2, 3] = -pt1[2]
    tr_inv[0, 3] = pt1[0]
    tr_inv[1, 3] = pt1[1]
    tr_inv[2, 3] = pt1[2]
    rot = np.eye(4)
    rot[:3, :3] = general_rotation(pt2 - pt1, theta)
    return np.dot(np.dot(tr_inv, rot), tr)


def rotate_point_about_axis(pt, ax_pt1, ax_pt2, theta):
    """Rotate a point, pt about an axis given by ax_pt1 and ax_pt2."""
    pt_translated = pt - ax_pt1
    r_matrix = general_rotation(ax_pt2 - ax_pt1, theta)
    pt_rotated = np.dot(r_matrix, pt_translated)
    return pt_rotated + ax_pt1


def rotate_points_about_axis(pts, ax_pt1, ax_pt2, theta):
    """Rotate a point, pt about an axis given by ax_pt1 and ax_pt2."""
    pts_translated = pts - ax_pt1
    r_matrix = general_rotation(ax_pt2 - ax_pt1, theta)
    pts_rotated = np.transpose(np.dot(r_matrix, np.transpose(pts_translated)))
    return pts_rotated + ax_pt1


def axisangle(a, theta):
    """
    A wrapper to general_rotation named more appropriately.
    Returns a rotation matrix that rotates about an axis by an angle.
    args:
        a: The axis to rotate about
        theta: The angle to rotate by.
    """
    return general_rotation(a, theta)


def matrix_to_axisangle(m):
    """
    For a rotation matrix in 3 dimensions (rotations about the origin), we need 4 parameters.
    An axis about which we are going to rotate and an angle which is the extent of rotation.
    This method takes the rotation matrix in as input and returns an axis and angle combination that would generate that matrix.
    args:
        m: The rotation matrix (collection of orthonormal vectors in a matrix).
    """
    theta = np.arccos((m[0, 0] + m[1, 1] + m[2, 2] - 1) / 2)
    x = (m[2, 1] - m[1, 2]) / np.sqrt(
        (m[2, 1] - m[1, 2]) ** 2 + (m[0, 2] - m[2, 0]) ** 2 + (m[1, 0] - m[0, 1]) ** 2
    )
    y = (m[0, 2] - m[2, 0]) / np.sqrt(
        (m[2, 1] - m[1, 2]) ** 2 + (m[0, 2] - m[2, 0]) ** 2 + (m[1, 0] - m[0, 1]) ** 2
    )
    z = (m[1, 0] - m[0, 1]) / np.sqrt(
        (m[2, 1] - m[1, 2]) ** 2 + (m[0, 2] - m[2, 0]) ** 2 + (m[1, 0] - m[0, 1]) ** 2
    )
    return (theta, np.array([x, y, z]))


def rotation(n, theta=np.pi/3):
    """
    Returns a general rotation matrix of any dimensionality.
    This is achieved by a sequence of successive 2d rotations.
    http://www.continuummechanics.org/rotationmatrix.html
    args:
        n : The dimensionality of the space in which we are going to rotate things.
        theta: The angle of rotation for each of the planar 2-d rotation matrices.
    """
    r = np.eye(n)
    for i in range(n):
        for j in range(i + 1, n):
            rij = np.eye(n)
            rij[i, i] = np.cos(theta)
            rij[i, j] = -np.sin(theta)
            rij[j, i] = np.sin(theta)
            rij[j, j] = np.cos(theta)
            r = np.dot(r, rij)
    return r


def rotation_transition(
    i=0,
    oldr=general_rotation(np.array([1, 0, 0]), np.pi/2),
    newr=rotation(3, 2 * np.pi * 4/30.0),
):
    """
    A sequence of intermediate rotations that take the system from an initial rotated state (oldr) to a final one (newr).
    args:
        i: 1 means complete rotation to new coordinates, 0 means old rotation.
        oldr: Old rotation matrix.
        newr: New rotation matrix.
    """
    transn = np.dot(newr, np.transpose(oldr))
    (theta, vec) = matrix_to_axisangle(transn)
    r = general_rotation(vec, i * theta)
    return np.dot(r, oldr)


def rotate_vec2vec(oldvec, newvec):
    """
    What rotation matrix is needed to rotate an old vector to a new vector.
    args:
        oldvec: The vector we are starting with.
        newvec: The vector to which we are rotating.
    """
    axis = np.cross(oldvec, newvec)
    oldvec1 = oldvec / np.sqrt(sum(oldvec ** 2))
    newvec1 = newvec / np.sqrt(sum(newvec ** 2))
    theta = np.arccos(sum(oldvec1 * newvec1))
    return axisangle(axis, theta)


def tetrahedral_rotations(p=1.0):
    """
    The (chiral) tetrahedral symmetry group consists of twelve rotations:
    eight (by +/- 1/3 turn) around the main diagonals of a cube,
    three (by 1/2 turn) around the coordinate axes,
    and the identity or null rotation.
    See comment by Anton Sherwood: https://math.stackexchange.com/a/2582519/155881
    """
    from pyray.shapes.solid.cube import Cube

    c = Cube(3)
    vers = c.vertices
    rotations = []
    for body_diag_indices in [[0, 7], [1, 6], [3, 4], [2, 5]]:
        ver1 = vers[body_diag_indices[0]].binary
        ver2 = vers[body_diag_indices[1]].binary
        rotations.append(general_rotation((ver1 - ver2), 2 * np.pi / 3 * p))
        rotations.append(general_rotation((ver1 - ver2), -2 * np.pi / 3 * p))
    rotations.append(general_rotation(np.array([1, 0, 0]), 2 * np.pi / 2 * p))
    rotations.append(general_rotation(np.array([0, 1, 0]), 2 * np.pi / 2 * p))
    rotations.append(general_rotation(np.array([0, 0, 1]), 2 * np.pi / 2 * p))
    return np.array(rotations)


class Quaternion:
    def __init__(self, c, x, y, z):
        self.c = c
        self.x = x
        self.y = y
        self.z = z

    def __mul__(self, other):
        print("not implemented")

    def __rmul__(self, other):
        print("not implemented")


def quaternion_mult(q, r):
    return [
        r[0] * q[0] - r[1] * q[1] - r[2] * q[2] - r[3] * q[3],
        r[0] * q[1] + r[1] * q[0] - r[2] * q[3] + r[3] * q[2],
        r[0] * q[2] + r[1] * q[3] + r[2] * q[0] - r[3] * q[1],
        r[0] * q[3] - r[1] * q[2] + r[2] * q[1] + r[3] * q[0],
    ]


def point_rotation_by_quaternion(point, q):
    r = [0] + point
    q_conj = [q[0], -1 * q[1], -1 * q[2], -1 * q[3]]
    return quaternion_mult(quaternion_mult(q, r), q_conj)[1:]


def rotate_plane(plane, pt1, pt2, theta):
    """
    Rotates a plane (collection of points)
    about an axis defined by
    pt1 and pt2 by an angle theta.
    args:
        pt1: First point defining axis.
        pt2: Second point defining axis.
    """
    plane_tmp = np.copy(plane)
    plane_e = np.append(plane_tmp, np.ones(plane.shape[0])[..., None], 1)
    r = axis_rotation(pt1, pt2, theta)
    plane1 = np.dot(r, plane_e.T).T
    return plane1[:, np.array([0, 1, 2])]


def angle_btw_planes(face1, face2):
    """
    Calculates the angle between two planes.
    To define a plane we need at least three points.
    args:
        face1: The first plane.
        face2: The second plane.
    """
    face1_per = np.cross(face1[0] - face1[1], face1[1] - face1[2])
    face1_per_normd = face1_per / np.sqrt(sum(face1_per ** 2))
    face2_per = np.cross(face2[0] - face2[1], face2[1] - face2[2])
    face2_per_normd = face2_per / np.sqrt(sum(face2_per ** 2))
    return np.arccos(np.dot(face1_per_normd, face2_per_normd))


## A series of methods relating to 1-d rotation.


def rotate_abt_x_line(y_line=-3, y_pt=1, theta=np.pi / 2):
    radius = y_line - y_pt
    y_proj = radius * np.cos(theta)
    y_prime = y_line - y_proj
    return y_prime


def refl_abt_horizntl(y, y_ref=-3):
    delta = y_ref - y
    return y + 2 * delta
