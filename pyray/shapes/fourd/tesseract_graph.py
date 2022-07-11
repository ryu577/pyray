import numpy as np
import networkx as nx
import pyray.shapes.solid.open_cube as oc
from collections import deque


def cube_trees():
    # First for a cube.. getting the spanning trees.
    a = 5*np.eye(5) - np.ones((5, 5))
    a[0, 3] = 0
    a[3, 0] = 0
    a[1, 4] = 0
    a[4, 1] = 0
    np.linalg.det(a)
    # >> 384


class Face1(oc.Face):
    def __init__(self, val, rgba=(255, 255, 0, 180)):
        self.val = val
        self.rgba = rgba
        self.x = oc.char2coord(val[0])
        self.y = oc.char2coord(val[1])
        self.z = oc.char2coord(val[2])
        self.w = oc.char2coord(val[3])
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
             shift=np.array([256, 256, 0, 0]),
             scale=35,
             rgba=None,
             wdh=2):
        if rgba is None:
            rgba = self.rgba
        super().plot(r=r, rgba=rgba, scale=scale, wdh=wdh, draw=draw,
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

    def shift_and_simpl_rotate(self, theta, axes=[0, 1],
                               new_orig=np.array([0, 0, 0, 0])):
        self.vertices = self.vertices - new_orig
        self.simple_rotate(theta, axes)
        self.vertices = self.vertices + new_orig
        self.face_center = self.vertices.mean(axis=0)

    def reset(self):
        self.vertices = self.o_verts.copy()
        self.face_center = self.vertices.mean(axis=0)


class TsrctFcGraph(oc.GraphCube):
    def __init__(self, angle=0):
        self.face_map = {'--00': 0, '-0-0': 1,
                         '-00-': 2, '-00+': 3, '-0+0': 4, '-+00': 5,
                         '0--0': 6, '0-0-': 7, '0-0+': 8, '0-+0': 9,
                         '0+-0':10, '0+0-':11,'0+0+':12, '0++0':13,
                         '00--':14, '00-+':15, '00+-':16, '00++':17,
                         '+-00':18, '+0-0':19, '+00-':20,
                         '+00+':21, '+0+0':22,'++00':23}
        self.angle = angle
        self.g = nx.Graph()
        self.constrct()
        self.g_min_tree = nx.minimum_spanning_tree(self.g)
        self.adj = nx.to_dict_of_dicts(self.g_min_tree)
        self.vert_props = {}
        for k in self.face_map.keys():
            self.vert_props[k] = Face1(k)
        self.grey_rots = {}

    def constrct(self):
        # Each face is connected to 8 other faces.
        deg_mat = np.eye(24)*8
        face_map = self.face_map
        adj_mat = np.zeros((24, 24))
        for fc in self.face_map.keys():
            edgs = get_edges(fc)
            for ed in edgs:
                adj_mat[face_map[fc], face_map[ed]] = 1
                self.g.add_edge(fc, ed, weight=np.random.uniform())

        lapl = deg_mat - adj_mat
        b = np.delete(lapl, 1, 0)
        b = np.delete(b, 1, 1)
        print("Number of spanning trees of face graph: ")
        print(np.linalg.det(b))

    def dfs_flatten(self, u):
        self.vert_props[u].color = "grey"
        # Apply all the rotations.
        st = deque()
        for kk in self.grey_rots.keys():
            if self.vert_props[kk].color != "black":
                st.append(kk)
        while st:
            kk = st.pop()
            args = self.grey_rots[kk]
            self.vert_props[u].shift_and_simpl_rotate(self.angle, *args)
        for v in self.adj[u]:
            if self.vert_props[v].color == "white":
                # Apply rotations of grey vertices.
                self.grey_rots[v] = get_rot(self.vert_props[u],
                                            self.vert_props[v])
                self.dfs_flatten(v)
        self.vert_props[u].color = "black"

    def dfs_plot(self, u):
        super().dfs_plot_2(u)

    def reset_vert_col(self):
        super().reset_vert_col()

    def reset_rotations(self):
        for k in self.face_map.keys():
            self.vert_props[k].reset()
        self.reset_vert_col()


def get_rot(f1, f2):
    xx1 = [f1.x, f1.y, f1.z, f1.w]
    xx2 = [f2.x, f2.y, f2.z, f2.w]
    axes = []
    new_orig = np.zeros(4)
    for i in range(4):
        if xx1[i] ^ xx2[i] != 0:
            axes.append(i)
        new_orig[i] = np.sign(xx1[i]+xx2[i])
    for i in range(4):
        summ = 0
        for j in range(4):
            if new_orig[j] == f1.o_verts[i][j]:
                summ += 1
        if summ >= 3:
            new_orig1 = f1.vertices[i]
            break
    return axes, new_orig1


def get_edges(fc='00++'):
    zero_ixs = []
    non_zero_ixs = []
    ix = 0
    for ch in fc:
        if ch == '0':
            zero_ixs.append(ix)
        else:
            non_zero_ixs.append(ix)
        ix += 1
    res = []
    for zix in zero_ixs:
        for nix in non_zero_ixs:
            for repl_ch in ['+', '-']:
                ch = '0000'
                ch1 = list(ch)
                ch1[nix] = fc[nix]
                ch1[zix] = repl_ch
                res.append(''.join(ch1))
    return res


#############
## For a 4-d cube and its 3-d graph.

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


def tsrct_cu_grph():
    deg_mat = 7*np.eye(8)
    adj_mat = np.ones((8, 8))
    for ix in range(8):
        adj_mat[ix, ix] = 0
        adj_mat[ix, 7-ix] = 0
    lapl = deg_mat - adj_mat

    b = np.delete(lapl, 1, 0)
    b = np.delete(b, 1, 1)

    np.linalg.det(b)
    # > 416745 spanning trees.
    # > 261 distinct meshes.
