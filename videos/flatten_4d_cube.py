from pyray.shapes.fourd.open_tsrct import TsrctFcGraph2
from pyray.rotation import rotation
from pyray.shapes.fourd.tsrct_cube_graph import primitive_tsrct_open,\
    TsrctCubeTree, open_tsrct_proper
import pyray.shapes.solid.open_cube as oc
from pyray.rotation2.rotn_4d import get_common_verts
from pyray.shapes.solid.open_cube import map_to_plot, plot_grid
from pyray.rotation import general_rotation, yzrotation, xyrotation
from PIL import Image, ImageDraw
import numpy as np
from copy import deepcopy


def tsrct1(persp=0, i=0, r=rotation(4, np.pi*17/60.0)):
    tf = TsrctFcGraph2(angle=0.0)
    #tf.adj, tf.face_map = scope_graph(tf.adj, tf.face_map)
    tf.bfs('00++')
    tf.reset_vert_col()
    im = Image.new("RGB", (512, 512), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    tf.plot_all_faces(draw, r, persp=persp)
    im.save("Images//RotatingCube//im" +
                        str(i).rjust(4, '0') +
                        ".png")


def scene1():
    # Note: the rotation scheme from here has been promoted to
    # rotn_4d/rotn_1
    r1 = np.eye(4)
    r1[1:3,1:3] = \
            np.array([[np.cos(np.pi/4), np.sin(np.pi/4)],
                    [-np.sin(np.pi/4),np.cos(np.pi/4)]])
    r2 = np.eye(4)
    r2[0:2,0:2] = \
            np.array([[np.cos(np.pi/4), np.sin(np.pi/4)],
                    [-np.sin(np.pi/4),np.cos(np.pi/4)]])
    r = np.dot(r1, r2)
    r3 = np.eye(4)

    persps = [0, 21, 19, 18, 16, 14, 
            12, 10, 9, 8, 7, 6, 5]
    for i in range(100):
        r3[np.ix_([0,3],[0,3])] = \
            np.array([[np.cos(np.pi/8*i/13), np.sin(np.pi/8*i/13)],
                    [-np.sin(np.pi/8*i/13),np.cos(np.pi/8*i/13)]])
        r = np.dot(r1, r2)
        r = np.dot(r, r3)
        i1 = min(i, len(persps)-1)
        tsrct1(persp=5, i=i, r=r)


def scene2():
    r1 = np.eye(4)
    r1[1:3,1:3] = \
            np.array([[np.cos(np.pi/4), np.sin(np.pi/4)],
                    [-np.sin(np.pi/4),np.cos(np.pi/4)]])
    r2 = np.eye(4)
    r2[0:2,0:2] = \
            np.array([[np.cos(np.pi/4), np.sin(np.pi/4)],
                    [-np.sin(np.pi/4),np.cos(np.pi/4)]])
    r = np.dot(r1, r2)
    r3 = np.eye(4)
    for i in range(100):
        i1 = i
        r3[np.ix_([0,3],[0,3])] = \
            np.array([[np.cos(np.pi/8*i1/13), np.sin(np.pi/8*i1/13)],
                    [-np.sin(np.pi/8*i1/13),np.cos(np.pi/8*i1/13)]])
        r = np.dot(r1, r2)
        r = np.dot(r, r3)
        primitive_tsrct_open(persp=5, i=i, r=r)


#########################
## Now start the scenes.

# scene-1
i = 0
for j in range(20):
    i = j
    im = Image.new("RGB", (512, 512), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    gr = oc.GraphCube(survive_ros={0, 1, 2, 3, 6})
    f1 = oc.Face('00+')
    f1.vertices = np.array([[-5,1,-5],[-5,1,5],[5,1,-5],[5,1,5]])
    r = general_rotation(np.array([1,1,1]), np.pi/6)
    z1 = np.dot(r, np.array([0,1,0]))
    r1 = general_rotation(z1, np.pi/20*i)
    gr.draw = draw
    gr.r = np.dot(r1, r)
    #gr.dfs_flatten('0+0')
    #gr.reset_vert_col()
    gr.dfs_plot_2('00+', rgba=(128, 108, 81, 97))
    f1.plot(draw, gr.r, scale=40, rgba=(113, 121, 126, 40), wdh=0)
    im.save("Images//RotatingCube//im" +
                                    str(i).rjust(4, '0') +
                                    ".png")
# ffmpeg -framerate 10 -i im%04d.png -c:v libx264 -vf "format=yuv420p" out.mp4

# Draw the edges.
# scene-2
r = gr.r
surv = {0, 1, 2, 3, 6}
for i in range(20):
    im = Image.new("RGB", (512, 512), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    r1 = general_rotation(z1, np.pi/60*i)
    gr.r = np.dot(r1, r)
    gr.draw = draw
    gr.reset_vert_col()
    gr.dfs_plot_2('00+', rgba=(128, 108, 81, 97))
    p = 1-i/11.0
    p = max(p, 0.0)
    f1 = oc.Face('00+')
    f1.vertices = np.array([[-5,1,-5],[-5,1,5],[5,1,-5],[5,1,5]])
    f1.plot(draw, gr.r, scale=40, rgba=(113, 121, 126, 40), wdh=0)
    for j in range(12):
        if j not in surv:
            edge = gr.edges[j]
            f1 = gr.vert_props[edge[0]]
            f2 = gr.vert_props[edge[1]]
            v1 = get_common_verts(f1.vertices, f2.vertices)
            rotated_verts = np.transpose(np.dot(gr.r, np.transpose(v1)))
            x, y = map_to_plot(rotated_verts[0][0], rotated_verts[0][1])
            x1, y1 = map_to_plot(rotated_verts[1][0], rotated_verts[1][1])
            x_mid = (x+x1)/2
            y_mid = (y+y1)/2
            xx = p*x_mid+(1-p)*x
            xx1 = p*x_mid+(1-p)*x1
            yy = p*y_mid+(1-p)*y
            yy1 = p*y_mid+(1-p)*y1
            draw.line((xx, yy, xx1, yy1), fill=(120, 120, 0), width=5)
    im.save("Images//RotatingCube//im" +
            str(i).rjust(4, '0') +
            ".png")

# ffmpeg -framerate 10 -i im%04d.png -c:v libx264 -vf "format=yuv420p" out.mp4

# Open the cube.
# scene-3 and scene-4. Scene-3 is 1-10 and 4 is 11 onwards
r = gr.r
for i in range(41):
    im = Image.new("RGB", (512, 512), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    gr = oc.GraphCube(survive_ros={0, 1, 2, 3, 6})
    gr.r = r
    gr.angle = -np.pi*i/20.0
    gr.draw = draw
    f1 = oc.Face('00+')
    f1.vertices = np.array([[-5,1,-5],[-5,1,5],[5,1,-5],[5,1,5]])
    f1.plot(draw, gr.r, scale=40, rgba=(113, 121, 126, 40), wdh=0)
    gr.dfs_flatten('0+0')
    gr.reset_vert_col()
    gr.dfs_plot_2('0+0', rgba=(128, 108, 81, 97))
    mm = 0
    if i >= mm:
        im.save("Images//RotatingCube//im" +
            str(i-mm).rjust(4, '0') +
            ".png")

# scene-5
# Show grid.
for i in range(11):
    im = Image.new("RGB", (512, 512), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    gr = oc.GraphCube(survive_ros={0, 1, 2, 3, 6})
    gr.r = r
    gr.angle = -np.pi*i/20.0
    #gr.angle = -0.0
    gr.draw = draw
    gr.dfs_flatten('0+0')
    gr.reset_vert_col()
    gr.dfs_plot_2('00+',
                  rgba=(128, 108, 81, 97),
                  scale=40,
                  shift=(256,256))
    plot_grid(draw, gr.r)
    f1 = oc.Face('00+')
    f1.vertices = np.array([[-5,1,-5],[-5,1,5],[5,1,-5],[5,1,5]])
    f1.plot(draw, gr.r, scale=40, rgba=(113, 121, 126, 40), wdh=0)
    im.save("Images//RotatingCube//im" +
                str(i).rjust(4, '0') +
                ".png")


def plot_msh(msh, draw):
    #draw.line((3, 3, 250, 250), 
    #        fill = (255,255,255,100), width = 5)
    gr, shift, scale = msh
    gr.reset_vert_col()
    gr.draw = draw
    gr.dfs_plot_2('00+',
                    rgba=(128, 108, 81, 97),
                    scale=scale,
                    shift=shift)


def make_scene6(surv={0, 1, 2, 3, 6}, i1=0, mshno=0):
    meshes = []
    th = np.pi/2
    r_yz = yzrotation(th)
    r_xy = xyrotation(3*th)
    rr1 = np.dot(r_yz, r.T)
    rr1 = np.dot(r_xy, rr1)
    ee, q = np.linalg.eig(rr1)
    for i in range(11):
        im = Image.new("RGB", (512, 512), (0,0,0))
        draw = ImageDraw.Draw(im, 'RGBA')
        gr1 = oc.GraphCube(survive_ros=surv)
        gr1.r = r
        gr1.angle = -np.pi/20.0*(i)
        gr1.draw = draw
        gr1.dfs_flatten('0+0')
        gr1.reset_vert_col()
        gr1.dfs_plot_2('00+',
                    rgba=(128, 108, 81, 97),
                    scale=40,
                    shift=(256,256))
        plot_grid(draw, gr1.r)
        f1 = oc.Face('00+')
        f1.vertices = np.array([[-5,1,-5],[-5,1,5],[5,1,-5],[5,1,5]])
        f1.plot(draw, gr1.r, scale=40, rgba=(113, 121, 126, 40), wdh=0)
        for msh in meshes:
            plot_msh(msh, draw)
        im.save("Images//RotatingCube//im" +
                    str(i1+i).rjust(4, '0') +
                    ".png")
        i2 = i1+i
    for i in range(11):
        im = Image.new("RGB", (512, 512), (0, 0, 0))
        draw = ImageDraw.Draw(im, 'RGBA')
        gr = oc.GraphCube(survive_ros=surv)
        rr = np.dot(np.dot(q,np.diag(ee**(i/10.0))), 
                    np.linalg.inv(q))
        gr.r = np.dot(rr, r)
        gr.angle = -np.pi/2.0
        gr.draw = draw
        gr.dfs_flatten('0+0')
        gr.reset_vert_col()
        gr.dfs_plot_2('00+',
                    rgba=(128, 108, 81, 97),
                    scale=40-3.2*i,
                    shift=(256-23*i+75*(mshno%6)*i/10,256-23*i+75*(mshno//6)*i/10))
        if i == 10:
            gr.draw = None
            meshes.append((deepcopy(gr), 
                           (256-23*i+75*(mshno%6)*i/10,256-23*i+75*(mshno//6)*i/10), 40-3.2*i))
        gr1 = oc.GraphCube(survive_ros=surv)
        gr1.r = r
        gr1.angle = -np.pi/20.0*(10-i)
        gr1.draw = draw
        gr1.dfs_flatten('0+0')
        gr1.reset_vert_col()
        gr1.dfs_plot_2('00+',
                    rgba=(128, 108, 81, 97),
                    scale=40,
                    shift=(256,256))
        
        plot_grid(draw, gr1.r)
        f1 = oc.Face('00+')
        f1.vertices = np.array([[-5,1,-5],[-5,1,5],[5,1,-5],[5,1,5]])
        f1.plot(draw, gr1.r, scale=40, rgba=(113, 121, 126, 40), wdh=0)
        for msh in meshes:
            plot_msh(msh, draw)
        im.save("Images//RotatingCube//im" +
                    str(i2+i+1).rjust(4, '0') +
                    ".png")

# scene-6
#make_scene6()

# scene-7:
trees = \
[
    [('-00','00+'),('00+','+00'),('00+','0-0'),('0-0','00-'),('00-','0+0')],
    [('-00','00+'),('00+','0-0'),('0-0','+00'),('0-0','00-'),('00-','0+0')],
    [('-00','00+'),('00+','0-0'),('0-0','00-'),('00-','+00'),('00-','0+0')],
    [('-00','00+'),('00+','0-0'),('0-0','00-'),('00-','0+0'),('0+0','+00')],
    [('00+','0-0'),('0-0','-00'),('0-0','00-'),('00-','0+0'),('00-','+00')],
    [('00+','0-0'),('0-0','+00'),('0-0','-00'),('0-0','00-'),('00-','0+0')],
    #[('-00','00+'),('00+','0-0'),('0-0','00-'),('00-','0+0'),('0+0','+00')],
    [('00+','-00'),('-00','0-0'),('0-0','00-'),('0-0','+00'),('00-','0+0')],
    [('-00','00+'),('00+','0-0'),('0-0','+00'),('+00','00-'),('00-','0+0')],
    [('-00','00+'),('00+','0-0'),('0-0','00-'),('00-','+00'),('+00','0+0')],
    [('-00','00+'),('00+','0-0'),('0-0','+00'),('+00','00-'),('+00','0+0')],
    [('0+0','00-'),('00-','0-0'),('0-0','+00'),('+00','00+'),('00+','-00')]
 ]

gr = oc.GraphCube(survive_ros={0, 1, 2, 3, 6})
incl_lst = []
for i in range(len(trees)):
    tree = trees[i]
    j = 0
    surv = set()
    for ed in tree:
        if ed in gr.edg_dict:
            surv.add(gr.edg_dict[ed])
        elif ed in gr.rev_edg_dict:
            surv.add(gr.rev_edg_dict[ed])
        else:
            break
    incl_lst.append(surv)


for i in range(len(incl_lst)):
    make_scene6(incl_lst[i], 22*i, mshno=i)

# 230608 for scene7.


