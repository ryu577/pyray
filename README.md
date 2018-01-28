# Introduction

I'm creating this repository in January 2018 and it is crazy that the best open source option for rendering 3d scenes remains POV ray.
Now, POV ray is a great program, but why can't we have that functionality (rendering 2d, 3d and higher dimensional objects and scenes) in Python, a language that is perhaps the most widely used already and only growing in popularity?
This code is a first step towards that goal - have the ability to do everything POV ray does - rendering complex 3d objects and scenes, animations and much more in plain, vanilla Python. I imagine this would find applications in creating videos, video games, physical simulations or just pretty pictures.

While there certainly is a very long way to go before this can be a reality, it won't happen without taking a first step. And of course, I could use help :)

Above all else, I want to emphasize simplicity in this library and minimize the dependence on external libraries so more people can hit the ground running with it.


# Demonstrations
So far, I've been using this to create YouTube videos for <a href="https://www.youtube.com/channel/UCd2Boc12Ora42VIJBULz0kA">my channel</a>.

Here are some that demonstrate the abilities of this code (also see below for some images created with it) - 

1. <a href="https://www.youtube.com/watch?v=KuXnrg1YpiY">Binomial coefficients on hypercubes.</a>

2. <a href="https://www.youtube.com/watch?v=OV7c6S32IDU&t=3s">Why does Gradient descent work?</a>

3. <a href="https://www.youtube.com/watch?v=STkcP5jcJYo">Introduction to Platonic solids</a>

4. <a href="https://www.youtube.com/watch?v=57g6nQGBFcY">Slice a 4d hypercube (Teserract).</a>

# Requirements
I've made every effort to keep the requirements for this project to the bare minimum so most people can get it running with almost no pain. These are - 
Python Imaging Library (PIL), numpy and scipy. For writing on math equations images using the methods in WriteOnImage.py, you'll need matplotlib and sympy. All of these can be installed quite easily with pip.

# Usage
To keep things simple and the dependencies minimal, the program simply writes an image or a series of images to the folder `./Images/RotatingCube` (this was the first object that was animated with this tool). 

You can run any method tagged @MoneyShot to see how this works. For example, you can run the following method from cube.py - 

```python
from cube import *
cube_with_cuttingplanes(7, popup=True)
```
and this will generate a colorful 3d cube with diagonal cutting planes shaded in different colors (in the ./Images/RotatingCube folder). Something like this - 

<a href="http://www.youtube.com/watch?feature=player_embedded&v=KuXnrg1YpiY" 
target="_blank"><img src="https://github.com/ryu577/pyray/blob/master/Images/RotatingCube/im0.png" 
alt="Image formed by above method" width="240" height="180" border="10" /></a>


You can now create a series of them using the following code - 

```python
for i in range(3, 15):
	cube_with_cuttingplanes(numTerms = i, im_ind = i-3)
```

The series of images can then be easily converted to a video using the open source <a href="https://ffmpeg.org/download.html">ffmpeg program</a>. For example

> ffmpeg -framerate 10 -f image2 -i im%d.png -vb 20M vid.avi

The video can then be converted to a .gif file if required - 

> ffmpeg -i vid.avi -pix_fmt rgb24 -loop 0 out.gif

For example, somthing like this:

<a href="https://www.youtube.com/watch?v=OV7c6S32IDU" 
target="_blank"><img src="https://github.com/ryu577/ryu577.github.io/blob/master/Downloads/GradientAscent/which_direction.gif" 
alt="Image formed by above method" width="240" height="180" border="10" /></a>


# Super Simple Example

>python examples.py

This will create a rotating pink sphere in `Images` folder.

