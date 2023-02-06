import numpy as np
import queue
from collections import defaultdict
from itertools import combinations, permutations
from pyray.rotation import general_rotation, rotate_points_about_axis
from pyray.misc import zigzag3
from PIL import Image, ImageDraw
from copy import deepcopy


class Face():
    def __init__(self, val, color="white"):
        self.dim = 3
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
        self.o_verts = self.vertices.copy()
        self.o_face_center = self.face_center.copy()

    def plot(self, draw, r=np.eye(3),
             shift = np.array([256,256,0]),
             scale = 35,
             rgba = (255, 255, 0, 180),
             wdh=2):
        rotated_face = np.transpose(np.dot(r, np.transpose(self.vertices)))
        #rotated_face = np.dot(self.vertices, r)
        self.plot_face(rotated_face, draw, r, shift,
                       scale, rgba, wdh)

    def plot_face(self, rotated_face, draw, r=np.eye(3),
             shift = np.array([256,256,0]),
             scale = 35,
             rgba = (255, 255, 0, 180),
             wdh=2):
        [v1, v2, v3, v4] = scale * rotated_face
        v1[:2] = v1[:2] + shift[:2]
        v2[:2] = v2[:2] + shift[:2]
        v3[:2] = v3[:2] + shift[:2]
        v4[:2] = v4[:2] + shift[:2]
        draw.polygon([(v1[0], v1[1]), (v2[0], v2[1]), (v4[0], v4[1]),
                      (v3[0], v3[1])], rgba)
        draw.line((v1[0], v1[1], v2[0], v2[1]), fill=rgba[:3], width=wdh)
        draw.line((v2[0], v2[1], v4[0], v4[1]), fill=rgba[:3], width=wdh)
        draw.line((v4[0], v4[1], v3[0], v3[1]), fill=rgba[:3], width=wdh)
        draw.line((v3[0], v3[1], v1[0], v1[1]), fill=rgba[:3], width=wdh)

    def plot_perspective(self, draw, r=np.eye(3),
                         shift = np.array([256,256,0]),
                         scale = 35,
                         rgba = (255, 255, 0, 180),
                         wdh=2, e=4, c=-4):
        rotated_face = np.transpose(np.dot(r, np.transpose(self.vertices)))
        for rot in rotated_face:
            az = rot[len(rot)-1]
            for i in range(len(rot)-1):
                rot[i] = e*rot[i]/(az-c)
        self.plot_face(rotated_face, draw, r, shift,
                       scale, rgba, wdh)

    def rotate(self, ax_pt1, ax_pt2, theta):
        self.vertices = rotate_points_about_axis(self.vertices,
                                                 ax_pt1, ax_pt2, theta)
        self.face_center = self.vertices.mean(axis=0)

    def simple_rotate(self, theta, axes):
        """
        args:
            axes: An array (ex: [0,1]). Identifies axes that will be rotating.
                  The other two axes will remain unchanged.
        """
        r = np.eye(self.dim)
        r[np.ix_(axes, axes)] = np.array([[np.cos(theta), -np.sin(theta)],
                                        [np.sin(theta), np.cos(theta)]])
        self.vertices = np.dot(self.vertices, r)
        self.face_center = self.vertices.mean(axis=0)

    def shift_and_simpl_rotate(self, theta, axes,
                               new_orig=np.array([0, 0, 0]),
                               sign=1):
        self.vertices = self.vertices - new_orig
        self.simple_rotate(sign*theta, axes)
        self.vertices = self.vertices + new_orig
        self.face_center = self.vertices.mean(axis=0)

    def reset(self):
        self.vertices = self.o_verts.copy()
        self.face_center = self.vertices.mean(axis=0)


class Edge():
    def __init__(self, face1, face2):
        self.face1 = face1
        self.face2 = face2


def char2coord(ch):
    if ch == '0':
        return 0
    elif ch == '+':
        return 1
    elif ch == '-':
        return -1


class GraphCube():
    def __init__(self, survive_ros={}, angle=np.pi/2):
        self.dim = 3
        self.white_verts = set()
        self.grey_verts = set()
        self.grey_rots = {}
        self.black_verts = set()
        self.adj = defaultdict(dict)
        self.vert_props = {}
        self.cov_p = set()
        self.cov_p.add((0,0))
        self.angle = angle
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
        self.black_verts = set()
        self.grey_verts = set()
        self.grey_rots = {}

    def print_vert_props(self):
        for k in self.vert_props.keys():
            print(str(self.vert_props[k].__dict__))

    def dfs(self, u):
        self.vert_props[u].color = "grey"
        for v in self.adj[u]:
            if self.vert_props[v].color == "white":
                self.dfs(v)
        self.black_verts.add(u)

    def dfs_flatten(self, u):
        self.vert_props[u].color = "grey"
        self.grey_verts.add(u)
        # Apply all the rotations.
        for kk in self.grey_rots.keys():
            if kk not in self.black_verts:
                ax1, ax2 = self.grey_rots[kk]
                self.vert_props[u].rotate_face(ax1, ax2, self.angle)
        for v in self.adj[u]:
            if self.vert_props[v].color == "white":
                # Apply rotations of grey vertices.
                self.grey_rots[v] = get_rot_ax(self.vert_props[u], self.vert_props[v])
                self.dfs_flatten(v)
        self.vert_props[u].color = "black"
        self.black_verts.add(u)

    def dfs_plot(self, u):
        """Assumes a draw object attached to graph"""
        self.vert_props[u].color = "grey"
        w = 2
        shift = (256, 256)
        if self.dim == 3:
            shift = (256, 256, 0)
        elif self.dim == 4:
            shift = (256, 256, 0, 0)
        scale = 40
        if "shift" in self.__dict__:
            shift = self.shift
        if "scale" in self.__dict__:
            scale = self.scale
        x, y = map_to_plot(self.vert_props[u].x, self.vert_props[u].y,
                           scale, shift=shift)
        self.draw.ellipse((x-w, y-w, x+w, y+w),
                          fill=(255, 0, 0),
                          outline=(0, 0, 0))
        for v in self.adj[u]:
            if self.vert_props[v].color == "white":
                x1, y1 = map_to_plot(self.vert_props[v].x, self.vert_props[v].y,
                                     scale, shift=shift)
                self.draw.line((x, y, x1, y1),
                               fill=(255, 255, 0), width=1)
                self.dfs_plot(v)

    def dfs_plot_2(self, u, rgba=(12, 90, 190, 90)):
        """Assumes a draw object and rotation object attached to graph"""
        shift = (256, 256)
        scale = 40
        if "shift" in self.__dict__:
            shift = self.shift
        if "scale" in self.__dict__:
            scale = self.scale
        if "to_plot" in self.__dict__:
            if u in self.to_plot:
                self.vert_props[u].plot(self.draw, self.r,
                                scale=scale,
                                rgba=rgba, shift=shift)
        else:
            self.vert_props[u].plot(self.draw, self.r,
                                scale=scale,
                                rgba=rgba, shift=shift)
        self.vert_props[u].color = "grey"
        for v in self.adj[u]:
            if self.vert_props[v].color == "white":
                self.dfs_plot_2(v, rgba)

    def dfs_plot_perspective(self, u, rgba=(12, 90, 190, 90),\
                             persp=4):
        """Assumes a draw object and rotation object attached to graph"""
        shift = (256, 256)
        scale = 40
        if "shift" in self.__dict__:
            shift = self.shift
        if "scale" in self.__dict__:
            scale = self.scale
        self.vert_props[u].plot_perspective(self.draw, self.r,
                                scale=scale,
                                rgba=rgba, shift=shift,
                                e=persp, c=-persp)
        self.vert_props[u].color = "grey"
        for v in self.adj[u]:
            if self.vert_props[v].color == "white":
                self.dfs_plot_perspective(u=v, persp=persp)


def get_rot_ax(f1, f2):
    x1, y1, z1 = f1.x, f1.y, f1.z
    x2, y2, z2 = f2.x, f2.y, f2.z
    f2_center = np.array([f2.x, f2.y, f2.z])
    x3, y3, z3 = x1+x2, y1+y2, z1+z2
    if x3 == 0:
        p1, p2 = np.array([1,y3,z3]), np.array([-1,y3,z3])
        pt1, pt2 = (f1.vertices[(f1.o_verts==p1).sum(axis=1)==3].flatten(),
                f1.vertices[(f1.o_verts==p2).sum(axis=1)==3].flatten())
    elif y3 == 0:
        p1, p2 = np.array([x3,1,z3]), np.array([x3,-1,z3])
        pt1, pt2 = (f1.vertices[(f1.o_verts==p1).sum(axis=1)==3].flatten(),
                f1.vertices[(f1.o_verts==p2).sum(axis=1)==3].flatten())
    else:
        p1, p2 = np.array([x3,y3,1]), np.array([x3,y3,-1])
        pt1, pt2 = (f1.vertices[(f1.o_verts==p1).sum(axis=1)==3].flatten(),
                f1.vertices[(f1.o_verts==p2).sum(axis=1)==3].flatten())
    norm = np.cross(p2-p1, p2-f2_center)
    dt = np.dot(norm, f2_center)
    if dt > 0:
        return (pt1, pt2)
    else:
        return (pt2, pt1)


def map_to_plot(x, y, scale=40, shift=(256, 256)):
    return shift[0] + x * scale, shift[1] + y * scale

######################################
# test cases and money shots.

def tst():
    ix = 0
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
    r = general_rotation(np.array([1,1,1]), np.pi/6)
    for combo in combinations(lst, 5):
        survive = set(combo)
        gr = GraphCube(survive, -np.pi/2)
        gr.dfs('0+0')
        if len(gr.black_verts) == 6:
            print(combo)
            im = Image.new("RGB", (512, 512), (0,0,0))
            draw = ImageDraw.Draw(im,'RGBA')
            gr.r = r
            gr.reset_vert_col()
            gr.dfs_flatten('0+0')
            gr.draw = draw
            gr.reset_vert_col()
            gr.dfs_plot_2('0+0')
            im.save("Images//RotatingCube//im" + str(ix) + ".png")
            ix += 1
    print(ix)


def main():
    lst = np.arange(12)
    ix = 0
    r = general_rotation(np.array([1,1,1]), np.pi/6)
    prev_surv = {}
    for combo in combinations(lst, 5):
        survive = set(combo)
        gr = GraphCube(survive, -np.pi/2)
        gr.dfs('0+0')
        if len(gr.black_verts) == 6:
            print(combo)
            ix = tst_open_cube(ix, survive, prev_surv)
            prev_surv = deepcopy(survive)


def tst_plot_faces():
    for ix in range(10):
        im = Image.new("RGB", (512, 512), (0,0,0))
        draw = ImageDraw.Draw(im, 'RGBA')
        r = general_rotation(np.array([1,1,1]), np.pi/6)
        for fc in ['00+', '00-', '0+0']:
            f = Face(fc)
            f.plot(draw, r, scale=80, rgba=(12, 90, 190, 90))
        f = Face('0-0')
        f.rotate(np.array([-1,-1,-1]),
                      np.array([-1,-1,1]), -np.pi/6*ix/10)
        f.plot(draw, r, scale=80, rgba=(12, 90, 190, 90))
        im.save("Images//RotatingCube//im" + str(ix) + ".png")


def tst_open_cube(ix=0, surv={0, 1, 2, 3, 6}, prev_surv={}):
    r = general_rotation(np.array([1,1,1]), np.pi/6)
    for i in range(ix, ix+22):
        im = Image.new("RGB", (512, 512), (0,0,0))
        draw = ImageDraw.Draw(im, 'RGBA')
        #gr = GraphCube({3, 10, 11, 8, 5}, -np.pi/2*i/18)
        theta = -np.pi/2*zigzag3(i-ix)/10
        plot_open_cube(draw, r, surv, theta)
        plot_open_cube(draw, r, surv, -np.pi/2, rgba=(125, 125, 12, 80))
        plot_grid(draw, r)
        im.save("Images//RotatingCube//im" + str(i).rjust(4,'0') + ".png")
    return i


def plot_open_cube(draw, r, surv, theta, rgba=(12, 90, 190, 90)):
    gr = GraphCube(surv, theta)
    gr.draw = draw
    gr.r = r
    gr.dfs_flatten('0+0')
    gr.reset_vert_col()
    gr.dfs_plot_2('0+0', rgba=rgba)


def plot_grid(draw, r):
    f = Face('0+0')
    aa = np.array([1,-1,0])
    for x in np.arange(-5,6):
        for z in np.arange(-5,6):
            f.vertices += 2*np.array([x,0,z])
            f.plot(draw, r, scale=40,
                   shift=np.array([256,256,0]),
                   rgba=(180, 132, 12, 10),
                   wdh=1)
            f.vertices -= 2*np.array([x,0,z])


# ffmpeg -framerate 24 -f image2 -i "*?png" -vb 20M vid.avi
# ffmpeg -r 24 -f image2 -pattern_type glob -i "*?png" -vcodec libx264 -crf 20 -pix_fmt yuv420p output.mp4


