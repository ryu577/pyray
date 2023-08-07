import numpy as np
from pyray.shapes.fourd.tesseract_graph import TsrctFcGraph, Face1
import pyray.shapes.fourd.tsrct_face_rotation as tfr
from pyray.rotation import rotation
from pyray.rotation2.rotn_4d import rotate_points_about_plane_helper
from PIL import Image, ImageDraw
import queue


def open_given_cube(tf, base_fc='+00+', i=0):
    """
    tf: Instance of TesseractFaceGraph.
    """
    tf.reset_vert_col()
    tf.dfs_flatten2(base_fc)
    tf.reset_vert_col()
    while tf.rot_st:
        tf.reset_vert_col()
        (u, rot) = tf.rot_st.pop()
        tf.vert_props[u].shift_and_simpl_rotate(tf.angle, *rot)
        print("Rotated face: " + str(i))
    tf.mk_xy_set()
    print(len(tf.xy_set))


class TsrctFcGraph3(TsrctFcGraph):
    def __init__(self, angle, adj=None):
        super().__init__(angle, adj)
        self.theta = angle
        self.face_arr = []
        self.rot_array = []
        self.max_depth = 0
        self.face_map = self.vert_props
        self.black_verts = set()
        self.grey_verts = set()

    def bfs(self, s):
        self.face_map[s].color = "grey"
        self.face_map[s].d = 0
        q = queue.Queue()
        q.put(s)
        while q.qsize() > 0:
            u = q.get()
            if u in self.adj:
                for v in self.adj[u]:
                    if self.face_map[v].color == "white":
                        self.face_map[v].color = "grey"
                        self.face_map[v].d = self.face_map[v].d + 1
                        if self.max_depth < self.face_map[v].d:
                            self.max_depth = self.face_map[v].d
                        self.face_map[v].pi = u
                        self.face_map[v].rot_sign = get_rot_sign(u, v)
                        q.put(v)
            self.face_map[u].color = "black"
            self.black_verts.add(u)

    def dfs1(self, u):
        self.face_map[u].color = "grey"
        self.grey_verts.add(u)
        u_face = self.face_map[u]
        for i in range(len(self.face_arr)):
            fc = self.face_arr[i]
            fu = self.face_map[fc]
            pi_name = self.face_map[fu.key].pi
            pi = self.face_map[pi_name]
            if fc not in self.black_verts and fc in self.grey_verts:
                rot1 = self.rot_array[i]
                rot1.do_rotate(u_face, theta=self.theta)
        if u in self.adj:
            for v in self.adj[u]:
                if self.face_map[v].color == "white":
                    self.face_arr.append(v)
                    f0 = self.face_map[u]
                    f1 = self.face_map[v]
                    sign = self.face_map[v].rot_sign
                    rot1 = Rotation1(f0, f1, sign)
                    self.rot_array.append(rot1)
                    self.dfs1(v)
        self.face_map[u].color = "black"
        self.black_verts.add(u)

    def plot(self, draw, r, persp=0, rgba=(10,31,190,80),
                       shift=np.array([514, 595, 0, 0]),scale=105):
        for kk in self.face_map.keys():
            ff = self.vert_props[kk]
            if persp == 0:
                ff.plot(draw, r, rgba=rgba,shift=shift,scale=scale)
            else:
                ff.plot_perspective(draw, r,
                                    rgba=rgba,
                                    e=persp,
                                    c=-persp,shift=shift,scale=scale)

    def reset(self):
        for u in self.face_map.keys():
            #self.face_map[u].reset()
            self.face_map[u].color = "white"
        self.black_verts = set()
        self.grey_verts = set()

    def dfs(self, u):
        self.vert_props[u].color = "grey"
        for v in self.adj[u]:
            if self.vert_props[v].color == "white":
                self.do_rotn(v)
                self.dfs(v)
        self.vert_props[u].color = "black"

    def do_rotn(self, v):
        pi_face = self.face_map[self.face_map[v].pi]
        if self.face_map[v].d >= self.curr_d:
            # First get the rotation.
            pt1, pt2, pt3 = tfr.get_rotation_plane(pi_face,
                                                   self.face_map[v])
            self.rotn = pt1, pt2, pt3
            # Now rotate that face
            self.face_map[v].rotate(pt1, pt2, pt3,
                                      self.theta*self.face_map[v].rot_sign)


def get_rot_sign(u, v):
    fu = Face1(u)
    fv = Face1(v)
    pt1, pt2, pt3 = tfr.get_rotation_plane(fu, fv)
    pts2 = rotate_points_about_plane_helper(np.array([pt1]), 
                                            pt1, pt2, pt3,
                                            np.random.normal(size=4),
                                            np.pi/2)
    if sum((pts2[0] - fu.face_center)**2) < 1:
        return -1
    return 1

class Rotation1():
    def __init__(self, f0, f1, sign=1):
        self.f0 = f0
        self.f1 = f1
        self.ax1, self.ax2, self.ax3 = tfr.get_rotation_plane(f0, f1)
        self.sign = sign
    
    def do_rotate(self, fc, theta):
        fc.rotate(self.ax1, self.ax2, self.ax3, theta*self.sign)


class TsrctFcGraph2(TsrctFcGraph):
    """
    This class is being created to open the Tesseract
    smoothly.
    """
    def __init__(self, angle=0, adj=None, base_face='00++'):
        super().__init__(angle, adj)
        self.theta = angle
        self.grey_verts = set()
        self.base_face = Face1(base_face)
        self.random_face = Face1('+00+')
        self.rot_array = []
        self.rot_dict = {}
        self.curr_rotn_layer = 1
        self.max_depth = 0
        self.ref_pt = self.base_face.face_center
        for u in self.vert_props.keys():
            self.vert_props[u].pi = None
        self.rotn = None
        self.curr_d = 0

    def dfs(self, u):
        self.vert_props[u].color = "grey"
        for v in self.adj[u]:
            if self.vert_props[v].color == "white":
                self.do_rotn(v)
                self.dfs(v)
        self.vert_props[u].color = "black"

    def do_rotn(self, v):
        pi_face = self.vert_props[self.vert_props[v].pi]
        if self.vert_props[v].d == self.curr_d:
            # First get the rotation.
            pt1, pt2, pt3 = tfr.get_rotation_plane(pi_face,
                                                   self.vert_props[v])
            self.rotn = pt1, pt2, pt3
            # Now rotate that face
            self.vert_props[v].rotate_about_plane(pt1, pt2, pt3, 
                                                  self.theta,
                                                  ref_pt=pi_face.face_center,
                                                  take_farther=True)
        elif self.vert_props[v].d > self.curr_d:
            if self.rotn is not None:
                pt1, pt2, pt3 = self.rotn
                self.vert_props[v].rotate_about_plane2(pt1, pt2, pt3, 
                                                  self.theta,
                                                  ref_face=pi_face)

    def bfs(self, s):
        self.grey_verts.add(s)
        self.vert_props[s].color = "grey"
        self.vert_props[s].d = 0
        q = queue.Queue()
        q.put(s)
        while q.qsize() > 0:
            u = q.get()
            for v in self.adj[u]:
                if self.vert_props[v].color == "white":
                    self.grey_verts.add(v)
                    self.vert_props[v].color = "grey"
                    self.vert_props[v].d = self.vert_props[u].d + 1
                    if self.max_depth < self.vert_props[v].d:
                        self.max_depth = self.vert_props[v].d
                    self.vert_props[v].pi = u
                    q.put(v)
            self.vert_props[u].color = "black"
            self.black_verts.add(u)

    def plot_all_faces(self, draw, r, persp=0, rgba=(10,31,190,80),
                       shift=np.array([514, 595, 0, 0]),scale=105):
        for kk in self.face_map.keys():
            ff = self.vert_props[kk]
            if persp == 0:
                ff.plot(draw, r, rgba=rgba,shift=shift,scale=scale)
            else:
                ff.plot_perspective(draw, r,
                                    rgba=rgba,
                                    e=persp,
                                    c=-persp,shift=shift,scale=scale)

    def tst_dfs_rotate(self, u):
        self.vert_props[u].color = "grey"
        self.grey_verts.add(u)
        ax1, ax2, ax3 = tfr.get_rotation_plane(self.base_face, 
                                               self.random_face)
        for v in self.adj[u]:
            if self.vert_props[v].color == "white":
                # Apply rotations of grey vertices.
                self.vert_props[u].rotate_about_plane(ax1, ax2,
                                                      ax3,
                                                      self.angle)
                self.tst_dfs_rotate(v)
        self.vert_props[u].color = "black"
        self.black_verts.add(u)

    def reset(self):
        for u in self.vert_props.keys():
            self.vert_props[u].reset()

    def dfs1(self, u):
        """
        Assumes BFS has already run.
        Then vertex colors should be reset.
        TODO: This approach doesn't currently work.
        """
        self.vert_props[u].color = "grey"
        if self.vert_props[u].pi is not None:
            self.rot_array.append(u)
            face = self.vert_props[u]
            pi_face = self.vert_props[self.vert_props[u].pi]
            pt1, pt2, pt3 = tfr.get_rotation_plane(pi_face,
                                                   self.vert_props[u])
            self.rot_dict[u] = pt1, pt2, pt3
            face.rotate_about_plane(pt1, pt2, pt3, self.theta,
                                    ref_pt=pi_face.face_center,
                                    take_farther=True)
        for v in self.adj[u]:
            if self.vert_props[v].color == "white":
                face1 = self.vert_props[v]
                face_pi = self.vert_props[self.vert_props[v].pi]
                for vx in self.rot_array:
                    # All the parents who are still grey.
                    if self.vert_props[vx].color == "grey":
                        ### TODO: Verify and fix this.
                        pt1, pt2, pt3 = self.rot_dict[vx]
                        face1.rotate_about_plane2(pt1, pt2, pt3,
                                                 self.theta,
                                                 ref_face=face_pi)
                # Apply rotations of grey vertices.
                self.dfs1(v)
        self.vert_props[u].color = "black"
        self.black_verts.add(u)

    def dfs_flatten(self, u):
        """
        TODO: Doesn't work.
        """
        self.vert_props[u].color = "grey"
        self.grey_verts.add(u)
        # Apply all the rotations.
        for kk in self.rot_array:
            if kk not in self.black_verts and\
                    self.vert_props[u].d >= self.curr_rotn_layer:
                rr = self.grey_rots[kk]
                self.vert_props[u].rotate_about_plane(rr.ax1,
                                                    rr.ax2,
                                                    rr.ax3,
                                                    self.angle,
                                                    self.ref_pt)
        for v in self.adj[u]:
            if self.vert_props[v].color == "white":
                # The adjacency list of the base face.
                if self.vert_props[v].d == self.curr_rotn_layer:
                    self.grey_rots[v] = Rotation(self.vert_props[u],
                                                self.vert_props[v],
                                                self.angle)
                    self.rot_array.append(v)
                    self.vert_props[u].color = "grey"
                    self.grey_verts.add(v)
                self.dfs_flatten(v)
        self.vert_props[u].color = "black"
        self.black_verts.add(u)

    def flatten(self, u):
        for _ in range(self.max_depth):
            print("Rotations of layer: " + str(self.curr_rotn_layer))
            print(self.vert_props['0--0'].vertices)
            print(self.vert_props['+0-0'].vertices)
            #print(self.vert_props['-0+0'].vertices)
            print("---------------------------")
            self.dfs_flatten(u)
            self.curr_rotn_layer += 1
            self.reset_vert_col()


def scope_graph(adj, map, scoped=None):
    if scoped is None:
        scoped = {'00++', '+00+', '00-+', 
                  '-0-0', '00--', 
                  '0--0', '+0-0', '0+-0'}
    adj1 = {x:[i for i in adj[x] if i in scoped] for x in adj
                            if x in scoped}
    for k in adj1.keys():
        adj1[k] = [kk for kk in adj1[k] if kk in scoped]
    map1 = {x:map[x] for x in map
                            if x in scoped}
    return adj1, map1


def check_edge_case1(u, rr):
    pts = Face1(u).vertices
    ax1, ax2, ax3 = rr.ax1, rr.ax2, rr.ax3
    v1 = ax1 - ax2
    v2 = ax2 - ax3
    v3 = np.mean(pts, axis=0) - ax1
    v4 = np.random.uniform(size=4)
    a = np.array([v1, v2, v3, v4])
    if np.linalg.cond(a) > 1e5:
        print("Edge case-1: \
                The vectors aren't independent\
                as we were expecting!")
        return True
    return False


class Rotation():
    def __init__(self, f1, f2, angle=0):
        self.f1 = f1
        self.f2 = f2
        self.angle = angle
        self.ax1, self.ax2, self.ax3 = tfr.get_rotation_plane(
                                               f1, f2)


def tst_open():
    tf = TsrctFcGraph2(angle=np.pi/10)
    tf.bfs('00++')
    tf.reset_vert_col()
    r = rotation(4, np.pi*17/60.0)
    im = Image.new("RGB", (512, 512), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    tf.plot_all_faces(draw, r)
    im.save("Images//RotatingCube//im" +
                        str(0).rjust(4, '0') +
                        ".png")
    tf.curr_rotn_layer = 1
    for i in range(tf.max_depth):
        im = Image.new("RGB", (512, 512), (0, 0, 0))
        draw = ImageDraw.Draw(im, 'RGBA')
        #tf.flatten('00++')
        #tf.plot_all_faces(draw, r)
        tf.dfs_flatten('00++')
        tf.curr_rotn_layer += 1
        tf.reset_vert_col()
        tf.plot_all_faces(draw, r)
        im.save("Images//RotatingCube//im" +
                        str(i+1).rjust(4, '0') +
                        ".png")


def tst_open2(persp=0):
    tf = TsrctFcGraph2(angle=0.0)
    #tf.adj, tf.face_map = scope_graph(tf.adj, tf.face_map)
    tf.bfs('00++')
    tf.reset_vert_col()
    r = rotation(4, np.pi*17/60.0)
    im = Image.new("RGB", (512, 512), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    tf.plot_all_faces(draw, r, persp=persp)
    im.save("Images//RotatingCube//im" +
                        str(0).rjust(4, '0') +
                        ".png")
    for i in range(21):
        im = Image.new("RGB", (512, 512), (0, 0, 0))
        draw = ImageDraw.Draw(im, 'RGBA')
        tf.theta = np.pi/42.0*(i+1)
        for j in range(tf.max_depth):
            tf.reset_vert_col()
            tf.curr_d = j+1
            tf.dfs('00++')
        tf.plot_all_faces(draw, r, persp=persp)
        tf.reset()
        im.save("Images//RotatingCube//im" +
                        str(i+1).rjust(4, '0') +
                        ".png")


# if __name__ == "__main__":
#     #tf = TsrctFcGraph2()
#     #tf.dfs_flatten('00++')
#     tst_open2()
