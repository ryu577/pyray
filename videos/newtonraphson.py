from functions.functionalforms import *
from rotation.rotation import *
from utils.imageutils import *
from PIL import Image, ImageDraw, ImageFont, ImageMath
import numpy as np

def create_2d_scene(scale=200.0,ind=0, base_ind=0, x0=-3.05):
    im = Image.new("RGB", (2048, 2048), (1, 1, 1))
    draw = ImageDraw.Draw(im, 'RGBA')
    base_coeff = 0.02
    i=2.0
    shift=np.array([1000.0, 1000.0, 0.0])
    fn = lambda x, y : paraboloid(x, y, coeff=i*base_coeff, intercept=i)
    cfn = lambda x, y : 0.0
    r = np.eye(3)
    #drawFunctionalXYGrid(draw, r, scale=scale, fn=fn, extent=30, rgba2=(0,255,0,40))
    r1 = np.eye(4)
    r1[:3,:3] = r
    pt1 = np.array([0,2,0])
    pt1 = np.dot(r,pt1)*scale+shift[:3]
    pt2 = np.array([1,0,0])
    pt2 = np.dot(r,pt2)*scale+shift[:3]
    p=5.0
    pt3 = p*pt1+(1-p)*pt2
    ind1 = 10
    p=5.0*(-ind1/10.0+1)
    pt4 = p*pt1+(1-p)*pt2
    p=ind/10.0
    p=1.0
    #draw.line((pt3[0], pt3[1], pt4[0], pt4[1]), fill=(0,153,255), width=5)    
    mix_draw(draw, p, scale, shift, x_max=1.0+6.0*10.0/10.0)
    #Iterations: [-2, -3.5]
    y0 = draw_fns(x0, p)
    #xax = y0/(2*x0+2)+x0
    xax = y0/(x0*np.cos(2*x0)+np.sin(2*x0)/2+np.exp(x0)/5.0)+x0
    parpt = np.dot(r, np.array([x0, y0, 0]))*scale+shift[:3]
    xaxpt = np.dot(r, np.array([xax, 0, 0]))*scale+shift[:3]
    parpt2 = np.dot(r, np.array([xax, draw_fns(xax, p), 0]))*scale+shift[:3]
    p2 = 10.0/10.0
    parpt2 = p2*parpt2 + (1-p2)*xaxpt
    ### White vertical line, controlloed by p2.
    #draw.line((xaxpt[0],xaxpt[1],parpt2[0],parpt2[1]), fill='white', width=5)
    p1 = 3.0/3.0
    xaxpt = xaxpt *p1 + parpt * (1-p1)
    ### Red tangent line controlled by p1.
    draw.line((parpt[0], parpt[1], xaxpt[0], xaxpt[1]), fill='red', width=5)
    p3 = 0.0/3.0
    parpt = parpt2*p3+parpt*(1-p3)
    draw.ellipse((parpt[0]-8, parpt[1]-8, parpt[0]+8, parpt[1]+8), fill = (255,255,102), outline = (0,0,0))
    w = 7
    #draw.ellipse((xaxpt[0]-w, xaxpt[1]-w, xaxpt[0]+w, xaxpt[1]+w), fill = (255,255,255), outline = (0,0,0))
    #removeImagePortion(im, 1000-ind*100,1000+ind*100,1000-ind*100,1000+ind*100)
    font = ImageFont.truetype("arial.ttf", 300-ind1*10)
    #draw.text((273-ind1*24,380-ind1*30), "y = 2x -2", (255,255,255), font=font)
    im_eq0 = Image.open("..\\images\\temp\\eqn4.png")
    im_eq1 = Image.open("..\\images\\temp\\eqn5.png")
    
    #pasteImage(im_eq1, im, (0,0), img2=im_eq0, p=p)
    w=9*(1+0.5*np.sin(np.pi*2*ind/5.0))
    w=9*1.2
    #draw.ellipse((pt4[0]-w,pt4[1]-w,pt4[0]+w,pt4[1]+w), fill = (255,255,102), outline = (0,0,0))
    font = ImageFont.truetype("arial.ttf", 70)
    #draw.text((1237,870), "x = 1, y = 0", (255,255,102), font=font)
    drawXYGrid(draw, r, meshLen=1.0, scale=scale, shift=shift)
    render_scene_4d_axis(draw, r1, 4)
    im.save("..\\images\\RotatingCube\\im" + str(ind+base_ind) + ".png")


def rotate_axes(ind=0, j=21, scale=200.0, shift=np.array([1000.0, 1000.0, 0.0]), base_coeff=0.02, iii = 2.0, sep = 8):
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
    drawFunctionalXYGrid(draw, r, scale=20, fn=fn, extent=30, rgba2=(0,255,0,40),
                saperatingPlane=np.array([-1,-1,sep]))
    decorateAxes(draw, r, extent=5.2, zextent=5.4)
    im_eq0 = Image.open("..\\images\\temp\\eqn7.png")
    #pasteImage(im_eq0, im, (0,0))
    #angle = int(180*ind/10.0)
    #angle = int(180*ind/20)
    angle = 86 + int((180-86))
    draw_circle_x_y(draw, r, center=np.array([0,0]), radius=np.sqrt(1/base_coeff),
                scale=20, arcExtent=180, width=7)
    
    shift1 = np.dot(r, np.array([sep,sep,0.0]))*20.0 + np.array([1000.0, 1000.0, 0.0])
    drawFunctionalXYGrid(draw, r, scale=20, fn=fn, shift=shift1, rgba=(202,200,20,150),
                extent=30, rgba2=(202,200,20,40), saperatingPlane=np.array([1,1,sep]))

    draw_circle_x_y(draw, r, center=np.array([0,0]), radius=np.sqrt(1/base_coeff),
                scale=20, shift=shift1, arcExtent=180)
    paraboloid_intersection(draw, r, sep, sep, iii*base_coeff, iii, scale=20,
                start_line=-12, width=7)

    theta = angle*np.pi*2/180 + np.pi/2
    arrowPt = np.array([np.cos(theta), np.sin(theta), 0])*1.3
    #arrowV1(draw, r, start=np.array([0,0,0]), end=arrowPt, scale=100, rgb=(255,127,80))
    #arrowV1(draw, r, start=np.array([0,0,0]), end=arrowPt, scale=100, rgb=(255,127,80), shift=shift1)
    theta1 = 52.4*np.pi*2/180 + np.pi/2
    arrowPt = np.dot(r, np.array([np.cos(theta1), np.sin(theta1), 0])*1.3)*100+shift1[:3]
    w = 9
    draw.ellipse((arrowPt[0]-w,arrowPt[1]-w,arrowPt[0]+w,arrowPt[1]+w), fill = (255,255,102), outline = (0,0,0))
    theta1 = 86*np.pi*2/180 + np.pi/2
    arrowPt = np.dot(r, np.array([np.cos(theta1), np.sin(theta1), 0])*1.3)*100+shift1[:3]
    w = 9
    draw.ellipse((arrowPt[0]-w,arrowPt[1]-w,arrowPt[0]+w,arrowPt[1]+w), fill = (255,255,102), outline = (0,0,0))
    #d = -12.0#*np.cos(np.pi*2*ind/10.0)
    d = -12.0
    frac = 6.0/15.0
    pt_orig = d*np.array([np.cos(np.pi*frac), np.sin(np.pi*frac), 0])
    pt = pt_orig
    z1 = iii*base_coeff*(pt[0]**2 + pt[1]**2) - iii
    z2 = iii*base_coeff*((pt[0] - sep)**2 + (pt[1] - sep)**2) - iii
    pt1 = np.array([pt[0],pt[1],z1])
    pt1 = np.dot(r, pt1)*20.0+shift
    pt2 = np.array([pt[0],pt[1],z2])
    pt2 = np.dot(r, pt2)*20.0+shift
    
    pt = np.dot(r, pt)*20.0+shift
    w = 7
    draw.ellipse((pt[0]-w, pt[1]-w, pt[0]+w, pt[1]+w), fill = (255,0,120))
    p = 1.0
    pp = pt1*p+pt*(1-p)
    draw.line((pt[0], pt[1], pp[0], pp[1]), fill="white", width=3)
    w = 7+ 5*np.sin(np.pi*ind/10.0)
    draw.ellipse((pt1[0]-w, pt1[1]-w, pt1[0]+w, pt1[1]+w), fill = (0,255,120))
    #draw.ellipse((pt2[0]-5, pt2[1]-5, pt2[0]+5, pt2[1]+5), fill = (202,200,20))

    c = iii*base_coeff
    [x0, y0] = [0, 0]
    [x1, y1] = pt_orig[:2]
    [a1, b1, d1] = [2*c*(x1-x0), 2*c*(y1-y0), c*(x1-x0)**2 + c*(y1-y0)**2 - i -2*c*(x1-x0)*x1 - 2*c*(y1-y0)*y1]

    [x0_1, y0_1] = [sep, sep]
    [a2, b2, d2] = [2*c*(x1-x0_1), 2*c*(y1-y0_1), c*(x1-x0_1)**2 + c*(y1-y0_1)**2 - i -2*c*(x1-x0_1)*x1 - 2*c*(y1-y0_1)*y1]

    #[line_pt1, line_pt2] = plane_intersection(draw, r, plane1=[a1, b1, d1], plane2=[a2, b2, d2], 
    #    x_start=pt_orig[0]-7, x_end=pt_orig[0]+7, scale=20.0, shift=shift)
    
    #generalizedParaboloidTangent(draw, r, pt_orig[0], pt_orig[1], d=10.0, x0=0, y0=0,
    # c=c, i=iii , scale=20.0, shift=shift, line_pt1=line_pt1, line_pt2=line_pt2, rgba=(153,255,102,150), p=ind/10.0)
    
    #generalizedParaboloidTangent(draw, r, pt_orig[0], pt_orig[1], d=10.0, x0=sep, y0=sep,
    # c=c, i=iii , scale=20.0, shift=shift, line_pt1=line_pt1, line_pt2=line_pt2, rgba=(255,204,102,150), p=ind/10.0)
    im.save("..\\images\\RotatingCube\\im" + str(ind) + ".png")


def draw_fns(x, p):
    #return -(2*x-2)*(1-p)-(x-1)*(x+3)*p
    #return -(x-1)*(x+3)*(1-p)-(x-1)*(x+3)*(x+5)*0.2*p
    #return -(x-1)*(x+3)*(x+5)*0.2*(1-p)-(2**x-2)*p
    #return -(2**x-2)*(1-p)-(x-1)*(x+3)*p
    return -(x-1)*(x+3)*(1-p)-(x/2*np.sin(2*x)+np.exp(x)/5)*p


def mix_draw(draw, p, scale, shift, x_max=1.0):
    x=-7
    pt1 = np.array([x, draw_fns(x,p),0])*scale+shift[:3]
    while x<=x_max:
        x+=0.1
        pt2 = np.array([x, draw_fns(x,p),0])*scale+shift[:3]
        draw.line((pt1[0], pt1[1], pt2[0], pt2[1]), fill=(0,153,255), width=5)
        pt1=pt2


def tst():
    ind1 = 10
    im = Image.new("RGB", (2048, 2048), (1, 1, 1))
    draw = ImageDraw.Draw(im, 'RGBA')
    font = ImageFont.truetype("arial.ttf", 200)
    draw.text((273-ind1*24,380-ind1*30), "y = sin(x-1)", (255,255,255), font=font)
    im.save("..\\images\\RotatingCube\\im" + str(160) + ".png")



