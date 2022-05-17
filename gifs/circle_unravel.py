import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageMath
import os


basedir = '.\\Images\\RotatingCube\\'
font_loc = "arial.ttf"
if os.name == 'posix':
    basedir = 'Images/RotatingCube/'
    font_loc = 'Arial.ttf'


def circle(draw, center = (256,256), r=50, frac=1.0, start_angle=0):
    for t in np.arange(start_angle, start_angle-2*np.pi*frac+0.01, -0.01):
        pt1 = np.exp(-1j*t)*r + (center[0]+1j)+center[1]*(1j)
        pt2 = np.exp(-1j*(t+0.01))*r+(center[0]+1j)+center[1]*(1j)
        draw.line((pt1.real, pt1.imag, pt2.real, pt2.imag), fill=(255,0,0))


## scene-1
r=30
center_o = np.array([256,256])
base_pt = center_o + np.array([0,r])
for ix in range(11):
    im = Image.new("RGB", (512,512), "black")
    draw = ImageDraw.Draw(im, 'RGBA')
    t = np.pi*2*ix/10
    center = center_o + np.array([t*r,r])
    circle(draw, center, r, 1-t/2/np.pi, np.pi/2)
    pt2 = center-np.array([0,r])
    draw.line((base_pt[0],base_pt[1]-r, center[0], center[1]-r), fill=(255,0,0))
    pt = center_o
    draw.ellipse((pt[0]-4, pt[1]-4, pt[0]+4, pt[1]+4), fill = (255,255,0,150), outline = (0,0,0))
    im.save(basedir + 'im' + str(10-ix) + '.png')


## scene-2
r = 30
center_o = np.array([256,256])
for ix in range(10):
    im = Image.new("RGB", (512,512), "black")
    draw = ImageDraw.Draw(im, 'RGBA')
    circle(draw, center, r, 1, np.pi/2)
    center = center_o
    t = np.sin(ix*np.pi/20.0+3*np.pi/2)
    pt1 = np.exp(-1j*t)*r + (center[0]+1j)+center[1]*(1j)
    pt = (pt1.real, pt1.imag)
    draw.ellipse((pt[0]-4, pt[1]-4, pt[0]+4, pt[1]+4), fill = (255,255,0,150), outline = (0,0,0))
    draw.line((center[0]-35,center[1]+r,center[0]+35,center[1]+r),fill=(255,255,0),width=1)
    im.save(basedir + 'im' + str(ix) + '.png')




## scene-3
r = 30
center_o = np.array([256,256])
for ix in range(6):
    im = Image.new("RGB", (512,512), "black")
    draw = ImageDraw.Draw(im, 'RGBA')
    circle(draw, center, r, 1, np.pi/2)
    center = center_o
    t = np.sin(ix*np.pi/20.0+3*np.pi/2)
    pt1 = np.exp(-1j*t)*r + (center[0]+1j)+center[1]*(1j)
    pt = (pt1.real, pt1.imag)
    #draw.ellipse((pt[0]-4, pt[1]-4, pt[0]+4, pt[1]+4), fill = (255,255,0,150), outline = (0,0,0))
    #draw.line((center[0]-35,center[1]+r,center[0]+35,center[1]+r),fill=(255,255,0),width=1)
    font = ImageFont.truetype("arial.ttf", 14)
    draw.text((256,180), "First, generate (n+1) points on the circle.", (255,255,255), font=font)
    im.save(basedir + 'im' + str(ix) + '.png')


def draw_pt(t, draw, fill1=(255,255,0,150)):
    pt1 = np.exp(-1j*t)*r + (center[0]+1j)+center[1]*(1j)
    pt = (pt1.real, pt1.imag)
    draw.ellipse((pt[0]-4, pt[1]-4, pt[0]+4, pt[1]+4), fill = fill1, outline = (0,0,0))
    return pt

ts = []
for i in range(4):
    tt = np.random.uniform()*np.pi*2
    ts.append(tt)

for ix1 in range(3):
    im = Image.new("RGB", (512,512), "black")
    draw = ImageDraw.Draw(im, 'RGBA')
    circle(draw, center, r, 1, np.pi/2)
    center = center_o
    font = ImageFont.truetype("arial.ttf", 14)
    draw.text((256,180), "First, generate (n+1) points on the circle.", (255,255,255), font=font)
    for t in ts:
        draw_pt(t, draw)
    im.save(basedir + 'im' + str(ix+ix1) + '.png')

stat_pt = 0
for ix2 in range(8):
    im = Image.new("RGB", (512,512), "black")
    draw = ImageDraw.Draw(im, 'RGBA')
    circle(draw, center, r, 1, np.pi/2)
    center = center_o
    font = ImageFont.truetype("arial.ttf", 14)
    draw.text((256,180), "Mark one of them green.", (255,255,255), font=font)
    for t in ts:
        if t == ts[stat_pt]:
            draw_pt(t, draw, fill1="green")
        else:
            draw_pt(t, draw)
    im.save(basedir + 'im' + str(ix+ix1+ix2) + '.png')

ts = np.array(ts)
for ix3 in range(5):
    ts = ts + (np.pi/2-ts[stat_pt])*ix3/4
    im = Image.new("RGB", (512,512), "black")
    draw = ImageDraw.Draw(im, 'RGBA')
    circle(draw, center, r, 1, np.pi/2)
    center = center_o
    font = ImageFont.truetype("arial.ttf", 14)
    draw.text((256,180), "Rotate to align green point with horizon.", (255,255,255), font=font)
    for t in ts:
        if t == ts[stat_pt]:
            draw_pt(t, draw, fill1="green")
        else:
            draw_pt(t, draw)
    im.save(basedir + 'im' + str(ix+ix1+ix2+ix3) + '.png')


# scene-4
r=30
center_o = np.array([256,256])
base_pt = center_o + np.array([0,r])
bools = np.zeros(len(ts))
pts = [(0,0),(0,0),(0,0),(0,0)]
for ix in range(11):
    im = Image.new("RGB", (512,512), "black")
    draw = ImageDraw.Draw(im, 'RGBA')
    t = np.pi*2*ix/10
    center = center_o + np.array([t*r,r])
    circle(draw, center, r, 1-t/2/np.pi, np.pi/2)
    pt2 = center-np.array([0,r])
    draw.line((base_pt[0],base_pt[1]-r, center[0], center[1]-r), fill=(255,0,0))
    pt = center_o
    ts1 = ts+t
    ixx = 0
    for tt in ts1:
        if bools[ixx] == 0:
            if ixx == stat_pt:
                pt = draw_pt(tt, draw, fill1="green")
            else:
                pt = draw_pt(tt, draw)
        if abs(tt%(np.pi*2) - np.pi/2)<0.36 and pts[ixx][0]==0:
            bools[ixx] = 1
            pts[ixx] = pt
        for pt1 in pts:
            draw.ellipse((pt1[0]-4, pt1[1]-4, pt1[0]+4, pt1[1]+4), fill = "yellow", outline = (0,0,0))
        ixx+=1
    im.save(basedir + 'im' + str(ix) + '.png')

