import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageMath

im = Image.new("RGB", (512,512), "black")
draw = ImageDraw.Draw(im, 'RGBA')


def circle(draw, center = (256,256), r = 50):
    for t in np.arange(0,2*np.pi,0.01):
        pt1 = np.exp(1j*t)*r + (center[0]+1j)+center[1]*(1j)
        pt2 = np.exp(1j*(t+0.01))*r+(center[0]+1j)+center[1]*(1j)
        draw.line((pt1.real,pt1.imag,pt2.real,pt2.imag),fill=(255,0,0))

