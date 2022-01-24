import matplotlib.pyplot as plt
import numpy as np
import scipy.fftpack as fftp
from PIL import Image, ImageDraw, ImageFont, ImageMath
from scipy.fftpack import fft
from scipy.io import wavfile  # get the api

from pyray.axes import *


def plt_fft(filename, plot=False):
    fs, data = wavfile.read(filename)  # load the data
    a = data.T[0]  # this is a two channel soundtrack, I get the first track
    c = fft(a)  # calculate fourier transform (complex numbers list)
    d = int(len(c) / 2)  # you only need half of the fft list (real signal symmetry)
    if plot:
        plt.plot(abs(c[1 : (d - 1)]), "r")
        plt.show()
    return abs(c[1 : (d - 1)])


def fourier_series(x, y, wn, n=None):
    # get FFT
    myfft = fftp.fft(y, len(y))
    # kill higher freqs above wavenumber wn
    # myfft[wn:-wn] = 0
    # make new series
    freqs = myfft[0 : int(len(myfft) / 2)]
    freqs[0] = 0
    freqs = np.concatenate((freqs, np.flip(freqs, 0)), axis=0)
    y2 = fftp.ifft(myfft)
    y2 = np.array([i.real for i in y2])
    plt.figure(num=None)
    plt.plot(x, y, x, y2)
    plt.show()


if __name__ == "__main__":
    x = np.array([float(i) for i in range(0, 360)])
    y = np.sin(2 * np.pi / 360 * x) + np.sin(2 * 2 * np.pi / 360 * x) + 5
    fourier_series(x, y, 3, 360)


##
def get_fft(filename="..\\sounds\\NYTLaurel.wav"):
    fs, data = wavfile.read(filename)  # load the data
    a = data.T[0]  # this is a two channel soundtrack, I get the first track
    b = [
        (ele / 2 ** 8.0) * 2 - 1 for ele in a
    ]  # this is 8-bit track, b is now normalized on [-1,1)
    c = fft(a)  # calculate fourier transform (complex numbers list)
    return c


def write_highpass(myfft, lowav=0, hiwav=0, writefile=False):
    fft1 = np.copy(myfft)  # Don't want  to change the original array.
    fft1[0:lowav] = fft1[0:lowav] * 0.0
    if lowav > 0:
        fft1[-lowav:] = (
            fft1[-lowav:] * 0.0
        )  # Remove all frequencies lower than this wave number.
    # hiwav = int(len(fft1)/2)-hiwav
    fft1[hiwav:-hiwav] = 0  # Remove all frequencies higher than this wave number.
    y2 = fftp.ifft(fft1)
    y2 = np.array([int(round(i)) for i in y2.real])
    y2 = np.array(
        y2, dtype=np.int16
    )  ## https://stackoverflow.com/questions/50431296/wavfile-write-identical-arrays-but-only-one-works
    if writefile:
        fs = 44100
        wavfile.write("..\\sounds\\Laurel_py.wav", fs, y2)
    return [y2, abs(fft1[1 : int(len(fft1) / 2)])]


def plot_wav(a, draw, rgba, frac=1.0, x_min=100, x_max=2000, y_frac=1.0, y_base=1000):
    a1 = a * y_frac + y_base
    prev = a[0]
    x1 = x_min
    for i in range(1, int(len(a1) * frac)):
        x2 = x1 + (x_max - x_min) / len(a1)
        draw.line((x1, a1[i - 1], x2, a1[i]), fill=rgba, width=3)
        x1 = x2


def sound_wav(
    filename="..\\sounds\\NYTLaurel.wav", filename1="..\\sounds\\MyLaurel.wav"
):
    # fs, data = wavfile.read(filename)
    # a = data.T[0]
    dfft = get_fft(filename)
    [a, dfft1] = write_highpass(dfft, lowav=0, hiwav=4000, writefile=False)
    dfft = dfft1
    dfft2 = get_fft(filename1)
    [a1, dfft1] = write_highpass(dfft2, lowav=0, hiwav=0, writefile=False)
    txt = "Links to the sound\nclip and python code\nused to perform the fourier\ntransform included in the\ndescription. And don't forget\nto like and\nsubscribe :)"
    # arrowV1(draw, np.eye(3), end=np.array([1200,140,0])/120.0, start=np.array([1500,140,0])/120.0, scale=120, shift=np.array([0,0,0]))
    for ii in range(35, 40):
        im = Image.new("RGB", (2048, 2048), (1, 1, 1))
        draw = ImageDraw.Draw(im, "RGBA")
        # plot_wav(a, draw, (137,80,195,120), i/30)
        plot_wav(a, draw, (120, 120, 120, 30), 1.0, 100, 600, 0.25, 250)
        plot_wav(a1, draw, (120, 120, 120, 30), 1.0, 100, 600, 0.25, 600 + 250)
        plot_wav(dfft, draw, (120, 120, 120, 120), 1.0, 1200, 1800, 1e-3, 250)
        plot_wav(dfft1, draw, (120, 120, 120, 120), 1.0, 1200, 1800, 5e-4, 600 + 250)
        i = 31
        # plot_wav(a, draw, (120,120,120,120), 1.0, 100, 2000-(-600+2000)*float(i)/31, 1.0-(-0.25+1.0)*float(i)/31, 1500-(1500-250)*float(i)/31)
        # plot_wav(a1, draw, (137,80,195,120), ii/30.0, 100, 600, 0.25, 600+250)
        writeStaggeredText(txt, draw, ii, (600, 1250))
        writeStaggeredText("Here be\n    Yanny", draw, 30, (1299, 113), (255, 0, 0))
        draw.ellipse((1246, 208, 1303, 396), fill=(0, 0, 0, 0), outline="red")
        im.save("..\\images\\RotatingCube\\im" + str(ii) + ".png")
