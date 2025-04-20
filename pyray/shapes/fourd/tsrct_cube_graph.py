import numpy as np
from pyray.shapes.fourd.tesseract_graph import TsrctFcGraph
import pyray.shapes.solid.open_cube as oc
from pyray.rotation2.rotn_4d import rotate_points_about_plane
from copy import deepcopy
from PIL import Image, ImageDraw
from pyray.rotation import rotation, axis_rotation
from pyray.rotation2.rotn_4d import rotate_points_about_plane_helper
from pyray.shapes.fourd.tesseract_graph import Face1
import queue


class TsrctCube(TsrctFcGraph):
    def __init__(self, key='000+', rot_sign=1) -> None:
        super().__init__()
        self.color = "white"
        self.key = key
        self.faces = {}
        self.rot_sign = rot_sign
        for i in range(len(key)):
            ch = key[i]
            if ch == '0':
                for ch1 in ['+', '-']:
                    str1 = ''
                    for j in range(len(key)):
                        if j != i:
                            str1 = str1 + key[j]
                        else:
                            str1 = str1 + ch1
                    self.faces[str1] = deepcopy(self.vert_props[str1])

        self.cube_center = []
        for ch in self.key:
            if ch == '0':
                self.cube_center.append(0)
            elif ch == '+':
                self.cube_center.append(1)
            else:
                self.cube_center.append(-1)
        self.cube_center = np.array(self.cube_center)
        self.o_cube_center = deepcopy(self.cube_center)

    def get_common_face(self, other_key='000+'):
        return get_common_face(self.key, other_key)
    
    def plot_perspective(self, draw, r, persp=5, rgba=(123, 22, 10, 40),
                         shift=np.array([256, 256, 0, 0]),
                         scale=35):
        for f in self.faces.keys():
            self.faces[f].plot_perspective(draw, r, e=persp, c=-persp, 
                                           rgba=rgba, shift=shift, scale=scale)

    def rotate(self, ax1, ax2, ax3, theta, ref_pt=None, take_further=True):
        for ff in self.faces.keys():
            self.faces[ff].rotate_about_plane(ax1, ax2, ax3, theta)
            # if self.rot_sign != 0:
            #     self.faces[ff].rotate_about_plane(ax1, ax2, ax3, theta*self.rot_sign)
            # elif ss != 0:
            #     self.faces[ff].rotate_about_plane(ax1, ax2, ax3, theta*ss)
            # else:
            #     self.faces[ff].rotate_about_plane(ax1, ax2, ax3, theta,
            #                                       ref_pt, 
            #                                       take_farther=take_further)

    def reset(self):
        for fc in self.faces.keys():
            self.faces[fc].reset()


class TsrctCubeTree(TsrctFcGraph):
    def __init__(self, free_rot=False, take_further=True) -> None:
        super().__init__()
        self.max_depth = 0
        self.face_map = self.vert_props
        self.cubes = {'000+':0, '000-':1,
                      '00+0':2, '00-0':3,
                      '0+00':4, '0-00':5,
                      '+000':6, '-000':7}
        self.cube_map = {}
        for k in self.cubes.keys():
            self.cube_map[k] = TsrctCube(k)
        # Legacy methods still use vert_props.
        self.vert_props = self.cube_map
        self.adj = {
            '000-': ['00-0','+000','0-00','-000','0+00','00+0'],
            '00-0': ['000+']
        }
        self.black_verts = set()
        self.grey_verts = set()
        self.cube_arr = []
        self.rot_arr = []
        self.theta = np.pi/20.0
        self.free_rot = free_rot
        self.take_further = take_further

    def plot(self, draw, r, persp=5, rgba=(123, 22, 10, 40),
             shift=np.array([256, 256, 0, 0]),
             scale=35):
        for c1 in self.cube_map.keys():
            self.cube_map[c1].plot_perspective(draw, r, persp
                                               , rgba=rgba,
                                               shift=shift,
                                               scale=scale)

    def dfs_flatten(self, u):
        self.cube_map[u].color = "grey"
        self.grey_verts.add(u)
        u_cube = self.cube_map[u]
        for i in range(len(self.cube_arr)):
            cc = self.cube_arr[i]
            cu = self.cube_map[cc]
            pi_name = self.cube_map[cu.key].pi
            pi = self.cube_map[pi_name]
            if cc not in self.black_verts and cc in self.grey_verts:
                rot1 = self.rot_arr[i]
                if self.free_rot:
                    rot1.do_rotate(u_cube, theta=self.theta)
                else:
                    rot1.do_rotate(u_cube, theta=self.theta,
                               ref_pt=pi.cube_center,
                               take_further=self.take_further)

        if u in self.adj:
            for v in self.adj[u]:
                if self.cube_map[v].color == "white":
                    # Apply rotations of grey vertices.
                    self.cube_arr.append(v)
                    c0 = self.cube_map[u]
                    c1 = self.cube_map[v]
                    sign = self.cube_map[v].rot_sign
                    rot1 = Rotation(c0, c1, sign)
                    self.rot_arr.append(rot1)
                    self.dfs_flatten(v)
        self.cube_map[u].color = "black"
        self.black_verts.add(u)

    def bfs(self, s):
        #self.grey_verts.add(s)
        self.cube_map[s].color = "grey"
        self.cube_map[s].d = 0
        q = queue.Queue()
        q.put(s)
        while q.qsize() > 0:
            u = q.get()
            if u in self.adj:
                for v in self.adj[u]:
                    if self.cube_map[v].color == "white":
                        self.cube_map[v].color = "grey"
                        self.cube_map[v].d = self.cube_map[u].d + 1
                        if self.max_depth < self.cube_map[v].d:
                            self.max_depth = self.cube_map[v].d
                        self.cube_map[v].pi = u
                        self.cube_map[v].rot_sign = get_rot_sign(u, v)
                        q.put(v)
            self.cube_map[u].color = "black"
            self.black_verts.add(u)

    def reset(self):
        for cu in self.cube_map.keys():
            self.cube_map[cu].reset()


def get_rot_sign(u, v):
    fc1 = get_common_face(u, v)
    face1 = Face1(fc1)
    cu = TsrctCube(u)
    cv = TsrctCube(v)
    pt1 = deepcopy(cv.cube_center)
    pts2 = rotate_points_about_plane_helper(np.array([pt1]), 
                                            face1.vertices[0], 
                                            face1.vertices[1], 
                                            face1.vertices[2],
                                            np.random.normal(size=4),
                                            np.pi/2)
    if sum((pts2[0] - cu.cube_center)**2) < 1:
        return -1
    return 1


class Rotation():
    def __init__(self, c0, c1, sign=1):
        self.c0 = c0
        self.c1 = c1
        self.sign = sign
        f1 = get_common_face(c0.key, c1.key)
        fc1 = c0.faces[f1]
        self.ax1, self.ax2, self.ax3 = \
            fc1.vertices[0], fc1.vertices[1],\
            fc1.vertices[2]
        #self.ref_pt = c0.cube_center
        self.ref_pt = np.array([0,0,0,0])

    def do_rotate(self, c1, theta=np.pi*3/200.0, ref_pt=None, 
                  take_further=True):
        # c1.rotate(self.ax1, self.ax2, self.ax3, \
        #           theta, ref_pt=ref_pt, take_further=take_further)
        c1.rotate(self.ax1, self.ax2, self.ax3, \
                   theta*self.sign)


class MshObj():
    def __init__(self, tt, r, scale, shift, persp):
        self.tt = tt
        self.r = r
        self.scale = scale
        self.shift = shift
        self.persp = persp
    
    def plot(self, draw, rgba=(100,100,100,40)):
        self.tt.plot(draw, self.r, rgba=rgba,
            shift=self.shift,
            scale=self.scale,
            persp=self.persp)


def get_common_face(f1='000+', f2='00-0'):
    res = []
    for i in range(len(f1)):
        if f1[i] != '0':
            res.append(f1[i])
        elif f2[i] != '0':
            res.append(f2[i])
        else:
            res.append('0')
    return ''.join(res)


def primitive_tsrct_open(persp=0, i=0, r=rotation(4, np.pi*17/60.0), theta=np.pi/20.0):
    """
    Primitive way to open a cube.
    """
    im = Image.new("RGB", (512, 512), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    tf = TsrctCubeTree()
    c0 = tf.cube_map['000-']
    c1 = tf.cube_map['-000']
    c2 = tf.cube_map['+000']
    c3 = tf.cube_map['0+00']
    c4 = tf.cube_map['0-00']
    c5 = tf.cube_map['00+0']
    c6 = tf.cube_map['00-0']
    c7 = tf.cube_map['000+']
    #
    f1 = get_common_face(c0.key, c1.key)
    fc1 = c0.faces[f1]
    ax1, ax2, ax3 = fc1.vertices[0], fc1.vertices[1], fc1.vertices[2]
    c1.rotate(ax1, ax2, ax3, np.pi*i/200.0, ref_pt=c0.cube_center)
    #
    f1 = get_common_face(c0.key, c2.key)
    fc1 = c0.faces[f1]
    ax1, ax2, ax3 = fc1.vertices[0], fc1.vertices[1], fc1.vertices[2]
    c2.rotate(ax1, ax2, ax3, np.pi*i/200.0, ref_pt=c0.cube_center)
    #
    f1 = get_common_face(c0.key, c3.key)
    fc1 = c0.faces[f1]
    ax1, ax2, ax3 = fc1.vertices[0], fc1.vertices[1], fc1.vertices[2]
    c3.rotate(ax1, ax2, ax3, np.pi*i/200.0, ref_pt=c0.cube_center)
    #
    f1 = get_common_face(c0.key, c4.key)
    fc1 = c0.faces[f1]
    ax1, ax2, ax3 = fc1.vertices[0], fc1.vertices[1], fc1.vertices[2]
    c4.rotate(ax1, ax2, ax3, np.pi*i/200.0, ref_pt=c0.cube_center)
    #
    f1 = get_common_face(c0.key, c5.key)
    fc1 = c0.faces[f1]
    ax1, ax2, ax3 = fc1.vertices[0], fc1.vertices[1], fc1.vertices[2]
    c5.rotate(ax1, ax2, ax3, np.pi*i/200.0, ref_pt=c0.cube_center)
    #
    f1 = get_common_face(c0.key, c6.key)
    fc1 = c0.faces[f1]
    ax1, ax2, ax3 = fc1.vertices[0], fc1.vertices[1], fc1.vertices[2]
    c6.rotate(ax1, ax2, ax3, np.pi*i/200.0, ref_pt=c0.cube_center)
    c7.rotate(ax1, ax2, ax3, np.pi*i/200.0, ref_pt=c0.cube_center)
    #
    f1 = get_common_face(c6.key, c7.key)
    fc1 = c6.faces[f1]
    ax1, ax2, ax3 = fc1.vertices[0], fc1.vertices[1], fc1.vertices[2]
    c7.rotate(ax1, ax2, ax3, np.pi*i/200.0, ref_pt=c6.cube_center)

    tf.plot(draw, r, persp=persp, rgba=(120, 23, 110, 30))
    im.save("Images//RotatingCube//im" +
                        str(i).rjust(4, '0') +
                        ".png")


def open_tsrct_proper(adj=None):
    for i in range(11):
        tt = TsrctCubeTree()
        if adj is not None:
            tt.adj = adj
        tt.bfs('000-')
        tt.reset_vert_col()
        tt.theta = np.pi/20.0*i
        tt.dfs_flatten('000-')
        im = Image.new("RGB", (512, 512), (255, 255, 255))
        draw = ImageDraw.Draw(im, 'RGBA')
        r = rotation(4, np.pi*17/60.0)
        tt.plot(draw, r, rgba=(100, 100, 100, 40))
        im.save("Images//RotatingCube//im" +
                str(i).rjust(4, '0') +
                ".png")


def tst():
    for i in range(31):
        tt = TsrctCubeTree()
        tt.adj = {
                    '000-':['-000','+000','00-0','00+0'],
                    '00-0':['0+00','000+'],
                    '00+0':['0-00']
                }
        tt.bfs('000-')
        tt.reset_vert_col()
        tt.theta = min(np.pi/20.0*i, np.pi/2)
        tt.dfs_flatten('000-')
        im = Image.new("RGB", (512, 512), (255, 255, 255))
        draw = ImageDraw.Draw(im, 'RGBA')
        r=np.eye(4)
        r2_3d = axis_rotation(np.array([0,0,0]), np.array([1,1,1]),
                              np.pi/4+2*np.pi/20.0*i)[:3,:3]
        r[:3,:3] = r2_3d
        tt.plot(draw, r, rgba=(100,100,100,40))
        tt.cube_map['0-00'].plot_perspective(draw, r, 5,
                                             rgba=(255, 0, 0, 50),
                                             shift=np.array([256, 256, 0, 0]),
                                             scale=35)
        tt.cube_map['0+00'].plot_perspective(draw, r, 5,
                                             rgba=(0, 255, 0, 50),
                                             shift=np.array([256, 256, 0, 0]),
                                             scale=35)
        tt.cube_map['-000'].plot_perspective(draw, r, 5,
                                             rgba=(255, 255, 0, 50),
                                             shift=np.array([256, 256, 0, 0]),
                                             scale=35)
        tt.cube_map['+000'].plot_perspective(draw, r, 5,
                                             rgba=(255, 255, 0, 50),
                                             shift=np.array([256, 256, 0, 0]),
                                             scale=35)
        im.save("Images//RotatingCube//im" +
                str(i).rjust(4, '0') +
                ".png")
