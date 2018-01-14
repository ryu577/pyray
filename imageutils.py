import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import sympy

try:
    xrange          # Python 2
except NameError:
    xrange = range  # Python 3


def writeLatex(im, lat, coordn = (50,50), color = (120,80,200), flip_im = False):
    """
    Given an image and pair of coordinates, writes out a Math equation at said coordinates.
    Tools taken from - https://stackoverflow.com/questions/1381741/converting-latex-code-to-images-or-other-displayble-format-with-python
    args:
        lat: The equation as a latex string. For example, '\\sin{\\left (\\sqrt{ \\frac{x^{2}}{y} + 20} \\right )} + 1'
    """
    lst = list(coordn)
    lst[0] = lst[0] - 139 + 50
    lst[1] = lst[1] - 475 + 50
    coordn = tuple(lst)
    fig, ax = plt.subplots()
    fig.patch.set_visible(False)
    ax.axis('off')
    lst = np.array(list(color))
    lst = lst / 255.0
    color = tuple(lst)
    plt.text(0, 0, r"$%s$" % lat, fontsize = 70, color = color)
    #fig = plt.gca()
    #fig.axes.get_xaxis().set_visible(False)
    #fig.axes.get_yaxis().set_visible(False)
    plt.savefig(".\\Images\\Math\\temp.png")
    im_math = Image.open(".\\Images\\Math\\temp.png")
    #coordn = (coordn[0] - im_math.size[0]/2.0, coordn[1] - im_math.size[1]/2.0)
    pasteImage(im_math,im,coordn,True)
    plt.close()


def pasteImage(img, bigim, posn, whiteBackground = False, color = None):
    """
    Pastes a small image onto a bigger image at the coordinates specified by posn.
    """
    pixdata = img.load()
    width, height = img.size
    bw,bh = bigim.size
    mainpixdata = bigim.load()
    for y in xrange(height):
        for x in xrange(width):
            if x < bw - posn[0] and y < bh - posn[1] and x + posn[0] > 0 and y + posn[1] > 0:
                if sum(pixdata[x, y][:3]) != 0 and not (whiteBackground and sum(pixdata[x, y][:3]) == 255 * 3):
                    if color is None:
                        mainpixdata[x+posn[0], y+posn[1]] = pixdata[x,y]
                    else:
                        mainpixdata[x+posn[0], y+posn[1]] = color

