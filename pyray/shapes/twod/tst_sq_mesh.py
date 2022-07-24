import numpy as np
import pyray.shapes.twod.square_mesh as sm
import pyray.shapes.fourd.tesseract_graph as tg


def tst1():
    tf = tg.TsrctFcGraph(angle=np.pi/2)
    tf.dfs_flatten2('00-+')
    tf.reset_vert_col()
    tf.actually_flatten()
    msh = sm.SqMesh(tf)
    m1, m2 = msh.cut_mesh('-0-0', '00-+')

