'''
Methods for drawing primitive constructs like axes, grids, arrows, etc.
'''

import numpy np

'''
Draws four axes in 4d space. If the fourth row and fourth column of the rotation matrix, r are identity-like (0,0,0,1), you will not see the fourth axis.
'''
def render_scene_4d_axis(draw, r = np.eye(4), width = 9, scale = 200, shift = np.array([1000,1000,0])):
    shift2 = -shift + np.array([1000,1000,0])
    x_axis_start = new_vector_4d(r, np.array([0, 1000, 0, 0]))
    x_axis_end = new_vector_4d(r, np.array([2048, 1000, 0, 0]))
    y_axis_start = new_vector_4d(r, np.array([1000, 0, 0, 0]))
    y_axis_end = new_vector_4d(r, np.array([1000, 2048, 0, 0]))
    z_axis_start = new_vector_4d(r, np.array([1000, 1000, -1000, 0]))
    z_axis_end = new_vector_4d(r, np.array([1000, 1000, 2048, 0]))
    w_axis_start = new_vector_4d(r, np.array([1000, 1000, 0, -1000]))
    w_axis_end = new_vector_4d(r, np.array([1000, 1000, 0, 2048]))
    draw.line((x_axis_start[0]-shift2[0],x_axis_start[1]-shift2[1],x_axis_end[0]-shift2[0],x_axis_end[1]-shift2[1]), fill="silver", width=width)
    draw.line((y_axis_start[0]-shift2[0],y_axis_start[1]-shift2[1],y_axis_end[0]-shift2[0],y_axis_end[1]-shift2[1]), fill="silver", width=width)
    draw.line((z_axis_start[0]-shift2[0],z_axis_start[1]-shift2[1],z_axis_end[0]-shift2[0],z_axis_end[1]-shift2[1]), fill="silver", width=width)
    draw.line((w_axis_start[0],w_axis_start[1],w_axis_end[0],w_axis_end[1]), fill="gold", width=width)


def render_xy_plane(draw, r = np.eye(4), width = 5):
    for i in np.arange(0,2000,100)*1.0:
        x_axis_start = new_vector_4d(r, np.array([0, i, 0, 0]))
        x_axis_end = new_vector_4d(r, np.array([2048, i, 0, 0]))
        y_axis_start = new_vector_4d(r, np.array([i, 0, 0, 0]))
        y_axis_end = new_vector_4d(r, np.array([i, 2048, 0, 0]))
        draw.line((x_axis_start[0],x_axis_start[1],x_axis_end[0],x_axis_end[1]), fill=(248,50,0,70), width=width)
        draw.line((y_axis_start[0],y_axis_start[1],y_axis_end[0],y_axis_end[1]), fill=(248,50,0,70), width=width)


'''
Draws an x-y grid over the x-y plane
'''
def drawXYGrid(draw, r, meshLen = 0.5, extent = 1.0, shift = np.array([1000.0,1000.0,0.0]),scale=200.0):
    upper = 5.5*extent
    #First, draw some lines parallel to the x-axis
    for x in np.arange(-5.0,upper,meshLen):
        pt1 = np.dot(r, np.array([x,-5.0,0]))*scale + shift[:3]
        pt2 = np.dot(r,np.array([x,5.0,0]))*scale + shift[:3]
        draw.line((pt1[0],pt1[1],pt2[0],pt2[1]),(102,255,51, 120),width=2)
    for y in np.arange(-5.0,upper,meshLen):
        pt1 = np.dot(r, np.array([-5.0,y,0]))*scale + shift[:3]
        pt2 = np.dot(r,np.array([5.0,y,0]))*scale + shift[:3]
        draw.line((pt1[0],pt1[1],pt2[0],pt2[1]),(102,255,51, 120),width=2)


'''
Draws an arrow from start point to end point.
'''
def arrowV1(draw, r, start, end, rgb = (0,255,0), scale=200, shift=np.array([1000,1000,0])):
    rgba = rgb + (150,)
    [cx,cy,cz] = start + (end-start) * 0.8 # The base of the arrow.
    c_vec = np.dot(r, np.array([cx,cy,cz])) * scale + shift[:3]
    [ex,ey,ez] = (end - start)
    if abs(ez) < 1e-6:
        arrowV2(draw, r, start, end, rgb, scale, shift)
        return
    start = np.dot(r, start) * scale + shift[:3]
    end = np.dot(r, end) * scale + shift[:3]
    d = 0.08
    y1_range = abs(d * (ez**2 + ex**2)**0.5/ (ex**2 + ey**2 + ez**2)**.5)
    for y1 in np.arange(-y1_range, y1_range, 0.0033):
        det = max(4*ex**2*ey**2/ ez**4 * y1**2 - 4*((1 + ey**2/ez**2)*y1**2 - d**2)*(1 + ex**2/ez**2),0)
        x1 = (-2*(ex*ey/ez**2*y1) + det**0.5)/2/(1+ex**2/ez**2)
        z1 = (-ex*x1 - ey*y1)/ez
        xyz = np.array([x1 + cx, y1 + cy, z1 + cz ])
        xyz = np.dot(r, xyz) * scale + shift[:3]
        draw.line((xyz[0],xyz[1],c_vec[0],c_vec[1]), fill = rgba, width=5)
        draw.line((xyz[0],xyz[1],end[0],end[1]), fill = rgba, width=5)
        x1 = (-2*(ex*ey/ez**2*y1) - det**0.5)/2/(1+ex**2/ez**2)
        z1 = (-ex*x1 - ey*y1)/ez
        xyz = np.array([x1 + cx, y1 + cy, z1 + cz ])
        xyz = np.dot(r, xyz) * scale + shift[:3]
        draw.line((xyz[0],xyz[1],c_vec[0],c_vec[1]), fill = rgba, width=5)
        draw.line((xyz[0],xyz[1],end[0],end[1]), fill = rgba, width=5)
    draw.line((start[0],start[1],end[0],end[1]),fill=rgb,width=5)

def arrowV2(draw, r, start, end, rgb = (0,255,0), scale = 200, shift = np.array([1000,1000,0])):
    rgba = rgb + (150,)
    [cx,cy,cz] = start + (end-start) * 0.8 # The base of the arrow.
    c_vec = np.dot(r, np.array([cx,cy,cz])) * scale + shift[:3]
    [ex,ey,ez] = (end - start)
    if abs(ey) < 1e-6:
        arrowV3(draw, r, start, end, rgb, shift = shift, scale = scale)
        return
    start = np.dot(r, start) * scale + shift[:3]
    end = np.dot(r, end) * scale + shift[:3]
    d = 0.08
    x1_range = abs(d * ey / (ex**2 + ey**2)**0.5)

    for x1 in np.arange(-x1_range, x1_range, x1_range/30):
        y1 = -ex/ey * x1
        z1 = max( (d**2 - x1**2*(1+ex**2/ey**2)), 0) **0.5
        xyz = np.array([x1 + cx, y1 + cy, z1 + cz ])
        xyz = np.dot(r, xyz) * scale + shift[:3]
        draw.line((xyz[0],xyz[1],c_vec[0],c_vec[1]), fill = rgba, width=5)
        draw.line((xyz[0],xyz[1],end[0],end[1]), fill = rgba, width=5)
        z1 = -z1
        xyz = np.array([x1 + cx, y1 + cy, z1 + cz ])
        xyz = np.dot(r, xyz) * scale + shift[:3]
        draw.line((xyz[0],xyz[1],c_vec[0],c_vec[1]), fill = rgba, width=5)
        draw.line((xyz[0],xyz[1],end[0],end[1]), fill = rgba, width=5)
    draw.line((start[0],start[1],end[0],end[1]),fill=rgb,width=5)

def arrowV3(draw, r, start, end, rgb = (0,255,0), scale = 200, shift = np.array([1000,1000,0])):
    rgba = rgb + (150,)
    [cx,cy,cz] = start + (end-start) * 0.8 # The base of the arrow.
    c_vec = np.dot(r, np.array([cx,cy,cz])) * scale + shift[:3]
    [ex,ey,ez] = (end - start)
    start = np.dot(r, start) * scale + shift[:3]
    end = np.dot(r, end) * scale + shift[:3]
    d = 0.08
    for y1 in np.arange(-d, d, 0.0002):
        z1 = np.sqrt(d**2-y1**2)
        x1 = 0
        xyz = np.array([x1 + cx, y1 + cy, z1 + cz ])
        xyz = np.dot(r, xyz) * scale + shift[:3]
        draw.line((xyz[0],xyz[1],c_vec[0],c_vec[1]), fill = rgba, width=5)
        draw.line((xyz[0],xyz[1],end[0],end[1]), fill = rgba, width=5)
        z1 = -z1
        xyz = np.array([x1 + cx, y1 + cy, z1 + cz ])
        xyz = np.dot(r, xyz) * scale + shift[:3]
        draw.line((xyz[0],xyz[1],c_vec[0],c_vec[1]), fill = rgba, width=5)
        draw.line((xyz[0],xyz[1],end[0],end[1]), fill = rgba, width=5)
    draw.line((start[0],start[1],end[0],end[1]),fill=rgb,width=5)


'''
Types text onto an image, filling part by part to give the impression of it being typed.
args:
    txt: The text to be typed onto the image.
    im: The image object.
    im_ind: How far in the animation are we?
    pos: The position in the image at which the text is to be typed.
'''
def writeStaggeredText(txt, draw, im_ind, pos = (250,200)):
    font = ImageFont.truetype("arial.ttf", 78)
    draw.text(pos, txt[:min(im_ind*2, len(txt))], (255,255,255), font=font)

