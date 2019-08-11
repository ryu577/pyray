import numpy as np
from pyray.shapes.twod.paraboloid import gridSquarePolygon


def drawFunctionalXYGrid(draw, r, shift=np.array([1000.0, 1000.0, 0.0]),
        scale=200.0, rgba=(0,255,0,120), fn=None, extent=10,
        saperatingPlane=np.array([-1,-1,4]), rgba2=None):
    '''
    args:
        saperatingPlane: Take the dot product of this plane with [x,y,1]. If <0, draw lighter planes.
        rgba2: The color of the lighter portion of the plane.
    '''
    for i in range(-extent, extent, 1):
        for j in range(-extent, extent, 1):
            poly = gridSquarePolygon(i, j, r, shift, scale, fn)
            if np.dot(np.array([i, j, 1]), saperatingPlane) > 0 or rgba2 is None:
                draw.polygon(poly, rgba)
            else:
                draw.polygon(poly, rgba2)


def draw_functional_xygrid_in_circle(draw, r, shift=np.array([1000.0, 1000.0, 0.0]),
        scale=200.0, rgba=(0,255,0,120), fn=None, extent=10,
        saperatingPlane=np.array([-1,-1,4]), rgba2=None,radius=10):
    '''
    args:
        saperatingPlane: Take the dot product of this plane with [x,y,1]. If <0, draw lighter planes.
        rgba2: The color of the lighter portion of the plane.
    '''
    for i in range(-extent, extent, 1):
        for j in range(-extent, extent, 1):
            if i**2+j**2 < radius**2:
                poly = gridSquarePolygon(i, j, r, shift, scale, fn)
                if np.dot(np.array([i, j, 1]), saperatingPlane) > 0 or rgba2 is None:
                    draw.polygon(poly, rgba)
                else:
                    draw.polygon(poly, rgba2)



