import numpy as np
import networkx as nx


def cube_trees():
    # First for a cube.. getting the spanning trees.
    a=5*np.eye(5)-np.ones((5,5))
    a[0,3]=0;a[3,0]=0;a[1,4]=0;a[4,1]=0
    np.linalg.det(a)
    # >> 384


class TsrctFcGraph():
    def __init__(self):
        self.face_map = {'--00': 0, '-0-0': 1,
                    '-00-': 2, '-00+': 3, '-0+0': 4, '-+00': 5,
                    '0--0':6, '0-0-':7, '0-0+':8, '0-+0':9,
                    '0+-0':10, '0+0-':11,'0+0+':12, '0++0':13,
                    '00--':14, '00-+':15, '00+-':16, '00++':17,
                    '+-00':18, '+0-0':19, '+00-':20, 
                    '+00+':21, '+0+0':22,'++00':23}

    def constrct(self):
        # Each face is connected to 8 other faces.
        deg_mat = np.eye(24)*8

        adj_mat = np.zeros((24, 24))
        for fc in self.face_map.keys():
            edgs = get_edges(fc)
            for ed in edgs:
                adj_mat[face_map[fc], face_map[ed]] = 1

        lapl = deg_mat - adj_mat
        b = np.delete(lapl, 1, 0)
        b = np.delete(b, 1, 1)
        print("Number of spanning trees of face graph: ")
        print(np.linalg.det(b))


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

def tsrct_cu_grph():
    deg_mat = 7*np.eye(8)
    adj_mat = np.ones((8,8))
    for ix in range(8):
        adj_mat[ix,ix]=0
        adj_mat[ix,7-ix]=0
    lapl = deg_mat - adj_mat

    b = np.delete(lapl,1,0)
    b = np.delete(b,1,1)

    np.linalg.det(b)
    # > 416745 spanning trees.
    # > 261 distinct meshes.

