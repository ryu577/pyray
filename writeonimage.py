import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import sympy


'''
Given an image and pair of coordinates, writes out a Math equation at said coordinates.
Tools taken from - https://stackoverflow.com/questions/1381741/converting-latex-code-to-images-or-other-displayble-format-with-python
args:
    lat: The equation as a latex string. For example, '\\sin{\\left (\\sqrt{ \\frac{x^{2}}{y} + 20} \\right )} + 1'
'''
def writeLatex(im, lat, coordn = (50,50), color = (120,80,200), flip_im = False):
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
