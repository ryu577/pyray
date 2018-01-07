'''
Renders cubes of arbitrary dimensinoality and allows you to view them from different angles.
'''

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageMath
import sys

'''
A vertex object belonging to a cube.
'''
class Vertice():
    def __init__(self, i = 0, n = 4):
        # The dimensionality of the space the cube will live in.
        self.dim = n
        # All vertices of the cube have a natural index. For example, the point (0,0,..0) is index 0, (0,0,...,1) is index 1 and so on.
        self.index = i
        self.binary = self.to_binary()
        global scale

    '''
	Plots the vertice.
	args:
		r: The rotation matrix that describes what angle the scene is being viewed from.
		draw: The draw object associated with the image on which we can draw lines, ellipses and planes.
		rgba: The color we want the vertex.
		width: The size of the vertex circle.
		offset: Allows us to add an offset to all points while plotting.
		scale: How much are we scaling the scene?
		shift: What point on the image should correspond to the origin (coordinates larger than the second dimension will be 0)?
    '''
    def plot(self, r, draw, rgba, width=3, offset = None, scale=500, shift=np.array([1000,1000,0,0])):
        if offset is None:
            vv = np.dot(r,self.binary)
        else:
            vv = np.dot(r,self.binary + offset[:self.dim])
        [vx,vy] = (shift[:self.dim] + scale * vv)[0:2] # Projection on x-y plane
        draw.ellipse( (vx-width,vy-width,vx+width,vy+width), fill = rgba, outline = rgba)


	'''
    Obtains the binary representation of the current vertex.
    '''
    def to_binary(self):
        raw = np.zeros(self.dim)
        temp = self.index
        indx = 0
        while temp > 0:
            raw[indx] = temp%2
            temp = temp/2
            indx = indx + 1
        return raw

    '''
    Returns the rotated coordinates of the vertex after rotation by the associated rotation matrix.
    args:
    	r: The rotation matrix for the scene.
    '''
    def rotated(self, r):
        return np.dot(r,self.binary)

    '''
    Legacy method. Can be ignored.
    '''
    def plot_vid_ready(self,r,draw,rgba,width=9):
        dim = r.shape[0]
        reflection = np.ones(dim)
        reflection[1] = -1
        l = new_vector(r, (self.binary*reflection) * scale + shift[:dim] )
        draw.ellipse((l[0]-width,l[1]-width,l[0]+width,l[1]+width), fill = rgba, outline = rgba)

'''
The Edge object of the cube. There will be 12 edges.
'''
class Edge():
    def __init__(self, v1, v2, is_inter_dim_connector = False):
        self.vertice1 = v1
        self.vertice2 = v2
        self.is_inter_dim_connector = is_inter_dim_connector
        self.dim = v1.dim
        global scale

    '''
    Plots the edge
    args:
        offset: The amount by which the whole edge should be shifted in primitive coordinates.
    '''
    def plot(self, r, draw, rgba, width = 3, offset = None, scale=500, shift = np.array([1000,1000,1000,1000])):
        if offset is None:
            [v1, v2] = [np.dot(r, self.vertice1.binary), np.dot(r, self.vertice2.binary)]
        else:
            [v1, v2] = [np.dot(r, self.vertice1.binary+offset), np.dot(r, self.vertice2.binary+offset)]
        [v1x, v1y] = (shift[:self.dim] + scale * v1)[0:2]
        [v2x, v2y] = (shift[:self.dim] + scale * v2)[0:2]
        draw.line((v1x, v1y, v2x, v2y), fill=rgba, width=width)

    '''
    Legacy method. Can be ignored.
    '''
    def plot_vid_ready(self,r,draw,rgba,width=2):
        reflection = np.ones(dim)
        reflection[1] = -1
        v1 = new_vector(r,self.vertice1.binary*reflection * scale + shift[:dim])
        v2 = new_vector(r,self.vertice2.binary*reflection * scale + shift[:dim])
        draw.line((v1[0],v1[1],v2[0],v2[1]), fill=rgba, width=width)

'''
The Face object of the cube. There will be six faces.
'''
class Face():
    def __init__(self, vertices, is_inter_dim_connector = False):
        [v1,v2,v3,v4] = vertices
        self.vertice1 = v1
        self.vertice2 = v2
        self.vertice3 = v3
        self.vertice4 = v4
        self.is_inter_dim_connector = is_inter_dim_connector
        self.face_matrix = np.array([v1.binary, v2.binary, v3.binary, v4.binary]) # We can rotate the whole face in one shot.
        self.vertice_indices = np.array([v1.index,v2.index,v3.index,v4.index])
        global scale

    '''
    Adds an offset to the entire face.
    args:
    	a: The offset to add to the face.
    	dim: The dimensionality of the space our cube lives in.
    '''
    def add(self, a, dim):
        newv1 = Vertice(self.vertice1.index + a, dim)
        newv2 = Vertice(self.vertice2.index + a, dim)
        newv3 = Vertice(self.vertice3.index + a, dim)
        newv4 = Vertice(self.vertice4.index + a, dim)
        return Face([newv1, newv2, newv3, newv4])

    '''
    Changes the dimensionality of the underlying cube.
    args:
    	dim2: The new dimensionality we want the underlying cube to possess.
    '''
    def expand_dim(self, dim2):
        vertice1 = Vertice(self.vertice1.index, dim2)
        vertice2 = Vertice(self.vertice2.index, dim2)
        vertice3 = Vertice(self.vertice3.index, dim2)
        vertice4 = Vertice(self.vertice4.index, dim2)
        return Face([vertice1, vertice2, vertice3, vertice4])

    def expand_to_body(self, n = 0):
        if n == 0:
            curr_dim = len(self.vertice1.binary)
        else:
            curr_dim = n
        original_face = self
        original_face = self.expand_dim(curr_dim + 1)
        new_face = original_face.add(2**curr_dim, curr_dim+1)
        composed_face1 = Face([original_face.vertice1, original_face.vertice2, Vertice(original_face.vertice1.index + 2**(curr_dim), curr_dim+1), Vertice(original_face.vertice2.index+ 2**(curr_dim), curr_dim+1)])
        composed_face2 = Face([original_face.vertice2, original_face.vertice4, Vertice(original_face.vertice2.index + 2**(curr_dim), curr_dim+1), Vertice(original_face.vertice4.index+ 2**(curr_dim), curr_dim+1)])
        composed_face3 = Face([original_face.vertice3, original_face.vertice4, Vertice(original_face.vertice3.index + 2**(curr_dim), curr_dim+1), Vertice(original_face.vertice4.index+ 2**(curr_dim), curr_dim+1)])
        composed_face4 = Face([original_face.vertice1, original_face.vertice3, Vertice(original_face.vertice1.index + 2**(curr_dim), curr_dim+1), Vertice(original_face.vertice3.index+ 2**(curr_dim), curr_dim+1)])
        return Body([original_face, new_face, composed_face1, composed_face2, composed_face3, composed_face4])

    def plot(self, r, draw, rgba, highlightPoints = False):
        rotated_face = np.transpose(np.dot(r, np.transpose(self.face_matrix)))
        [v1,v2,v3,v4] = shift + scale * rotated_face
        draw.polygon([(v1[0], v1[1]), (v2[0], v2[1]), (v4[0], v4[1]), (v3[0], v3[1])], rgba) #First v4 then v3 because edges are not in increasing order
        if highlightPoints:
            for vv in [v1, v2, v3, v4]:
                [vx,vy] = vv[:2]
                draw.ellipse( (vx-4,vy-4,vx+4,vy+4), fill = 'red', outline = 'red')
            Edge(self.vertice1, self.vertice2).plot(r,draw,rgba,5)
            Edge(self.vertice2, self.vertice4).plot(r,draw,rgba,5)
            Edge(self.vertice3, self.vertice4).plot(r,draw,rgba,5)
            Edge(self.vertice1, self.vertice3).plot(r,draw,rgba,5)

    def plot_vid_ready(self, r, draw, rgba):
        dim = r.shape[0]
        reflection = np.ones(dim)
        reflection[1] = -1
        v1 = new_vector(r,self.vertice1.binary * reflection * scale + shift[:dim])
        v2 = new_vector(r,self.vertice2.binary * reflection * scale + shift[:dim])
        v3 = new_vector(r,self.vertice3.binary * reflection * scale + shift[:dim])
        v4 = new_vector(r,self.vertice4.binary * reflection * scale + shift[:dim])
        draw.polygon([(v1[0],v1[1]), (v2[0],v2[1]), (v4[0],v4[1]), (v3[0],v3[1])], rgba)

class Body():
    def __init__(self, faces):
        [f1,f2,f3,f4,f5,f6] = faces
        self.face1 = f1
        self.face2 = f2
        self.face3 = f3
        self.face4 = f4
        self.face5 = f5
        self.face6 = f6
    
    def add(self, a, dim):
        newf1 = self.face1.add(a, dim)
        newf2 = self.face2.add(a, dim)
        newf3 = self.face3.add(a, dim)
        newf4 = self.face4.add(a, dim)
        newf5 = self.face5.add(a, dim)
        newf6 = self.face6.add(a, dim)
        return Body([newf1,newf2,newf3,newf4,newf5,newf6])

    def plot(self, r, draw, rgba):
        self.face1.plot(r, draw, rgba, True)
        self.face2.plot(r, draw, rgba, True)
        self.face3.plot(r, draw, rgba, True)
        self.face4.plot(r, draw, rgba, True)
        self.face5.plot(r, draw, rgba, True)
        self.face6.plot(r, draw, rgba, True)


class Cube():    
    def __init__(self, n = 4, r = None):
        self.dim = n
        if r == None:
            self.r = np.eye(n)
        else:
            self.r = r
        config = self.generate_edges(n)
        self.vertices = config['vertices']
        self.edges = config['edges']
        self.generate_vertice_matrix()
        self.faces = self.generate_faces(n)
        self.bodies = self.generate_bodies(n)
        global scale

    def generate_vertice_matrix(self):
        self.vertice_matrix = []
        self.vertice_coordinate_sums = []
        for v in self.vertices:
            self.vertice_matrix.append(v.binary)
            self.vertice_coordinate_sums.append( sum(v.binary))
        self.vertice_matrix = np.array(self.vertice_matrix)
        self.vertice_coordinate_sums = np.array(self.vertice_coordinate_sums)

    def generate_edges(self,n):
        if n == 1:
            v1 = Vertice(0, self.dim)
            v2 = Vertice(1, self.dim)
            return { 'vertices': np.array([v1, v2]), 'edges': np.array([Edge(v1, v2)]) }
        else:
            previous = self.generate_edges(n-1)
            vertices = previous['vertices']
            edges = previous['edges']
            for i in previous['vertices']:
                v_new = Vertice(i.index + 2**(n-1), self.dim)
                vertices = np.insert(vertices, len(vertices), v_new )
                edges = np.insert(edges,len(edges),Edge(i, v_new))
            for i in previous['edges']: #Loop through edges
                edges = np.insert(edges, len(edges), (Edge(vertices[i.vertice1.index + 2**(n-1)], vertices[i.vertice2.index + 2**(n-1)])) )
            return {'vertices' : vertices, 'edges' : edges}

    def generate_faces(self, n):
        if n < 2:
            return None
        elif n == 2:
            vertices = self.generate_edges(2)['vertices']
            return np.array([Face( [vertices[0], vertices[1], vertices[2], vertices[3]])])
        else:
            faces = previous_faces = self.generate_faces(n-1)
            previous_edges = self.generate_edges(n-1)['edges']
            current_edges = self.generate_edges(n)
            current_vertices = current_edges['vertices']
            for i in previous_faces:
                faces = np.insert(faces, len(faces), Face(current_vertices[i.vertice_indices + 2**(n-1)]))
            for i in previous_edges:
                new_face = Face([i.vertice1, i.vertice2, current_vertices[i.vertice1.index + 2**(n-1)], current_vertices[i.vertice2.index + 2**(n-1)] ])
                faces = np.insert(faces,len(faces), new_face)
            return faces

    def generate_bodies(self, n):
        if n < 3:
            return None
        elif n == 3:
            faces = self.generate_faces(3)
            return np.array([Body(faces)])
        else:
            bodies = previous_bodies = self.generate_bodies(n-1)
            previous_faces = self.generate_faces(n-1)
            for i in previous_bodies:
                bodies = np.insert(bodies, len(bodies), i.add(2**(n-1),n))
            for i in previous_faces:
                bodies = np.insert(bodies, len(bodies), i.expand_to_body(n-1))
            return bodies

    def generate_sequential_edges(self):
        self.sequential_edges = []
        for i in range(len(self.vertices) - 1):
            self.sequential_edges.append(Edge(self.vertices[i], self.vertices[i+1]))

    def generate_classic_edges(self):
        self.classic_edges = []
        for i in self.edges:
            self.classic_edges.append(np.array([i.vertice1.binary, i.vertice2.binary]))
        self.classic_edges = np.array(self.classic_edges)

    def plot_edges(self, r = None, seq = False, j = 0):
        if r == None:
            r = rotation(self.dim)
        im = Image.new("RGB", (2048, 2048), (1,1,1))
        draw = ImageDraw.Draw(im,'RGBA')
        if seq:
            self.generate_sequential_edges()
            edges = self.sequential_edges
        else:
            edges = self.edges
        for edge in edges:
            [v1, v2] = [ np.dot(r, edge.vertice1.binary), np.dot(r, edge.vertice2.binary)]
            [v1x,v1y] = (shift[:self.dim] + scale * v1)[0:2]
            [v2x,v2y] = (shift[:self.dim] + scale * v2)[0:2]
            draw.line((v1x, v1y, v2x, v2y), fill=(255,165,0), width=2)
        return [im, draw]


    def plot_edges2(self, draw, r = None, seq = False, offset = None,fill=(255,165,5),scale=500,shift=np.array([1000,1000,0,0])):
        if offset is None:
            offset = np.zeros(self.dim)
        if r == None:
            r = rotation(self.dim)
        if seq:
            self.generate_sequential_edges()
            edges = self.sequential_edges
        else:
            edges = self.edges
        for edge in edges:
            if edge.vertice1.index == 0:
                [v1, v2] = [np.dot(r, edge.vertice1.binary + offset), np.dot(r, edge.vertice2.binary + offset)]
            elif edge.vertice2.index == 2**(self.dim) - 1:
                [v1, v2] = [np.dot(r, edge.vertice1.binary - offset), np.dot(r, edge.vertice2.binary - offset)]
            else:
                [v1, v2] = [np.dot(r, edge.vertice1.binary), np.dot(r, edge.vertice2.binary)]
            [v1x,v1y] = (shift[:self.dim] + scale * v1)[0:2]
            [v2x,v2y] = (shift[:self.dim] + scale * v2)[0:2]
            draw.line((v1x, v1y, v2x, v2y), fill=fill, width=4)

    def plot_faces(self, r = None, j = 0, body_indice = None):
        if r == None:
            r = rotation(self.dim)
        im = Image.new("RGB", (2048, 2048), "black")
        draw = ImageDraw.Draw(im,'RGBA')
        for f in self.faces:
            f.plot(r, draw, (255, 55, 0, 22))
        for edge in self.edges:
            edge.plot(r, draw, (255,131,0))
        if body_indice != None:
            indx = 0
            colors = [(255, 255, 0, 100), (200, 80, 100, 100), (255,0,0,100), (0,255,0,100), (0,0,255,100), (0,255,255,100), (255,0,255,100), (120,80,200,100)]
            for bi in body_indice:
                j = j + bi * 10**indx + 1
                body = self.bodies[bi]
                body.plot(r, draw, colors[bi])
                indx = indx + 1
        im.save('Images\\RotatingCube\\im' + str(j) + '.png')


'''
Legacy method. Can be ignored.
'''
def new_vector(r, v, dim = 4):
    translate = np.zeros(dim)
    translate[0] = 1000
    translate[1] = 1000
    v = v - translate #1000,1000 should go to 0,0. 
    v = v / scale
    v = np.dot(r,v)
    v = v * scale
    v = v + translate
    return v



