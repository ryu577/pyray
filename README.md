[![Build Status](https://travis-ci.com/ryu577/pyray.svg?branch=master)](https://travis-ci.com/ryu577/pyray)

# Introduction

I'm creating this repository in January 2018 and it is crazy that the best open source option for rendering 3d scenes remains POV ray.
Now, POV ray is a great program, but why can't we have that functionality (rendering 2d, 3d and higher dimensional objects and scenes) in Python, a language that is perhaps the most widely used already and only growing in popularity?
This code is a first step towards that goal - have the ability to do everything POV ray does - rendering complex 3d objects and scenes, animations and much more in plain, vanilla Python. I imagine this would find applications in creating videos, video games, physical simulations or just pretty pictures.

While there certainly is a very long way to go before this can be a reality, it won't happen without taking a first step. And of course, I could use help :)

Above all else, I want to emphasize simplicity in this library and minimize the dependence on external libraries so more people can hit the ground running with it.


# Installation
To install the library, run (pyray was taken on pypi):

```
pip install raypy
```

Make sure you have all the requirements (requirements.txt) installed. If not, you can run:

```
pip install -r requirements.txt
```

Alternately, you can fork/download the code and run from the main folder:

```
python setup.py install
```

# Requirements
I've made every effort to keep the requirements for this project to the bare minimum so most people can get it running with almost no pain. These are - 
Python Imaging Library (PIL), numpy and scipy. For writing on math equations images using the methods in WriteOnImage.py, you'll need matplotlib and sympy. All of these can be installed quite easily with `pip install -r requirements.txt`

# Usage
To keep things simple and the dependencies minimal, the program simply writes an image or a series of images to the folder `./Images/RotatingCube` (this was the first object that was animated with this tool). 

You can run any method tagged @MoneyShot to see how this works. For example, you can run the following method from cube.py - 

```python
from pyray.shapes.solid.cube import *
cube_with_cuttingplanes(7, popup=True)
```
and this will generate a colorful 3d cube with diagonal cutting planes shaded in different colors (in the folder where you run it from, file called im0.png). Something like this (click to see what happens) - 

<a href="http://www.youtube.com/watch?feature=player_embedded&v=KuXnrg1YpiY" 
target="_blank"><img src="https://github.com/ryu577/pyray/blob/master/Images/cube_planes.png" 
alt="Image formed by above method" width="240" height="240" border="10" align="center"/></a>


You can now create a series of them using the following code - 

```python
for i in range(3, 15):
	cube_with_cuttingplanes(numTerms = i, im_ind = i-3)
```

The series of images can then be easily converted to a video using the open source <a href="https://ffmpeg.org/download.html">ffmpeg program</a>. For example

> ffmpeg -framerate 10 -f image2 -i im%d.png -vb 20M vid.avi

The video can then be converted to a .gif file if required - 

> ffmpeg -i vid.avi -pix_fmt rgb24 -loop 0 out.gif

For example, something like this:


<a href="https://www.youtube.com/watch?v=OV7c6S32IDU" 
target="_blank"><img src="https://github.com/ryu577/ryu577.github.io/blob/master/Downloads/GradientAscent/which_direction.gif" 
alt="Image formed by above method" width="240" height="180" border="10" /></a>

In case you're wondering, you can generate the images used in the gif above via:

```python
from pyray.shapes.twod.plane import *
for i in range(20):
	best_plane_direction(im_ind=i)
```

If you think this is valuable, please star :)

# Contributing

We welcome any kind of contribution, bug report, suggestion, new module, etc. Anything is welcome.

# Install pre-commit hooks

The pre-commit hooks will run a set of linters and formmatters automatically against your code when
you commit. This enforces a common set of style standards and checks for common, simple mistakes in
code. If you have a project-specific set of hooks, install those instead. Otherwise, install the repo-wide hooks. From root:

```shell
pip install pre-commit
pre-commit install
```

# Other examples

To create a bouncy sphere or a wavy sphere, run 
```python
from pyray.shapes.solid.sphere import *
draw_wavy_sphere_wrapper('.\\im', 66, 1)
```

<img src="https://github.com/ryu577/pyray/blob/master/Images/WavySphere.gif" 
alt="Image formed by above method" width="240" height="240" border="10" /></a>

```python
import numpy as np;from PIL import Image, ImageDraw, ImageFont, ImageMath;from pyray.axes import *
from pyray.rotation import *;from pyray.axes import draw_2d_arrow, Path, ZigZagPath, draw_grid, draw_grey_grid
from pyray.misc import dist

im = draw_grid()
draw = ImageDraw.Draw(im,'RGBA')
pts = np.array([[0,0],[1,1],[5,-3]])
pth = Path(pts)
pth.zg.draw_lines(draw,i/10.0)
im.save("im" + str(i) + ".png")
```
<img src="https://camo.githubusercontent.com/a9229ef6577001fb21c262e75c472558061ee462/68747470733a2f2f73322e67696679752e636f6d2f696d616765732f416e6472655265666c636e2e676966" 
alt="Image formed by above method" width="240" height="240" border="10" /></a>


```python
from pyray.shapes.solid.polyhedron import *
basedir = '.\\'
tr = Tetartoid()
for i in range(0, 31):
    im = Image.new("RGB", (2048, 2048), (1,1,1))
    draw = ImageDraw.Draw(im, 'RGBA')
    r = general_rotation(np.array([0,1,0]), 2*np.pi*i/30)
    tr.render_solid_planes(draw, r, shift=np.array([1000, 1000, 0]), scale=750)
    im.save(basedir + "im" + str(i) + ".png")
```

<a href="https://www.youtube.com/watch?v=0JEFjS2fiTA&feature=youtu.be" 
target="_blank"><img src="https://github.com/ryu577/ryu577.github.io/blob/master/Downloads/tetartoid2.gif" 
alt="Image formed by above method" width="240" height="240" border="10" /></a>


```python
from pyray.shapes.twod.paraboloid import *
draw_paraboloids()
```

<a href="https://www.youtube.com/watch?v=acsSIyDugP0&t=53s" 
target="_blank"><img src="https://github.com/ryu577/ryu577.github.io/blob/master/Downloads/paraboloids.gif" 
alt="Image formed by above method" width="240" height="240" border="10" /></a>



```python
from pyray.shapes.zerod.pointswarm import *
points_to_bins()
```

<a href="https://www.youtube.com/watch?v=OV7c6S32IDU" 
target="_blank"><img src="https://github.com/ryu577/ryu577.github.io/blob/master/Downloads/classificn/classificn.gif" 
alt="Image formed by above method" width="240" height="240" border="10" /></a>

# Demonstrations
So far, I've been using this to create YouTube videos for <a href="https://www.youtube.com/channel/UCd2Boc12Ora42VIJBULz0kA">my channel</a>.

Here are some that demonstrate the abilities of this code (also see below for some images created with it) - 

1. <a href="https://www.youtube.com/watch?v=KuXnrg1YpiY">Binomial coefficients on hypercubes.</a>

2. <a href="https://www.youtube.com/watch?v=OV7c6S32IDU&t=3s">Why does Gradient descent work?</a>

3. <a href="https://www.youtube.com/watch?v=STkcP5jcJYo">Introduction to Platonic solids</a>

4. <a href="https://www.youtube.com/watch?v=57g6nQGBFcY">Slice a 4d hypercube (Teserract).</a>
