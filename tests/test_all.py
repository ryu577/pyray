import numpy as np
from pyray.rotation import rotation
from pyray.shapes.cube import Vertice
from pyray.color import heat_rgb
from pyray.misc import move_to_closest

def test_rotation_360():
    """
    Rotating by 360 degrees should preserve the vector.
    """
    rot_matrix = rotation(3, np.pi * 2)
    vec = np.random.uniform(size=3)
    vec_rot = np.dot(rot_matrix, vec)
    assert sum(abs(vec - vec_rot) / vec) < 1e-5

def test_binary_vec():
    """
    Check that the conversion of cube vertice to binary form works.
    """
    vertex = Vertice(i=3, n=4)
    binary = vertex.to_binary()
    binary_str = bin(3)[::-1]
    for i in [0, 1]:
        assert int(binary_str[i]) == int(binary[i])

def test_heat_map():
    """
    Tests that the heat map when set at its maximum value, returns red.
    """
    assert heat_rgb(0, 1, 1)[0] == 255

def test_move_to_closest():
    """
    Test moving a number to the closest one in an array.
    """
    assert move_to_closest(1.1, np.array([0, 1, 2]), 0.9) == 1.01

def test_tetartoid_dual_faces():
    """
    Test that the triangular faces of the
    dual solid of a Tetartoid has isocoles triangles.
    which is a very surprising fact given that
    the tetartoid itself is regular.
    """
    tr = Tetartoid(s=0.45,t=0.14)
    has_isocoles = False
    for j in range(20):
        dual_face = [np.mean(tr.planes[i],axis=0) for i in tr.dual_face_indices[j]]
        lengths = [np.sqrt(sum((dual_face[i]-dual_face[(i+1)%3])**2)) for i in range(3)]
        if abs(lengths[0]-lengths[1]) > 1e-6 and abs(lengths[1]-lengths[2]) > 1e-6:
            has_isocoles = True
    assert has_isocoles


