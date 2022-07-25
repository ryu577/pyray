import numpy as np
import pyray.shapes.twod.square_mesh as sm
import pyray.shapes.fourd.tesseract_graph as tg
from copy import deepcopy
import json
from PIL import Image, ImageDraw
from pyray.rotation import general_rotation, rotate_points_about_axis,\
    rotation
import time
import pyray.shapes.fourd.tst_open_tsrct as ot


def refresh_mesh(tf):
    tf.reset_rotations()
    tf.dfs_flatten2('00-+')
    tf.reset_vert_col()
    tf.actually_flatten()


def gen_tsrct_meshes():
    tf = tg.TsrctFcGraph(angle=np.pi/2)
    tf.dfs_flatten2('00-+')
    tf.reset_vert_col()
    tf.actually_flatten()

    ii = 0
    while ii < 100:
        # First get the two meshes.
        msh = sm.SqMesh(tf)
        f1 = np.random.choice([k for k in tf.adj.keys()])
        f2 = np.random.choice([k for k in tf.adj[f1]])
        #f1 = '-0-0'
        #f2 = '00-+'
        m1, m2 = msh.cut_mesh(f1, f2)

        # Loop through faces of m2.
        for u in m2.adj.keys():
            found = False
            vs = tg.get_edges(u)
            for v in vs:
                if (u,v) != (f1,f2):
                    if v in m1.adj:
                        old_adj = deepcopy(tf.adj)
                        tf.adj[f1].remove(f2)
                        tf.adj[f2].remove(f1)
                        tf.adj[u].add(v)
                        tf.adj[v].add(u)
                        refresh_mesh(tf)
                        tf.mk_xy_set()
                        if len(tf.xy_set) == 24:
                            print("Found a new mesh by connecting"
                                  + u + "," + v)
                            found = True
                            break
                        else:
                            print("Failed to find a valid mesh by connecting:"
                                  + u + "," + v)
                            tf.adj = old_adj
                            refresh_mesh(tf)
            if found:
                break

        if len(tf.xy_set) != 24:
            print("Invariant violated!")
            return
        if found:
            f_name = "Data//Meshes//mesh" +\
                                str(ii).rjust(4, '0') + ".txt"
            ii += 1
            adj = {}
            for k in tf.adj.keys():
                adj[k] = list(tf.adj[k])
            with open(f_name, "w") as file:
                file.write(json.dumps(adj))


def plot_mesh(ii=90):
    mesh_f1 = "Data//Meshes//mesh" +\
                                str(ii).rjust(4, '0') + ".txt"
    with open(mesh_f1, "r") as file:
        adj_str = file.read()
    adj = json.loads(adj_str)
    
    im = Image.new("RGB", (1024, 1024), (0, 0, 0))
    
    tf = tg.TsrctFcGraph(angle=np.pi/2)
    tf.adj = adj
    ot.rotate_tsrct_down(tf, im)
