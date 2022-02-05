import numpy as np
from PIL import Image, ImageDraw
from scipy.spatial import ConvexHull

from pyray.axes import *
from pyray.color import *
from pyray.geometric import *
from pyray.misc import *
from pyray.rotation import *
from pyray.shapes.solid.cube import *

width = 15
im_ind = 70
scale = 500
shift = np.array([1000, 1000, 0, 0, 0])
basepath = ".\\Images\\"

c1 = Cube(4)
r = np.eye(4)
r[:3, :3] = rotation(3, np.pi * 2 * 27 / 80.0)
r1 = rotation(4, np.pi * 2 * im_ind / 80.0)
r = np.dot(r, r1)

[im, draw] = c1.plot_edges(r, shift=shift, scale=scale)

rotated_vertices = (
    np.transpose(np.dot(r, np.transpose(c1.vertice_matrix))) * scale + shift[:4]
)
hexag = rotated_vertices[
    [i.index for i in c1.vertices[c1.vertice_coordinate_sums == 2]]
]
sqr1 = rotated_vertices[[i.index for i in c1.vertices[c1.vertice_coordinate_sums == 3]]]
sqr2 = np.delete(sqr1, -1, axis=1)
draw.polygon(ConvexHull(sqr2).points, (255, 0, 0, 60))
hexag2 = np.delete(hexag, -1, axis=1)
draw.polygon(ConvexHull(hexag2).points, (0, 255, 0, 30))

for ver in c1.vertices[c1.vertice_coordinate_sums == 3]:
    ver.plot(r, draw, (255, 0, 0), 10)
    for ver1 in c1.vertices[c1.vertice_coordinate_sums == 3]:
        e = Edge(ver, ver1)
        e.plot(r, draw, (255, 0, 0), width=2)

for ver in c1.vertices[c1.vertice_coordinate_sums == 1]:
    ver.plot(r, draw, (0, 0, 255), 10)
    for ver1 in c1.vertices[c1.vertice_coordinate_sums == 1]:
        e = Edge(ver, ver1)
        e.plot(r, draw, (0, 0, 255))
for ed in [
    (5, 3),
    (5, 6),
    (5, 9),
    (5, 12),
    (10, 3),
    (10, 6),
    (10, 9),
    (10, 12),
    (3, 6),
    (3, 9),
    (12, 6),
    (12, 9),
]:
    v1 = rotated_vertices[ed[0]]
    v2 = rotated_vertices[ed[1]]
    draw.line((v1[0], v1[1], v2[0], v2[1]), fill=(0, 255, 0), width=4)
for ver in c1.vertices[c1.vertice_coordinate_sums == 2]:
    ver.plot(r, draw, (0, 255, 0), 10)
sqr2 = rotated_vertices[[i.index for i in c1.vertices[c1.vertice_coordinate_sums == 1]]]
sqr3 = np.delete(sqr2, -1, axis=1)
draw.polygon(ConvexHull(sqr3).points, (0, 0, 255, 60))

v1 = rotated_vertices[0]
v2 = rotated_vertices[15]
draw.line((v1[0], v1[1], v2[0], v2[1]), fill=(255, 255, 255), width=2)
im.save(basepath + "im" + str(im_ind) + ".png")


######################

verts = np.array(
    [
        [0, 0, 1, 2],
        [0, 1, 0, 2],
        [1, 0, 0, 2],
        [0, 0, 2, 1],
        [0, 2, 0, 1],
        [2, 0, 0, 1],
        [0, 1, 2, 0],
        [1, 0, 2, 0],
        [2, 0, 1, 0],
        [0, 2, 1, 0],
        [1, 2, 0, 0],
        [2, 1, 0, 0],
    ]
)

edge_ixs = []
for i in range(len(verts)):
    for j in range(i + 1, len(verts)):
        v1 = verts[i]
        v2 = verts[j]
        if sum((v1 - v2) ** 2) < 3:
            edge_ixs.append((i, j))

r = np.eye(4)
r[:3, :3] = rotation(3, np.pi * 2 * 27 / 80.0)

for im_ind in range(100):
    r1 = rotation(4, np.pi * 2 * im_ind / 80.0)
    r = np.dot(r, r1)
    rotated_vertices = np.transpose(np.dot(r, np.transpose(verts))) * scale + shift[:4]
    im = Image.new("RGB", (2048, 2048), (1, 1, 1))
    draw = ImageDraw.Draw(im, "RGBA")
    for ex in edge_ixs:
        v1x, v1y = rotated_vertices[ex[0]][0], rotated_vertices[ex[0]][1]
        v2x, v2y = rotated_vertices[ex[1]][0], rotated_vertices[ex[1]][1]
        draw.line((v1x, v1y, v2x, v2y), fill=(255, 165, 0), width=2)

    im.save(basepath + "im" + str(im_ind) + ".png")


######################
import itertools

verts = list(itertools.permutations([0, 1, 2, 3]))
verts = np.asarray(verts)

edge_ixs = []
for i in range(len(verts)):
    for j in range(i + 1, len(verts)):
        v1 = verts[i]
        v2 = verts[j]
        if sum((v1 - v2) ** 2) < 3:
            edge_ixs.append((i, j))

r = np.eye(4)
r[:3, :3] = rotation(3, np.pi * 2 * 27 / 80.0)

for im_ind in range(100):
    r1 = rotation(4, np.pi * 2 * im_ind / 80.0)
    r = np.dot(r, r1)
    rotated_vertices = np.transpose(np.dot(r, np.transpose(verts))) * scale + shift[:4]
    im = Image.new("RGB", (2048, 2048), (1, 1, 1))
    draw = ImageDraw.Draw(im, "RGBA")
    for ex in edge_ixs:
        v1x, v1y = rotated_vertices[ex[0]][0], rotated_vertices[ex[0]][1]
        v2x, v2y = rotated_vertices[ex[1]][0], rotated_vertices[ex[1]][1]
        draw.line((v1x, v1y, v2x, v2y), fill=(255, 165, 0), width=2)

    im.save(basepath + "im" + str(im_ind) + ".png")
