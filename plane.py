import numpy as np


def xzplane(draw, r, y, shift = np.array([1000, 1000, 0, 0]), scale = 300):
    """
    Draws an x-z plane on the draw object of an image.
    """
    extent = 2.8
    pln = np.array(
            [
                [-extent,y,0],
                [extent,y,0],
                [extent,y,extent*2],
                [-extent,y,extent*2]
            ]
        )
    pln = np.dot(pln, np.transpose(r))
    pln = pln * scale + shift[:3]
    draw.polygon([(pln[0][0],pln[0][1]),(pln[1][0],pln[1][1]),(pln[2][0],pln[2][1]),(pln[3][0],pln[3][1])], (0,102,255,70))


def xyplane(draw, r, x, shift = np.array([1000, 1000, 0, 0]), scale = 300):
    """
    Draws an x-y plane on the draw object of an image.
    """
    extent = 2.8
    pln = np.array(
            [
                [x,-extent,0],
                [x,extent,0],
                [x,extent,extent*2],
                [x,-extent,extent*2]
            ]
        )
    pln = np.dot(pln,np.transpose(r))
    pln = pln * scale + shift[:3]
    draw.polygon([(pln[0][0],pln[0][1]),(pln[1][0],pln[1][1]),(pln[2][0],pln[2][1]),(pln[3][0],pln[3][1])], (0,102,255,70))


