import numpy as np
from pyray.shapes.fourd.tesseract_graph import TsrctFcGraph
import pyray.shapes.fourd.tsrct_face_rotation as tfr


class TsrctFcGraph2(TsrctFcGraph):
    """
    This class is being created to open the Tesseract
    smoothly. Experimental as of now.
    """
    def __init__(self, angle=0, adj=None):
        super().__init__(angle, adj)
        self.grey_verts = set()

    def dfs_flatten(self, u):
        self.vert_props[u].color = "grey"
        self.grey_verts.add(u)
        # Apply all the rotations.
        for kk in self.grey_rots.keys():
            if kk not in self.black_verts:
                ax1, ax2, ax3 = self.grey_rots[kk]
                self.vert_props[u].rotate_about_plane(ax1, ax2,
                                                      ax3,
                                                      self.angle)
        for v in self.adj[u]:
            if self.vert_props[v].color == "white":
                # Apply rotations of grey vertices.
                self.grey_rots[v] = tfr.get_rotation_plane(
                                               self.vert_props[u],
                                               self.vert_props[v])
                self.dfs_flatten(v)
        self.vert_props[u].color = "black"
        self.black_verts.add(u)


if __name__ == "__main__":
    tf = TsrctFcGraph2()
    tf.dfs_flatten('00++')
