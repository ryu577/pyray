import numpy as np
import queue
from collections import defaultdict
from itertools import combinations
from pyray.rotation import general_rotation, rotate_points_about_axis
from PIL import Image, ImageDraw


class Face():
    def __init__(self, val, color="white"):
        self.val = val
        self.color = color
        self.x = char2coord(val[0])
        self.y = char2coord(val[1])
        self.z = char2coord(val[2])
        self.face_center = np.array([self.x, self.y, self.z])
        vertices = np.array([[1, 1], [1, -1], [-1, 1], [-1, -1]])
        if self.x != 0:
            self.vertices = np.insert(vertices, 0, self.x, axis=1)
        elif self.y != 0:
            self.vertices = np.insert(vertices, 1, self.y, axis=1)
        else:
            self.vertices = np.insert(vertices, 2, self.z, axis=1)
        
        # The flattened coordinates.
        self.x1 = 0
        self.y1 = 0

    def plot(self, draw, r=np.eye(3),
             shift = np.array([256,256,0]),
             scale = 35,
             rgba = (255, 255, 0, 180)):
        rotated_face = np.transpose(np.dot(r, np.transpose(self.vertices)))
        [v1, v2, v3, v4] = shift + scale * rotated_face
        draw.polygon([(v1[0], v1[1]), (v2[0], v2[1]), (v4[0], v4[1]),
                      (v3[0], v3[1])], rgba)
        draw.line((v1[0], v1[1], v2[0], v2[1]), fill=rgba[:3], width=2)
        draw.line((v2[0], v2[1], v4[0], v4[1]), fill=rgba[:3], width=2)
        draw.line((v4[0], v4[1], v3[0], v3[1]), fill=rgba[:3], width=2)
        draw.line((v3[0], v3[1], v1[0], v1[1]), fill=rgba[:3], width=2)

    def rotate_face(self, ax_pt1, ax_pt2, theta):
        self.vertices = rotate_points_about_axis(self.vertices, ax_pt1, ax_pt2, theta)
        self.face_center = self.vertices.mean(axis=0)


def char2coord(ch):
    if ch == '0':
        return 0
    elif ch == '+':
        return 1
    elif ch == '-':
        return -1


class Edge():
    def __init__(face1, face2):
        self.face1 = face1
        self.face2 = face2


class GraphCube():
    def __init__(self, survive_ros={}):
        self.white_verts = set()
        self.grey_verts = set()
        self.black_verts = set()
        self.adj = defaultdict(dict)
        self.vert_props = {}
        self.cov_p = set()
        self.cov_p.add((0,0))
        self.edges = [['-00','0+0'],#2
                      ['-00','0-0'],#1
                      ['-00','00-'],#5
                      ['-00','00+'],#8
                      ['0-0','00+'],
                      ['0-0','00-'],#12
                      ['0-0','+00'],
                      ['0+0','00+'],
                      ['0+0','00-'],#11
                      ['0+0','+00'],
                      ['+00','00+'],#7
                      ['+00','00-']]
        self.time = 0
        for ix in range(len(self.edges)):
            ed = self.edges[ix]
            vert_0 = ed[0]
            vert_1 = ed[1]
            f0 = Face(vert_0)
            f1 = Face(vert_1)
            self.vert_props[vert_0] = f0
            self.vert_props[vert_1] = f1
            if ix in survive_ros:
                self.white_verts.add(vert_0)
                self.white_verts.add(vert_1)
                # Save graph as an adjacency list.
                self.adj[vert_0][vert_1] = Edge(f0, f1)
                self.adj[vert_1][vert_0] = Edge(f1, f0)

    def reset_vert_col(self):
        for v in self.vert_props.keys():
            self.vert_props[v].color = "white"

    def print_vert_props(self):
        for k in self.vert_props.keys():
            print(str(self.vert_props[k].__dict__))

    def dfs_rotate(self, u):
        """This code does not work, we will have to rotate explicitly"""
        self.vert_props[u].color = "grey"
        for v in self.adj[u]:
            if self.vert_props[v].color == "white":
                # Apply rotations of grey vertices.
                self.dfs_rotate(v)
        self.vert_props[u].color = "black"
        self.black_verts.add(u)

    def dfs_plot(self, u):
        """Assumes a draw object attached to graph"""
        self.vert_props[u].color = "grey"
        w = 2
        x, y = map_to_plot(self.vert_props[u].x, self.vert_props[u].y)
        self.draw.ellipse((x-w,y-w,x+w,y+w), fill=(255,0,0), outline = (0,0,0))
        for v in self.adj[u]:
            if self.vert_props[v].color == "white":
                x1, y1 = map_to_plot(self.vert_props[v].x, self.vert_props[v].y)
                self.draw.line((x, y, x1, y1),
                                fill = (255,255,0), width = 1)
                self.dfs_plot(v)


def map_to_plot(x, y):
    scale = 40
    return 256 + x * scale, 256 + y * scale


def tst():
    survive = {3, 10, 11, 8, 5}
    gr = GraphCube(survive)
    gr.dfs('00+')
    im = Image.new("RGB", (512, 512), (0,0,0))
    draw = ImageDraw.Draw(im,'RGBA')
    gr.draw = draw
    gr.reset_vert_col()
    gr.dfs_plot('00+')
    im.save("Images//RotatingCube//im" + str(ix) + ".png")


def tst_all_cuts():
    lst = np.arange(12)
    ix = 0
    for combo in combinations(lst, 5):
        survive = set(combo)
        gr = GraphCube(survive)
        gr.dfs('00+')
        if len(gr.black_verts) == 6:
            if len(survive - {0,1,6,9}) == len(survive):
                im = Image.new("RGB", (512, 512), (0,0,0))
                draw = ImageDraw.Draw(im,'RGBA')
                gr.draw = draw
                gr.reset_vert_col()
                gr.dfs_plot('00+')
                im.save("Images//RotatingCube//im" + str(ix) + ".png")
            ix += 1
    print(ix)


def tst_plot_faces():
    for ix in range(10):
        im = Image.new("RGB", (512, 512), (0,0,0))
        draw = ImageDraw.Draw(im, 'RGBA')
        r = general_rotation(np.array([1,1,1]), np.pi/6)
        for fc in ['00+', '00-', '0+0']:
            f = Face(fc)
            f.plot(draw, r, scale=80, rgba=(12, 90, 190, 90))
        f = Face('0-0')
        f.rotate_face(np.array([-1,-1,-1]), np.array([-1,-1,1]), -np.pi/6*ix/10)
        f.plot(draw, r, scale=80, rgba=(12, 90, 190, 90))
        im.save("Images//RotatingCube//im" + str(ix) + ".png")
