import numpy as np
import pyray.shapes.fourd.tesseract_graph as tg
from copy import deepcopy
import operator


class SqFace():
    def __init__(self, x, y, name, color="white"):
        self.x = x
        self.y = y
        self.name = name
        self.color = color


class SqMesh(tg.TsrctFcGraph):
    def __init__(self, tf):
        """
        tf is a Tesseract face graph or other object
        that has the relevant properties.
        """
        self.tf = tf
        self.adj = deepcopy(tf.adj)
        self.vert_props = {}
        self.vertices = []
        for k in self.adj.keys():
            x = round(tf.vert_props[k].face_center[0])
            y = round(tf.vert_props[k].face_center[1])
            self.vert_props[k] = SqFace(x, y, k)
            self.vertices.append([x, y])
        self.process_verts()
        
    def process_verts(self):
        self.vertices = np.array(self.vertices)
        self.vertices = sorted(self.vertices,key=operator.itemgetter(0,1))
        self.vertices = np.array(self.vertices)
        self.center_mass = self.vertices.mean(axis=0)
        self.vertices = self.vertices - self.center_mass

    def cut_mesh(self, f1, f2):
        m1 = deepcopy(self)
        m2 = deepcopy(self)
        m1.adj[f1].remove(f2)
        m1.adj[f2].remove(f1)
        m2.adj = deepcopy(m1.adj)
        m1.adj2 = {}
        m2.adj2 = {}
        m1.dfs_expl(f1)
        m2.dfs_expl(f2)
        m1.adj = m1.adj2
        m2.adj = m2.adj2
        return m1, m2

    def dfs_expl(self, u):
        self.vert_props[u].color = "grey"
        for v in self.adj[u]:
            if self.vert_props[v].color == "white":
                # Apply rotations of grey vertices.
                self.dfs_expl(v)
        self.vert_props[u].color = "black"
        self.adj2[u] = deepcopy(self.adj[u])

    def equals(self, m2):
        rot = np.array([[0,1],[-1,0]])
        for i in range(4):
            diff = abs(self.vertices-m2.vertices)
            if sum(sum(diff)) < 0.3:
                return True
            m2.vertices = np.dot(m2.vertices, rot)
            m2.process_verts()
        refl = np.array([[1,0],[0,-1]])
        m2.vertices = np.dot(m2.vertices, refl)
        m2.process_verts()
        for i in range(4):
            diff = abs(self.vertices-m2.vertices)
            if sum(sum(diff)) < 0.3:
                return True
            m2.vertices = np.dot(m2.vertices, rot)
            m2.process_verts()
        return False
