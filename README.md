# Introduction

I'm creating this repository in January 2018 and it is crazy that the best open source option for rendering 3d scenes remains POV ray.
Now, POV ray is a great program, but why can't we have that functionality in Python, a language that is perhaps the most widely used and only growing in popularity?
This code is a first step towards that goal - have the ability to do everything POV ray does - rendering complex 3d objects and scenes, animations and much more in plain, vanilla Python.
While there certainly is a very long way to go before this can be a reality, it won't happen without taking a first step. And of course, I could use help :)

Above all else, I want to emphasize simplicity in this library and minimize the dependence on external libraries so more people can hit the ground running with it.


# Demonstrations
So far, I've been using this to create YouTube videos for <a href="https://www.youtube.com/channel/UCd2Boc12Ora42VIJBULz0kA">my channel</a>.

Here are some that demonstrate the abilities of this code - 

1. <a href="https://www.youtube.com/watch?v=KuXnrg1YpiY">Binomial coefficients on hypercubes.</a>

2. <a href="https://www.youtube.com/watch?v=OV7c6S32IDU&t=3s">Why does Gradient descent work?</a>

3. <a href="https://www.youtube.com/watch?v=STkcP5jcJYo">Introduction to Platonic solids</a>

4. <a href="https://www.youtube.com/watch?v=57g6nQGBFcY">Slice a 4d hypercube (Teserract).</a>

# Requirements
I've made every effort to keep the requirements for this project to the bare minimum so most people can get it running with almost no pain. These are - 
Python Imaging Library


# Usage
To keep things simple and the dependencies minimal, the program simply writes an image or a series of images to the folder ./Images/RotatingCube (this was the first object that was animated with this tool). A series of images can be easily converted to a video using the open source <a href="https://ffmpeg.org/download.html">ffmpeg program</a>. Just run the command below once you have ffmpeg installed (set the frame rate as required).

> ffmpeg -framerate 10 -f image2 -i im%d.png -vb 20M vid.avi

The video can then be converted to a .gif file if required - 

> ffmpeg -i vid.avi -pix_fmt rgb24 -loop 0 out.gif

To check out the capabilities, you can simply run any method tagged @MoneyShot.


