import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageMath


def rotate_axes(ind=0, j=21, scale=200.0, scale2=20.0, shift=np.array([1000.0, 1000.0, 0.0]), base_coeff=0.02, iii = 2.0, sep = 8):
    im = Image.new("RGB", (2048, 2048), (1, 1, 1))
    draw = ImageDraw.Draw(im, 'RGBA')
    r = rot.rotation(3, np.pi/30*j)
    #r = np.eye(3)
    r1 = np.eye(4)
    r1[:3,:3] = r
    drawXYGrid(draw, r, meshLen=1.0, scale=scale, shift=shift)
    render_scene_4d_axis(draw, r1, 4)
    cfn = lambda x, y : 0.0
    fn = lambda x, y : paraboloid(x, y, coeff=iii*base_coeff, intercept=iii)
    #drawFunctionalXYGrid(draw, r, scale=scale2, fn=fn, extent=30, rgba2=(0,255,0,40),
    #            saperatingPlane=np.array([-1,-1,sep]))
    drawFunctionalXYGrid(draw, r, scale=scale2, fn=fn, extent=30)
    decorateAxes(draw, r, extent=5.2, zextent=5.4)
    im_eq0 = Image.open("..\\Images\\temp\\eqn7.png")
    #pasteImage(im_eq0, im, (0,0))
    #angle = int(180*ind/10.0)
    #angle = int(180*ind/20)
    angle = 86 + int((180-86))
    draw_circle_x_y(draw, r, center=np.array([0,0]), radius=np.sqrt(1/base_coeff),
                scale=scale2, arcExtent=180, width=7)
    
    shift1 = np.dot(r, np.array([sep,sep,0.0]))*scale2 + np.array([1000.0, 1000.0, 0.0])
    drawFunctionalXYGrid(draw, r, scale=scale2, fn=fn, shift=shift1, rgba=(202,200,20,150),
                extent=30, rgba2=(202,200,20,40), saperatingPlane=np.array([1,1,sep]))

    draw_circle_x_y(draw, r, center=np.array([0,0]), radius=np.sqrt(1/base_coeff),
                scale=scale2, shift=shift1, arcExtent=180)
    paraboloid_intersection(draw, r, sep, sep, iii*base_coeff, iii, scale=scale2,
                start_line=-12, width=7)

    theta = angle*np.pi*2/180 + np.pi/2
    arrowPt = np.array([np.cos(theta), np.sin(theta), 0])*1.3
    #arrowV1(draw, r, start=np.array([0,0,0]), end=arrowPt, scale=100, rgb=(255,127,80))
    #arrowV1(draw, r, start=np.array([0,0,0]), end=arrowPt, scale=100, rgb=(255,127,80), shift=shift1)
    theta1 = 52.4*np.pi*2/180 + np.pi/2
    arrowPt = np.dot(r, np.array([np.cos(theta1), np.sin(theta1), 0])*1.3)*100*scale2/20.0+shift1[:3]
    w = 9
    draw.ellipse((arrowPt[0]-w,arrowPt[1]-w,arrowPt[0]+w,arrowPt[1]+w), fill = (255,255,102), outline = (0,0,0))
    ############
    theta1 = 83.8*np.pi*2/180 + np.pi/2
    arrowPt = np.dot(r, np.array([np.cos(theta1), np.sin(theta1), 0])*1.39)*100*scale2/20.0+shift1[:3]
    w = 9
    draw.ellipse((arrowPt[0]-w,arrowPt[1]-w,arrowPt[0]+w,arrowPt[1]+w), fill = (255,255,102), outline = (0,0,0))
    #d = -12.0#*np.cos(np.pi*2*ind/10.0)
    d = -12.0
    frac = 6.0/15.0
    pt_orig = d*np.array([np.cos(np.pi*frac), np.sin(np.pi*frac), 0])
    #pt_orig = np.array([24.4405288584,-16.4405288584,0])
    #pt_orig = np.array([14.4404152889,-6.44041528886,0])
    #pt_orig = np.array([9.65122498192,-1.65122498192,0])
    pt = pt_orig
    z1 = iii*base_coeff*(pt[0]**2 + pt[1]**2) - iii
    z2 = iii*base_coeff*((pt[0] - sep)**2 + (pt[1] - sep)**2) - iii
    pt1 = np.array([pt[0],pt[1],z1])
    pt1 = np.dot(r, pt1)*scale2+shift
    pt2 = np.array([pt[0],pt[1],z2])
    pt2 = np.dot(r, pt2)*scale2+shift
    
    pt = np.dot(r, pt)*scale2+shift
    w = 7
    p = 1.0
    pp = pt1*p+pt*(1-p)
    draw.line((pt[0], pt[1], pp[0], pp[1]), fill="white", width=3)
    p = 1.0
    pp = pt2*p+pt1*(1-p)
    
    draw.line((pt[0], pt[1], pp[0], pp[1]), fill="white", width=3)
    #w = 7+ 5*np.sin(np.pi*ind/10.0)
    w = 9
    draw.ellipse((pt1[0]-w, pt1[1]-w, pt1[0]+w, pt1[1]+w), fill = (0,255,120))
    w = 9
    draw.ellipse((pt2[0]-w, pt2[1]-w, pt2[0]+w, pt2[1]+w), fill = (202,200,20))
    
    c = iii*base_coeff
    [x0, y0] = [0, 0]
    [x1, y1] = pt_orig[:2]
    [a1, b1, d1] = [2*c*(x1-x0), 2*c*(y1-y0), c*(x1-x0)**2 + c*(y1-y0)**2 - iii -2*c*(x1-x0)*x1 - 2*c*(y1-y0)*y1]

    [x0_1, y0_1] = [sep, sep]
    [a2, b2, d2] = [2*c*(x1-x0_1), 2*c*(y1-y0_1), c*(x1-x0_1)**2 + c*(y1-y0_1)**2 - iii -2*c*(x1-x0_1)*x1 - 2*c*(y1-y0_1)*y1]

    [line_pt1, line_pt2] = plane_intersection(draw, r, plane1=[a1, b1, d1], plane2=[a2, b2, d2], 
        x_start=pt_orig[0]-7, x_end=pt_orig[0]+7, scale=scale2, shift=shift)
    generalizedParaboloidTangent(draw, r, pt_orig[0], pt_orig[1], d=10.0, x0=0, y0=0,
     c=c, i=iii , scale=20.0, shift=shift, line_pt1=line_pt1, line_pt2=line_pt2, rgba=(153,255,102,150), p=1.0)
    
    generalizedParaboloidTangent(draw, r, pt_orig[0], pt_orig[1], d=10.0, x0=sep, y0=sep,
     c=c, i=iii , scale=20.0, shift=shift, line_pt1=line_pt1, line_pt2=line_pt2, rgba=(255,204,102,150), p=1.0)
    draw.ellipse((pt[0]-w, pt[1]-w, pt[0]+w, pt[1]+w), fill = (255,0,120))
    #im.save("..\\Images\\RotatingCube\\im" + str(ind) + ".png")

    mat = np.array([[a1, b1],[a2, b2]])
    rhs = np.array([-d1, -d2])
    pt_orig2 = np.linalg.solve(mat, rhs)
    pt_orig2 = np.append(pt_orig2, 0)
    print(str(pt_orig2[0])+","+str(pt_orig2[1]))
    ptt = np.dot(r, pt_orig2)*scale2+shift
    d1 = dist(ptt,line_pt1)
    d2 = dist(ptt,line_pt2)
    p = 1.0
    if d1 > d2:
        lll = (1-p)*line_pt1+(p)*ptt
        draw.line((lll[0], lll[1], line_pt1[0], line_pt1[1]),width=6,fill='purple')
    else:
        lll = (1-p)*line_pt2+(p)*ptt
        draw.line((lll[0], lll[1], line_pt2[0], line_pt2[1]),width=6,fill='purple')
    p = 1.0
    pt = ptt*p+pt*(1-p)
    draw.ellipse((pt[0]-w, pt[1]-w, pt[0]+w, pt[1]+w), fill = (255,255,255))
    writeStaggeredText("1) Start at a random point", draw, ind, (250,200))
    ind1 = ind
    ind = 76
    '''
    if ind > 13:
        writeStaggeredText("2) Approximate all equations with linear\n ones at the point", draw, ind-13, (250,270))
    if ind>43:
        writeStaggeredText("3) Solve the linear system and move\n point to solution", draw, ind-43, (250,445))
    if ind>70:
        writeStaggeredText("4) Repeat", draw, ind-70, (250,628))
    ind = ind1
    '''
    im.save("..\\Images\\RotatingCube\\im" + str(ind) + ".png")


def dist(pt1, pt2):
    return (pt2[0]-pt1[0])**2 + (pt2[1]-pt1[1])**2


