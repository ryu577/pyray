
import numpy as np
import colorsys


def colorFromAngle(angle):
    """
    Converts numbers into colors for shading effects.
    """
    return (int(230*(angle/450)), int(230*(angle/450)), 250)


def colorFromAngle2(angle, h=136, s=118, maxx = 0.8):
    """
    Converts simple numbers into colors using HSL color scale. This can be used to shade surfaces more exposed to light brighter.
    args:
        angle: Higher values of this argument correspond to brighter colors. If a plane of a polyhedron makes a large angle with a light source,
                it will look brighter.
    """
    l = 96+64*angle/maxx #/450
    r, g, b = colorsys.hls_to_rgb(h/255.0, l/255.0, s/255.0)
    r, g, b = [x*255.0 for x in (r, g, b)]
    return (int(r),int(g),int(b))
