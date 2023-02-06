import numpy as np
import networkx as nx
import pyray.shapes.solid.open_cube as oc
from collections import deque
from pyvis.network import Network


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
        self.dim = 4
        self.val = val
        self.rgba = rgba
        self.color = "white"
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
        self.o_face_center = self.face_center.copy()

    def plot(self, draw, r=np.eye(4),
             shift=np.array([256, 256, 0, 0]),
             scale=35,
             rgba=None,
             wdh=2):
        if rgba is None:
            rgba = self.rgba
        super().plot(r=r, rgba=rgba, scale=scale, wdh=wdh, draw=draw,
                     shift=shift)

    def plot_perspective(self, draw, r=np.eye(4),
             shift=np.array([256, 256, 0, 0]),
             scale=35,
             rgba=None,
             wdh=2, e=3, c=7):
        if rgba is None:
            rgba = self.rgba
        super().plot_perspective(r=r, rgba=rgba, scale=scale, wdh=wdh, draw=draw,
                     shift=shift, e=e, c=c)

    def shift_and_simpl_rotate(self, theta, axes,
                               new_orig=np.array([0, 0, 0, 0]),
                               sign=1):
        super().shift_and_simpl_rotate(theta, axes, new_orig, sign)

    def reset(self):
        super().reset()


class TsrctFcGraph(oc.GraphCube):
    def __init__(self, angle=0, adj=None):
        self.dim = 4
        self.face_map = {'--00': 0, '-0-0': 1,
                         '-00-': 2, '-00+': 3, '-0+0': 4, '-+00': 5,
                         '0--0': 6, '0-0-': 7, '0-0+': 8, '0-+0': 9,
                         '0+-0':10, '0+0-':11,'0+0+':12, '0++0':13,
                         '00--':14, '00-+':15, '00+-':16, '00++':17,
                         '+-00':18, '+0-0':19, '+00-':20,
                         '+00+':21, '+0+0':22,'++00':23}
        self.angle = angle
        self.g = nx.Graph()
        #self.constrct()
        if adj is None:
            self.adj = {
                '00-+': {'-0-0', '0-0+', '+00+', '0+0+'},
                '+00+': {'+-00', '00-+', '00++'},
                '00++': {'-00+', '+00+', '0++0'},
                '0++0': {'00++', '00+-'},
                '-00+': {'00++', '--00'},
                '--00': {'-00+', '-00-'},
                '-00-': {'--00'},
                '00+-': {'-0+0', '+0+0'},
                '-0+0': {'00+-'},
                '+-00': {'+00-'},
                '+00-': {'+-00'},
                '+0+0': {'00+-'},
                '0+0+': {'00-+','-+00'},
                '0-0+': {'00-+', '0-+0'},
                '0-+0': {'0-0+', '0-0-'},
                '0-0-': {'0-+0'},
                '-0-0': {'00--', '00-+'},
                '00--': {'-0-0', '0--0'},
                '0--0': {'00--', '+0-0'},
                '+0-0': {'0--0', '0+-0'},
                '0+-0': {'+0-0'},
                '-+00': {'0+0+', '0+0-'},
                '0+0-': {'-+00', '++00'},
                '++00': {'0+0-'}
            }
        else:
            #self.g_min_tree = nx.minimum_spanning_tree(self.g, weight='weight')
            #self.adj = nx.to_dict_of_dicts(self.g_min_tree)
            self.adj = adj
        self.make_adj_symm()
        self.vert_props = {}
        for k in self.face_map.keys():
            self.vert_props[k] = Face1(k)
        self.grey_rots = {}
        self.black_verts = set()
        self.rot_st = deque()
        self.xy_set = set()

    def make_adj_symm(self):
        adj2 = self.adj.copy()
        for k in self.adj.keys():
            for kk in self.adj[k]:
                if k not in self.adj[kk]:
                    print("Fixing " + k + "," + kk)
                adj2[kk].add(k)
        self.adj = adj2

    def constrct(self):
        # Each face is connected to 8 other faces.
        deg_mat = np.eye(24)*8
        face_map = self.face_map
        adj_mat = np.zeros((24, 24))
        self.phy_edges = set()
        i = 0
        for fc in self.face_map.keys():
            edgs = get_edges(fc)
            for ed in edgs:
                if (fc, ed) not in self.g.edges:
                    i += 1
                    #print(fc + " , " + ed)
                    adj_mat[face_map[fc], face_map[ed]] = 1
                    ed_loc = get_physical_edge(fc, ed)
                    if ed_loc in self.phy_edges:
                        self.g.add_edge(fc, ed, weight=np.random.uniform()*100)
                    else:
                        self.g.add_edge(fc, ed, weight=np.random.uniform())
                    self.phy_edges.add(ed_loc)
        print("Total edges: " + str(i))

        lapl = deg_mat - adj_mat
        b = np.delete(lapl, 1, 0)
        b = np.delete(b, 1, 1)
        print("Number of spanning trees of face graph: ")
        print(np.linalg.det(b))

    def print_edge_weights(self):
        i = 0
        for e in self.g.edges.data("weight"):
            if e[2] == 1:
                i += 1
            print(e)
        self.low_wts = i

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
        self.black_verts.add(u)

    def dfs_flatten2(self, u):
        self.vert_props[u].color = "grey"
        # Apply all the rotations.
        for kk in self.grey_rots.keys():
            if self.vert_props[kk].color != "black":
                args = self.grey_rots[kk]
                self.rot_st.append((u, args))
        for v in self.adj[u]:
            if self.vert_props[v].color == "white":
                # Apply rotations of grey vertices.
                self.grey_rots[v] = get_rot(self.vert_props[u],
                                            self.vert_props[v])
                self.dfs_flatten2(v)
        self.vert_props[u].color = "black"
        self.black_verts.add(u)

    def actually_flatten(self):
        while self.rot_st:
            self.reset_vert_col()
            (u, rot) = self.rot_st.pop()
            self.vert_props[u].shift_and_simpl_rotate(self.angle, *rot)

    def dfs_plot(self, u):
        super().dfs_plot_2(u)

    def dfs_plot_perspective(self, u, persp=4):
        super().dfs_plot_perspective(u=u, persp=persp)

    def mk_xy_set(self):
        """
        Should be run after dfs_flatten2 so cube is already
        flattened.
        """
        self.xy_set = set()
        for u in self.face_map:
            x = round(self.vert_props[u].face_center[0])
            y = round(self.vert_props[u].face_center[1])
            self.xy_set.add((x, y))

    def reset_vert_col(self):
        super().reset_vert_col()

    def reset_rotations(self):
        for k in self.face_map.keys():
            self.vert_props[k].reset()
        self.reset_vert_col()


class CubeFcGraph(TsrctFcGraph):
    def __init__(self, angle=0):
        self.angle = angle
        cu = oc.GraphCube()
        ix = 0
        self.face_map = {}
        self.g = nx.Graph()
        for ed in cu.edges:
            if ed[0] not in self.face_map:
                self.face_map[ed[0]] = ix
                ix += 1
            if ed[1] not in self.face_map:
                self.face_map[ed[1]] = ix
                ix += 1
            self.g.add_edge(ed[0], ed[1], weight=np.random.uniform())
        self.g_min_tree = nx.minimum_spanning_tree(self.g)
        self.adj = nx.to_dict_of_dicts(self.g_min_tree)
        self.vert_props = {}
        for k in self.face_map.keys():
            self.vert_props[k] = oc.Face(k)
        self.grey_rots = {}
        self.rot_st = deque()

    def dfs_flatten(self, u):
        self.vert_props[u].color = "grey"
        # Apply all the rotations.
        for kk in self.grey_rots.keys():
            if self.vert_props[kk].color != "black":
                args = self.grey_rots[kk]
                self.rot_st.append((u, args))
        for v in self.adj[u]:
            if self.vert_props[v].color == "white":
                # Apply rotations of grey vertices.
                self.grey_rots[v] = get_rot2(u, v)
                self.dfs_flatten(v)
        self.vert_props[u].color = "black"

    def dfs_flatten2(self, u):
        self.dfs_flatten(u)

    def dfs_plot(self, u):
        super().dfs_plot(u)

    def reset_vert_col(self):
        super().reset_vert_col()


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


def get_physical_edge(f1, f2):
    ff1 = Face1(f1)
    ff2 = Face1(f2)
    xx1 = [ff1.x, ff1.y, ff1.z, ff1.w]
    xx2 = [ff2.x, ff2.y, ff2.z, ff2.w]
    edge = np.zeros(4)
    ed_str = ''
    for i in range(4):
        edge[i] = np.sign(xx1[i]+xx2[i])
        if edge[i] == 1:
            ed_str = ed_str + '+'
        elif edge[i] == -1:
            ed_str = ed_str + '-'
        else:
            ed_str = ed_str + '0'
    return ed_str


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
    r = np.eye(4)
    theta = np.pi/2
    sign = 1
    r[np.ix_(axes, axes)] = np.array([[np.cos(theta), -np.sin(theta)],
                                      [np.sin(theta), np.cos(theta)]])
    dist = sum( (np.dot(f2.o_face_center, r) - f1.o_face_center)**2 )
    if dist > 0.3:
        sign = -1
    return axes, new_orig1, sign


def get_rot2(f1, f2):
    """
    f1 and f2 are face center strings.
    """
    ff1 = oc.Face(f1)
    ff2 = oc.Face(f2)
    xx1 = []
    for f in f1:
        xx1.append(oc.char2coord(f))
    xx2 = []
    for f in f2:
        xx2.append(oc.char2coord(f))
    new_orig = np.zeros(len(xx1))
    axes = []
    for i in range(len(xx1)):
        if xx1[i] ^ xx2[i] != 0:
            axes.append(i)
        new_orig[i] = np.sign(xx1[i]+xx2[i])
    for i in range(len(xx1)):
        summ = 0
        for j in range(len(xx1)):
            if new_orig[j] == ff1.o_verts[i][j]:
                summ += 1
        if summ >= 2:
            new_orig1 = ff1.vertices[i]
            break
    r = np.eye(3)
    theta = np.pi/2
    sign = 1
    r[np.ix_(axes, axes)] = np.array([[np.cos(theta), -np.sin(theta)],
                                        [np.sin(theta), np.cos(theta)]])
    dist = sum( (np.dot(ff2.o_face_center, r) - ff1.o_face_center)**2 )
    if dist > 0.3:
        sign = -1
    return axes, new_orig1, sign


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
