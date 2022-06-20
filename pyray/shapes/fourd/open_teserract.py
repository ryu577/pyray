import numpy as np
import queue
from collections import defaultdict
from itertools import combinations
from pyray.shapes.solid.open_cube import char2coord, Face
from pyray.rotation import general_rotation, rotate_points_about_axis,\
    rotation
from pyray.misc import zigzag3
from PIL import Image, ImageDraw


class Cube():
    """
    Each of the faces of a Teserract is a cube.
    """
    def __init__(self, val):
        self.x = char2coord(val[0])
        self.y = char2coord(val[1])
        self.z = char2coord(val[2])
        self.w = char2coord(val[3])
        self.cube_center = np.array([self.x, self.y,
                                     self.z, self.w])


class Face1(Face):
    def __init__(self, val, color="white"):
        self.val = val
        self.color = color
        self.x = char2coord(val[0])
        self.y = char2coord(val[1])
        self.z = char2coord(val[2])
        self.w = char2coord(val[3])
        self.face_center = np.array([self.x, self.y, self.z, self.w])
        self.vertices = np.array([[1, 1], [1, -1], [-1, 1], [-1, -1]])
        if self.x != 0:
            self.vertices = np.insert(self.vertices, 0, self.x, axis=1)
        if self.y != 0:
            self.vertices = np.insert(self.vertices, 1, self.y, axis=1)
        if self.z != 0:
            self.vertices = np.insert(self.vertices, 2, self.z, axis=1)
        if self.w != 0:
            self.vertices = np.insert(self.vertices, 3, self.w, axis=1)
        self.o_verts = self.vertices.copy()

    def plot(self, draw, r=np.eye(4),
             shift=np.array([256,256,0,0]),
             scale=35,
             rgba=(255, 255, 0, 180),
             wdh=2):
        super().plot(r=r,rgba=rgba,scale=scale,wdh=wdh,draw=draw,
                     shift=shift)

    def simple_rotate(self, theta, axes=[0, 1]):
        """
        args:
            axes: An array (ex: [0,1]). Identifies axes that will be rotating.
                  The other two axes will remain unchanged.
        """
        r = np.eye(4)
        r[np.ix_(axes, axes)] = np.array([[np.cos(theta), -np.sin(theta)],
                                          [np.sin(theta), np.cos(theta)]])
        self.vertices = np.dot(self.vertices, r)
        self.face_center = self.vertices.mean(axis=0)

    def shift_and_simpl_rotate(self, theta, axes=[0, 1], new_orig=np.array([0, 0, 0, 0])):
        self.vertices -= new_orig
        self.simple_rotate(theta, axes)
        self.vertices += new_orig
        self.face_center = self.vertices.mean(axis=0)


def tst():
    im = Image.new("RGB", (512, 512), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    r = rotation(4, np.pi/6)
    f = Face1('00++')
    f.plot(draw, r, scale=40,
           shift=np.array([256, 256, 0, 0]),
           rgba=(125, 125, 12, 80),
           wdh=1)
    im.save("Images//RotatingCube//im" + str(0).rjust(4, '0') + ".png")


def tst2():
    for ix in range(60):
        im = Image.new("RGB", (512, 512), (0, 0, 0))
        draw = ImageDraw.Draw(im, 'RGBA')
        r = rotation(4, np.pi*ix/60.0)
        for combo in combinations([0, 1, 2, 3], 2):
            (ix1, ix2) = combo
            for p1 in ['+', '-']:
                for p2 in ['+', '-']:
                    fc_st = '0000'
                    fc = list(fc_st)
                    fc[ix1] = p1
                    fc[ix2] = p2
                    f = Face1(''.join(fc))
                    f.plot(draw, r, scale=40,
                           shift=np.array([256, 256, 0, 0]),
                           rgba=(12, 90, 190, 90),
                           wdh=1)
        im.save("Images//RotatingCube//im" + str(ix).rjust(4, '0') + ".png")


def tst3():
    ix = 18
    for ii in np.arange(10):
        im = Image.new("RGB", (512, 512), (0, 0, 0))
        draw = ImageDraw.Draw(im, 'RGBA')
        r = rotation(4, np.pi*ix/60.0)
        theta = np.pi/2*ii/10.0
        # Generate all faces.
        for combo in combinations([0, 1, 2, 3], 2):
            (ix1, ix2) = combo
            for p1 in ['+', '-']:
                for p2 in ['+', '-']:
                    fc_st = '0000'
                    fc = list(fc_st)
                    fc[ix1] = p1
                    fc[ix2] = p2
                    f = Face1(''.join(fc))
                    f.plot(draw, r, scale=40,
                           shift=np.array([256, 256, 0, 0]),
                           rgba=(12, 90, 190, 90),
                           wdh=1)
        f = Face1('0+0+')
        f.simple_rotate(theta, [0, 3])
        f.plot(draw, r, scale=40,
               shift=np.array([256, 256, 0, 0]),
               rgba=(120, 90, 120, 90),
               wdh=1)
        im.save("Images//RotatingCube//im" + str(ii).rjust(4, '0') + ".png")


def tst4():
    ix = 18
    for ii in np.arange(11):
        im = Image.new("RGB", (512, 512), (0, 0, 0))
        draw = ImageDraw.Draw(im, 'RGBA')
        r = rotation(4, np.pi*ix/60.0)
        theta = -np.pi/2*ii/10.0
        # Generate all faces.
        for combo in combinations([0, 1, 2, 3], 2):
            (ix1, ix2) = combo
            for p1 in ['+', '-']:
                for p2 in ['+', '-']:
                    fc_st = '0000'
                    fc = list(fc_st)
                    fc[ix1] = p1
                    fc[ix2] = p2
                    f = Face1(''.join(fc))
                    if f.val[1] == '+':
                        f.shift_and_simpl_rotate(theta, [1, 3], np.array([0,1,0,1]))
                    elif f.val[1] == '-':
                        f.shift_and_simpl_rotate(-theta, [1, 3], np.array([0,-1,0,1]))
                    elif f.val[2] == '+':
                        f.shift_and_simpl_rotate(theta, [2, 3], np.array([0,0,1,1]))
                    elif f.val[2] == '-':
                        f.shift_and_simpl_rotate(-theta, [2, 3], np.array([0,0,-1,1]))
                    elif f.val[0] == '+':
                        f.shift_and_simpl_rotate(theta, [0, 3], np.array([1,0,0,1]))
                    elif f.val[0] == '-':
                        f.shift_and_simpl_rotate(-theta, [0, 3], np.array([-1,0,0,1]))
                    f.plot(draw, r, scale=40,
                           shift=np.array([256, 256, 0, 0]),
                           rgba=(12, 90, 190, 90),
                           wdh=1)
                    if f.val[3] == '+':
                        f.plot(draw, r, scale=40,
                           shift=np.array([256, 256, 0, 0]),
                           rgba=(180, 190, 70, 50),
                           wdh=1)
        im.save("Images//RotatingCube//im" + str(ii).rjust(4, '0') + ".png")

