import matplotlib.pyplot as plt
import numpy as np
import sympy
from PIL import Image

try:
    xrange  # Python 2
except NameError:
    xrange = range  # Python 3


def writeLatex(im, lat, coordn=(50, 50), color=(120, 80, 200), flip_im=False):
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
    ax.axis("off")
    lst = np.array(list(color))
    lst = lst / 255.0
    color = tuple(lst)
    plt.text(0, 0, r"$%s$" % lat, fontsize=70, color=color)
    # fig = plt.gca()
    # fig.axes.get_xaxis().set_visible(False)
    # fig.axes.get_yaxis().set_visible(False)
    plt.savefig(".\\Images\\Math\\temp.png")
    im_math = Image.open(".\\Images\\Math\\temp.png")
    # coordn = (coordn[0] - im_math.size[0]/2.0, coordn[1] - im_math.size[1]/2.0)
    pasteImage(im_math, im, coordn, True)
    plt.close()


def pasteImage(img, bigim, posn, whiteBackground=False, color=None, p=1.0, img2=None):
    """
    Pastes a small image onto a bigger image at the coordinates specified by posn.
    """
    pixdata = img.load()
    if img2 is not None:
        pixdata2 = img2.load()
    width, height = img.size
    bw, bh = bigim.size
    mainpixdata = bigim.load()
    for y in xrange(height):
        for x in xrange(width):
            if (
                x < bw - posn[0]
                and y < bh - posn[1]
                and x + posn[0] > 0
                and y + posn[1] > 0
            ):
                ss = 0
                if img2 is not None:
                    ss = sum(pixdata[x, y][:3]) + sum(pixdata2[x, y][:3])
                else:
                    ss = sum(pixdata[x, y][:3])
                if (
                    ss != 0
                ):  # and not (whiteBackground and sum(pixdata[x, y][:3]) == 255 * 3):
                    if color is None:
                        if img2 is None:
                            mainpixdata[x + posn[0], y + posn[1]] = pixdata[x, y]
                        else:
                            # try:
                            finaldata = (
                                min(
                                    int(
                                        pixdata[x, y][0] * p
                                        + pixdata2[x, y][0] * (1 - p)
                                    ),
                                    255,
                                ),
                                min(
                                    int(
                                        pixdata[x, y][1] * p
                                        + pixdata2[x, y][1] * (1 - p)
                                    ),
                                    255,
                                ),
                                min(
                                    int(
                                        pixdata[x, y][2] * p
                                        + pixdata2[x, y][2] * (1 - p)
                                    ),
                                    255,
                                ),
                            )
                            # except:
                            #    finaldata = pixdata[x,y]
                            mainpixdata[x + posn[0], y + posn[1]] = finaldata
                    else:
                        mainpixdata[x + posn[0], y + posn[1]] = color
    if img2 is not None:
        img2.close()
    img.close()


def removeImagePortion(img, x_min, x_max, y_min, y_max):
    pixdata = img.load()
    width, height = img.size
    bw, bh = img.size
    mainpixdata = img.load()
    for y in range(height):
        for x in range(width):
            if x_min < x and x < x_max and y_min < y and y < y_max:
                continue
            else:
                mainpixdata[x, y] = (0, 0, 0)
