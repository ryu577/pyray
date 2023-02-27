import numpy as np
from pyray.shapes.fourd.tesseract_graph import TsrctFcGraph, Face1
import pyray.shapes.fourd.tsrct_face_rotation as tfr
from pyray.rotation import rotation
from PIL import Image, ImageDraw


class TsrctFcGraph2(TsrctFcGraph):
    """
    This class is being created to open the Tesseract
    smoothly. Experimental as of now.
    """
    def __init__(self, angle=0, adj=None, base_face='00++'):
        super().__init__(angle, adj)
        self.grey_verts = set()
        self.base_face = Face1(base_face)
        self.random_face = Face1('+00+')

    def dfs_flatten(self, u):
        self.vert_props[u].color = "grey"
        self.grey_verts.add(u)
        # Apply all the rotations.
        for kk in self.grey_rots.keys():
            if kk not in self.black_verts:
                rr = self.grey_rots[kk]
                # Edge conditions.
                #if check_edge_case1(u, rr):
                #    breakpoint()
                # We need to ensure ax1, ax2, ax3 are
                # orthogonal to the face.
                self.vert_props[u].rotate_about_plane(rr.ax1,
                                                      rr.ax2,
                                                      rr.ax3,
                                                      self.angle)
        for v in self.adj[u]:
            if self.vert_props[v].color == "white":
                # Apply rotations of grey vertices.
                self.grey_rots[v] = Rotation(self.vert_props[u],
                                             self.vert_props[v],
                                             self.angle)
                self.dfs_flatten(v)
        self.vert_props[u].color = "black"
        self.black_verts.add(u)

    def plot_all_faces(self, draw, r):
        for kk in self.face_map.keys():
            ff = self.vert_props[kk]
            ff.plot(draw, r, rgba=(10,31,190,120))

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
    tf = TsrctFcGraph2(angle=np.pi/20)
    r = rotation(4, np.pi*17/60.0)
    im = Image.new("RGB", (512, 512), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    tf.plot_all_faces(draw, r)
    im.save("Images//RotatingCube//im" +
                        str(0).rjust(4, '0') +
                        ".png")
    for i in range(10):
        im = Image.new("RGB", (512, 512), (0, 0, 0))
        draw = ImageDraw.Draw(im, 'RGBA')
        tf.dfs_flatten('00++')
        tf.plot_all_faces(draw, r)
        im.save("Images//RotatingCube//im" +
                        str(i+1).rjust(4, '0') +
                        ".png")


if __name__ == "__main__":
    tf = TsrctFcGraph2()
    tf.dfs_flatten('00++')
