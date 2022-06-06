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


def tst():
    im = Image.new("RGB", (512, 512), (0,0,0))
    draw = ImageDraw.Draw(im, 'RGBA')
    #r = np.eye(4)
    r = rotation(4, np.pi/6)
    f = Face1('00++')
    f.plot(draw, r, scale=40,
                   shift=np.array([256,256,0,0]),
                   rgba=(125, 125, 12, 80),
                   wdh=1)
    im.save("Images//RotatingCube//im" + str(0).rjust(4,'0') + ".png")


def tst2():
    for ix in range(60):
        im = Image.new("RGB", (512, 512), (0,0,0))
        draw = ImageDraw.Draw(im, 'RGBA')
        r = rotation(4, np.pi*ix/60.0)
        for combo in combinations([0,1,2,3], 2):
            (ix1, ix2) = combo
            for p1 in ['+','-']:
                for p2 in ['+','-']:
                    fc_st = '0000'
                    fc = list(fc_st)
                    fc[ix1] = p1
                    fc[ix2] = p2
                    f = Face1(''.join(fc))
                    f.plot(draw, r, scale=40,
                       shift=np.array([256,256,0,0]),
                       rgba=(12, 90, 190, 90),
                       wdh=1)
        im.save("Images//RotatingCube//im" + str(ix).rjust(4,'0') + ".png")

