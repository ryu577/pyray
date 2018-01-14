
import numpy as np
import colorsys


'''
Converts numbers into colors for shading effects.
'''
def colorFromAngle(angle):
    return (int(230*(angle/450)), int(230*(angle/450)), 250)

'''
Converts simple numbers into colors using HSL color scale. This can be used to shade surfaces more exposed to light brighter.
'''
def colorFromAngle2(angle, h=136, s=118, maxx = 0.8):
    l = 96+64*angle/maxx #/450
    r, g, b = colorsys.hls_to_rgb(h/255.0, l/255.0, s/255.0)
    r, g, b = [x*255.0 for x in (r, g, b)]
    return (int(r),int(g),int(b))
