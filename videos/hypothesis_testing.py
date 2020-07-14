import numpy as np
from scipy.stats import norm
from pyray.shapes.oned.curve import *
from pyray.axes import draw_2d_arrow
from pyray.misc import zigzag2

def draw_trtmt_hist(draw,h1=100,h2=100):
    font = ImageFont.truetype("arial.ttf", 10)    
    ##First container
    draw.line((40,150,40,170))
    draw.line((40,170,60,170))
    draw.line((60,170,60,150))
    
    draw.polygon([(41,169),(59,169),(59,169-h1),(41,169-h1)],\
        fill=(255,190,25))
    
    draw.text((39,180), "Trtmt", (255,255,255), font=font)
    
    apart=35
    ##Second container
    draw.line((40+apart,150,40+apart,170))
    draw.line((40+apart,170,60+apart,170))
    draw.line((60+apart,170,60+apart,150))

    draw.text((39+apart,180), "Ctrl", (255,255,255), font=font)

    draw.polygon([(41+apart,169),(59+apart,169),(59+apart,169-h2),(41+apart,169-h2)],\
        fill=(255,190,25))

def draw_gauss(ix=0,extrema=500,std=50,h1=60,h2=0,twosided=False):
    im = Image.new("RGB", (512,512), "black")
    draw = ImageDraw.Draw(im, 'RGBA')
    fn = lambda x:300-norm.pdf(x-250,0,std)*7000
    draw_curve(fn,draw)
    draw.line((250,0,250,512),fill=(0,120,230),width=1)
    x1 = 250+0.8*std
    draw.line((x1,0,x1,512),fill=(255,20,147))
    y1 = fn(x1)
    pts = [(x1,y1),(x1,300),(extrema,fn(extrema))]
    for xx in np.arange(extrema-1,x1,-1):
        yx = fn(xx)
        pts.append((xx,yx))
    draw.polygon(pts,(255,20,147,100))
    if twosided:
        x1 = 250-std
        draw.line((x1,0,x1,512),fill=(255,20,147))
        y1 = fn(x1)
        extrema = 250-(extrema-250)
        pts = [(x1,y1),(x1,300),(extrema,fn(extrema))]
        for xx in np.arange(extrema+1,x1,1):
            yx = fn(xx)
            pts.append((xx,yx))
        draw.polygon(pts,(255,20,147,100))
    pt=np.array([266,300])
    draw.ellipse((pt[0]-2, pt[1]-2, pt[0]+2, pt[1]+2), fill = (0,255,0))
    draw_trtmt_hist(draw,h1=h1,h2=h2)
    im.save(basedir + 'im' + str(ix) + '.png')


def draw_two_gauss(ix=0,extrema=500,std=50,h1=0,h2=0,gap=50,
                    alpha=0.15865525393145707):
    im = Image.new("RGB", (512,512), "black")
    draw = ImageDraw.Draw(im, 'RGBA')
    fn = lambda x:300-norm.pdf(x-250,0,std)*7000
    draw_curve(fn,draw)
    fn2 = lambda x:300-norm.pdf(x-250,gap,std)*7000
    draw_curve(fn2,draw,rgba=(138,43,226))
    #draw.line((250,0,250,512),fill=(0,120,230),width=1)
    #draw.line((250,0,250,512),fill=(255,255,0),width=1)
    delta = norm.isf(alpha,0,std)
    x1 = 250+delta
    draw.line((x1,0,x1,512),fill=(255,20,147,150),width=1)
    y1 = fn(x1)
    pts = [(x1,y1),(x1,300),(extrema,fn(extrema))]
    for xx in np.arange(extrema-1,x1,-1):
        yx = fn(xx)
        pts.append((xx,yx))
    draw.polygon(pts,(255,255,0,100))
    y2=fn2(x1)
    pts = [(x1,y2),(x1,300),(180,fn2(180))]
    for xx in np.arange(179+1,x1,1):
        yx = fn2(xx)
        pts.append((xx,yx))
    draw.polygon(pts,(138,43,226,100))
    draw_trtmt_hist(draw,h1=h1,h2=h2)
    draw_alpha_beta_curve(draw,alpha,std=std,effect=gap)
    im.save(basedir + 'im' + str(ix) + '.png')


def draw_two_gauss_white(ix=0,extrema=500,std=50,h1=0,h2=0,gap=50,
                    alpha=0.15865525393145707):
    im = Image.new("RGB", (512,512), "white")
    draw = ImageDraw.Draw(im, 'RGBA')
    fn = lambda x:300-norm.pdf(x-250,0,std)*7000
    draw_curve(fn,draw,rgba=(0,0,255))
    fn2 = lambda x:300-norm.pdf(x-250,gap,std)*7000
    draw_curve(fn2,draw,rgba=(0,255,0))
    delta = norm.isf(alpha,0,std)
    x1 = 250+delta
    draw.line((x1,0,x1,512),fill=(255,0,0,150),width=1)
    y1 = fn(x1)
    pts = [(x1,y1),(x1,300),(extrema,fn(extrema))]
    for xx in np.arange(extrema-1,x1,-1):
        yx = fn(xx)
        pts.append((xx,yx))
    draw.polygon(pts,(0,0,255,100))
    y2=fn2(x1)
    pts = [(x1,y2),(x1,300),(180,fn2(180))]
    for xx in np.arange(179+1,x1,1):
        yx = fn2(xx)
        pts.append((xx,yx))
    draw.polygon(pts,(0,255,0,100))
    draw_trtmt_hist(draw,h1=h1,h2=h2)
    draw_alpha_beta_curve(draw,alpha,std=std,effect=gap)
    im.save(basedir + 'im' + str(ix) + '.png')


def draw_alpha_beta_curve(draw,alpha=0.15865525393145707,effect=50,std=50):
    font = ImageFont.truetype("arial.ttf", 12)
    draw.line((26,332,26,332+150),fill=(138,43,226))
    draw.line((26,332+150,26+150,332+150),fill=(255,255,0))
    pt1 = np.array([26,332]); moving_beta=1.0
    for alp in np.arange(0.05,1.05,0.05):
        moving_beta = betafn(alp,effect,std)
        x1 = 26+alp*150; y1=332+(1-moving_beta)*150
        draw.line((pt1[0],pt1[1],x1,y1))
        pt1 = np.array([x1,y1])
    beta = betafn(alpha,effect,std)
    x1 = 26+alpha*150; y1 = 332+(1-beta)*150
    draw.ellipse((x1-3,y1-3,x1+3,y1+3),outline=(255,20,147),fill=(255,20,147,150))
    draw.line((x1,y1,26,y1),fill=(255,255,0))
    draw.line((x1,y1,x1,332+150),fill=(138,43,226))
    draw.text((134-40,335),"alpha= "+str(round(alpha,2)), (255,255,0), font=font)
    draw.text((134-40,335+20),"beta= "+str(round(beta,2)), (138,43,226), font=font)
    x1,y1=50,464
    #draw.ellipse((x1-3,y1-3,x1+3,y1+3),outline=(20,200,35),fill=(20,200,35,150))

def betafn(alpha,effect,std):
    return norm.cdf(-effect+norm.isf(alpha,0,std),0,std)


def draw_worst_test(ix=0,extrema=500,std=50,h1=0,h2=0,gap=50,
                    alpha=0.15865525393145707):
    im = Image.new("RGB", (512,512), "black")
    draw = ImageDraw.Draw(im, 'RGBA')
    draw_trtmt_hist(draw,h1=h1,h2=h2)
    draw_alpha_beta_curve(draw,alpha,std=std,effect=gap)
    draw.line((26,332,26,332+150),fill=(138,43,226))
    im.save(basedir + 'im' + str(ix) + '.png')



basedir = '.\\images\\RotatingCube\\'

'''
Scene 1
'''
for i in range(26):
    draw_gauss(i,std=np.sqrt(300+2200*5/(i+5)),h1=2*i,h2=0)


'''
Scene 2
'''
for i in range(26):
    draw_gauss(i,std=np.sqrt(300*3/(i+3)+2200*5/(25+i)),h1=50,h2=2*i)


'''
Scene 3
'''
for i in range(12):
    draw_gauss(i,std=np.sqrt(300/(26+2*i)+2200/(26+2*i)),h1=50+4*i,h2=50+4*i)


'''
Scene 4
'''
for i in range(20):
    alpha = zigzag2(i/10.11,.158655,0.95,0.01)
    draw_two_gauss(ix=i,gap=80,alpha=alpha)

'''
Scene 5
'''
for i in range(20):
    draw_two_gauss(ix=i,gap=80,std=2500/(50+i),\
        h1=2*i,h2=2*i)


'''
Scene 6
'''
for i in range(20):
    draw_worst_test(ix=i,gap=80,std=2500/(50+i),\
        h1=2*i,h2=2*i)



