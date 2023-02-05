import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageMath
from pyray.rotation import planar_rotation
from pyray.shapes.twod.line import Line


class MapCoord(object):
    def __init__(self,scale=64,origin=np.array([8,8]),
                im_size=np.array([1024,1024])):
        """
        See ON//Building//Libraries//TwoD_plotting
        args:
            scale: The scale of the plot.
            origin: The origin in image coordinates.
        """
        self.scale = scale
        self.origin = origin
        self.im_size = im_size
        self.i_h, self.i_y = im_size[0], im_size[1]

    @staticmethod
    def plot_to_im_s(x,y,origin=np.array([8,8]),
                    scale=64,im_size=np.array([1024,1024])):
        ## Assumes no rotation.
        ih = im_size[1]
        x1 = (origin[0]+x)*scale
        y1 = (origin[1]+y)*scale
        return (x1,ih-y1)

    def plot_to_im(self,x,y):
        return MapCoord.plot_to_im_s(x,y,self.origin,
                self.scale,self.im_size)

    @staticmethod
    def im_to_plot_s(x,y,origin=np.array([8,8]),
                    scale=64,im_size=np.array([1024,1024])):
        ih = im_size[1]
        y1 = ih-y
        y2 = y1/scale
        x2 = x/scale
        y3 = y2-origin[1]
        x3 = x2-origin[0]
        return x3,y3

    def im_to_plot(self,x,y):
        return MapCoord.im_to_plot_s(x,y,self.origin,
                self.scale,self.im_size)


class Canvas(object):
    def __init__(self,map_crd,im=None,draw=None):
        self.map_crd=map_crd
        self.plot_ht, self.plot_wdth = map_crd.im_size[0], map_crd.im_size[1]
        if im is None:
            self.im=Image.new("RGB", (self.plot_ht, self.plot_wdth), (0,0,0))
        else:
            self.im=im
        if draw is None:
            self.draw=ImageDraw.Draw(self.im,'RGBA')
        else:
            self.draw=draw        

    @staticmethod
    def draw_grid_s(draw,r=np.eye(2),scale=64,origin=np.array([8,8]),
                    im_size=np.array([1024,1024])):
        lo_range = -scale
        hi_range = im_size[0]+3*scale
        for i in np.arange(lo_range, hi_range, scale):
            pt1 = np.dot(r,np.array([i,lo_range])-origin) + origin
            pt2 = np.dot(r,np.array([i,hi_range])-origin) + origin
            draw.line((pt1[0],pt1[1],pt2[0],pt2[1]),
                        fill=(120,120,120,120), width=2)
        hi_range = im_size[1]+3*scale
        for i in np.arange(lo_range,hi_range,scale):
            pt1 = np.dot(r,np.array([lo_range,i])-origin) + origin
            pt2 = np.dot(r,np.array([hi_range,i])-origin) + origin
            draw.line((pt1[0],pt1[1],pt2[0],pt2[1]), 
                        fill=(120,120,120,120), width=2)

    def draw_grid(self,r=np.eye(2)):
        Canvas.draw_grid_s(self.draw,r,self.map_crd.scale,self.map_crd.origin,
                    self.map_crd.im_size)

    @staticmethod
    def draw_2d_line_s(draw, r, start_pt=np.array([0,0]),
					end_pt=np.array([7,-3]), \
					origin=np.array([4,10]),scale=64, rgba="grey",
					width=2):
        pt1 = np.dot(r,start_pt)*scale + origin*scale
        pt2 = np.dot(r,end_pt)*scale + origin*scale
        draw.line((pt1[0],pt1[1],pt2[0],pt2[1]), fill=rgba, width=width)

    def draw_2d_line(self,start=np.array([0,0]),end=np.array([7,-3]),r=np.eye(2),
                    rgba="grey",width=2):
        Canvas.draw_2d_line_s(self.draw,r,start,end,self.map_crd.origin,
                        self.map_crd.scale, rgba, width)

    @staticmethod    
    def draw_2d_arrow_s(draw, r, start_pt=np.array([0,0]),
                        end_pt=np.array([7,-3]), \
                        origin=np.array([4,10]),scale=64, rgba="grey",
                        width=3):
        pt1 = np.dot(r,start_pt)*scale + origin*scale
        pt2 = np.dot(r,end_pt)*scale + origin*scale
        draw.line((pt1[0],pt1[1],pt2[0],pt2[1]), fill=rgba, width=width)
        vec = (pt2-pt1)
        vec = vec/np.sqrt(sum(vec**2))/2
        r1 = planar_rotation(5*np.pi/4)
        arrow_foot = np.dot(r1,vec)*scale + pt2
        draw.line((arrow_foot[0],arrow_foot[1],pt2[0],pt2[1]), fill=rgba, width=width)
        r1 = planar_rotation(3*np.pi/4)
        arrow_foot = np.dot(r1,vec)*scale + pt2
        draw.line((arrow_foot[0],arrow_foot[1],pt2[0],pt2[1]), fill=rgba, width=width)

    def draw_2d_arrow(self,start,end,rgba='grey',r=np.eye(2)):
        Canvas.draw_2d_arrow_s(self.draw,r,start,end,self.map_crd.origin,self.map_crd.scale,rgba)

    @staticmethod
    def draw_point_s(draw, pos=np.array([-1,1]),origin=np.array([4,4]),scale=64,r=np.eye(2),
                    im_size=np.array([512,512])):
        pt = MapCoord.plot_to_im_s(pos[0],pos[1],origin,scale,im_size)
        draw.ellipse((pt[0]-8, pt[1]-8, pt[0]+8, pt[1]+8), 
            fill = (255,25,25,250), outline = (0,0,0))

    def draw_point(self,pos,fill=(255,25,25,250),size=8):
        #Canvas.draw_point_s(self.draw,pos,self.map_crd.origin,
        #                self.map_crd.scale,np.eye(2),self.map_crd.im_size)
        pt = self.map_crd.plot_to_im(pos[0],pos[1])
        self.draw.ellipse((pt[0]-size, pt[1]-size, pt[0]+size, pt[1]+size), 
            fill = fill, outline = (0,0,0))

    def draw_line(self,pt1,pt2,fill=(255,25,25,250),width=4):
        pt1 = self.map_crd.plot_to_im(pt1[0],pt1[1])
        pt2 = self.map_crd.plot_to_im(pt2[0],pt2[1])
        self.draw.line((pt1[0],pt1[1],pt2[0],pt2[1]),fill=fill,width=width)    

    def draw_arrow(self,pt1,pt2,fill=(255,25,25,250),width=4,
                    arr_bk=.8,arr_per=.2):
        self.draw_line(pt1,pt2,fill=fill,width=width)
        l = Line(pt1,pt2)
        go_back = pt2*arr_bk+pt1*(1-arr_bk)
        arr_hd_1 = go_back+l.w*arr_per
        arr_hd_2 = go_back-l.w*arr_per
        self.draw_line(arr_hd_1,pt2,fill=fill,width=width)
        self.draw_line(arr_hd_2,pt2,fill=fill,width=width)

    def write_txt(self,pos,txt,rgba,size=18):
        font = ImageFont.truetype("Arial.ttf", size)
        pos1 = MapCoord.plot_to_im_s(pos[0],pos[1],self.map_crd.origin,scale=64,
                im_size=self.map_crd.im_size)
        self.draw.text(pos1,txt,rgba,font=font)


def draw_2d_arrow(draw,start,end,rgba='grey',r=np.eye(2)):
    return Canvas.draw_2d_arrow_s(draw, start, end, rgba)

def tst_2d_plot():
    mc = MapCoord(im_size=np.array([512,512]),origin=np.array([4,4]))
    cnv = Canvas(mc)
    cnv.draw_grid()
    cnv.draw_2d_arrow(np.array([-4,0]), np.array([4,0]))
    cnv.draw_2d_arrow(np.array([0,4]), np.array([0,-4]))
    cnv.draw_2d_line(np.array([-4,-4]),np.array([4,4]),rgba="purple")
    cnv.draw_2d_line(np.array([4,-4]),np.array([-4,4]),rgba="yellow")
    cnv.draw_point(np.array([-1,-1]))
    cnv.draw_point(np.array([1,1]),fill="green")
    cnv.write_txt((1,1),"(1,1)","green")
    cnv.write_txt((-1,-1),"(-1,-1)","red")
    basedir = '.\\images\\RotatingCube\\'
    cnv.im.save(basedir + "im" + str(1) + ".png")


