'''
Draw arbitrary planar circles viewed from any angle in 3d space.

We use two different coordinate systems in most of the code. 
The first is original coordinates. These are easiest to think of mathematically. 

For example, a unit cube will have a side of length 1. However, when we plot the cube on an image, 
we can't make its side only one pixel because then the cube will be so small. Therefore, 
we scale up each side and shift the coordinates so that one of the vertices of the cube, or its center, 
can be in the center of the image. (This is the second cordinate systems.)

We might also want to rotate the cube to see it from a different angle before plotting on the image. (rotation.py) 
The coordinate system which is ready for plotting directly on the image is called "image coordinates". When we just rotate the cube but don't scale and shift it, then the coordinate system is called "rotated coordinates".
'''

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageMath
import sys
from rotation import general_rotation
from rotation import rotation


def generalized_circle(draw, center, vec, radius, rotation_matrix, scale=100, shift=np.array([1000, 1000, 0]), rgba=(255, 122, 0, 100), width=5):
    """
    Draws a circle as seen from a given angle.
    args:
        draw: The draw object associated with image we are plotting on. Used to make lines, ellipses and planes on it.
        center: The center of the circle. Provided in original coordinates (see file header). Example: [0,0,0]
        vec: The vector that passes through the center and is perpendicular to the plane of the circle. 
             Provided in original coordinates (see file header). Example: np.array([0,0,1])
        radius: the radius of the circle.
        scale: The amount by which the whole plot is to be scaled.
        shift: The origin corresponds to this pixel on the images (first two coordinates).
        rgba: The color of the line.
    """
    # Make the vec a unit vector by dividing it by its length
    vec = vec / sum(vec**2)**0.5
    if vec[0] == 0 and vec[1] == 0:
        # Let's say the vec is [0, 0, z]. [0, 0, z]*[1, 1, 0] will be always [0, 0, 0].
        orthogonal_vec = np.array([1, 1, 0])
    else:
        # For example, the orthogonal vector of [2, 1, 0] is [-1, 2, 0].
        orthogonal_vec = np.array([vec[1], -vec[0], 0])
    # Normalizing
    orthogonal_vec = orthogonal_vec / sum(orthogonal_vec**2)**0.5
    # We are drawing the circle from the rotation_starting_point
    rotation_starting_point = center + radius * orthogonal_vec
    rotation_starting_point = np.dot(rotation_matrix, rotation_starting_point)
    # We complete drawing the circle with 80 steps
    theta = np.pi * 2.0 / 80.0
    # runner is a 3-dimensional rotation matrix that rotates by incremental amount.
    runner = general_rotation(np.dot(rotation_matrix, vec), theta)
    for j in range(0, 80):
        rotation_ending_point = np.dot(runner, rotation_starting_point)
        draw.line((rotation_starting_point[0] * scale + shift[0], rotation_starting_point[1] * scale + shift[1], 
                    rotation_ending_point[0] * scale + shift[0], rotation_ending_point[1] * scale + shift[1]), 
                    fill=rgba, width=width)
        rotation_starting_point = rotation_ending_point


def draw_sphere(draw, center, vec, radius, rotation_matrix, num_circle, wavy_index=-1, scale=200, shift=np.array([250, 250, 0]), rgba=(255, 255, 255, 1), width=10):
    """
    Draws a sphere as seen from a given angle.
    args:
        draw: The draw object associated with image we are plotting on. 
        center: The center of the sphere. Provided in original coordinates (see file header). Example: [0,0,0]
        vec: The vector that passes through the center and is perpendicular to the plane of the circles of the sphere. 
             Provided in original coordinates (see file header). Example: np.array([0,0,1])
        radius: the radius of the sphere.
        num_circle: the number of circles that consist of the sphere
        scale: The amount by which the whole plot is to be scaled.
        shift: The origin corresponds to this pixel on the images. 
               Specifically in this method, it is set as [250, 250, 0] because in example.py, 
               we create the smaller canvas whose size is [500, 500]
        rgba: The color of the line.
    """
    # Make the vec a unit vector by dividing it by its length
    vec = vec / sum(vec**2)**0.5
    if vec[0] == 0 and vec[1] == 0:
        # Let's say the vec is [0, 0, z]. [0, 0, z]*[1, 1, 0] will be always [0, 0, 0].
        orthogonal_vec = np.array([1, 1, 0])
    else:
        # For example, the orthogonal vector of [2, 1, 0] is [-1, 2, 0].
        orthogonal_vec = np.array([vec[1], -vec[0], 0])
    # Normalizing
    orthogonal_vec = orthogonal_vec / sum(orthogonal_vec**2)**0.5
    # theta is the angle that ranges from 0 to 180 degrees and is used to draw multiple different sized circles that consist of the sphere
    theta_step = np.pi / num_circle
    # Non-wavy sphere
    if wavy_index == -1:
        for j in range(0, num_circle):
            radius_runner = radius * np.sin(theta_step*j) 
            # drawing a sphere with multiple circles by changing the z-axis 
            center = np.array([0,0, radius * np.cos(theta_step*j)])
            draw_circle(draw, center, vec, radius_runner, rotation_matrix, shift=shift, rgba = rgba, width = width)
    
    # Wavy sphere
    else:
        for j in range(0, num_circle):
            if j == wavy_index:
                # Making wavy by adding 0.1
                radius_runner = radius * (np.sin(theta_step*j) + 0.05)
            else:
                radius_runner = radius * np.sin(theta_step*j) 
            # drawing a sphere with multiple circles by changing the z-axis 
            center = np.array([0,0, radius * np.cos(theta_step*j)])
            draw_circle(draw, center, vec, radius_runner, rotation_matrix, shift=shift, rgba = rgba, width = width)
            # Make the radius smaller again.
            radius_runner -= 0.1



def draw_sphere2(draw, center, vec, radius, rotation_matrix, num_circle, wavy_index=-1, scale=200, shift=np.array([250, 250, 0]), rgba=(255, 255, 255, 1), width=10):
    """
    The only difference between draw_sphere2 and draw_sphere is draw_sphere2 accelerates the 
    """
    # Make the vec a unit vector by dividing it by its length
    vec = vec / sum(vec**2)**0.5
    if vec[0] == 0 and vec[1] == 0:
        # Let's say the vec is [0, 0, z]. [0, 0, z]*[1, 1, 0] will be always [0, 0, 0].
        orthogonal_vec = np.array([1, 1, 0])
    else:
        # For example, the orthogonal vector of [2, 1, 0] is [-1, 2, 0].
        orthogonal_vec = np.array([vec[1], -vec[0], 0])
    # Normalizing
    orthogonal_vec = orthogonal_vec / sum(orthogonal_vec**2)**0.5
    # theta is the angle that ranges from 0 to 180 degrees and is used to draw multiple different sized circles that consist of the sphere
    theta_step = np.pi / num_circle
    # Non-wavy sphere
    if wavy_index == -1:
        for j in range(0, num_circle):
            radius_runner = radius * np.sin(theta_step*j) 
            # drawing a sphere with multiple circles by changing the z-axis 
            center = np.array([0,0, radius * np.cos(theta_step*j)])
            draw_circle(draw, center, vec, radius_runner, rotation_matrix, shift=shift, rgba = rgba, width = width)
    
    # Wavy sphere
    else:
        for j in range(0, num_circle):
            if j == wavy_index:
                # Making wavy by adding 0.1
                radius_runner = radius * (np.sin(theta_step*j) + 0.05)
            else:
                radius_runner = radius * np.sin(theta_step*j) 
            # drawing a sphere with multiple circles by changing the z-axis 
            center = np.array([0,0, radius * np.cos(theta_step*j)])
            draw_circle(draw, center, vec, radius_runner, rotation_matrix, shift=shift, rgba = rgba, width = width)
            # Make the radius smaller again.
            radius_runner -= 0.1



def generalized_circle2(draw, center, vec, radius, r, scale=200, shift=np.array([1000, 1000, 0]), rgba=(255, 20, 147, 250), width=5):
    """
    Basically the same as generalized_circle but the center and vec are expected in the rotated coordinates (image coordinates).
    args:
        draw: The draw object associated with image we are plotting on. Used to make lines, ellipses and planes on it.
        center: The center of the circle. Provided in image coordinates (see file header).
        vec: The vector that passes through the center and is perpendicular to the plane of the circle. Provided in image coordinates (see file header).
        radius: the radius of the circle.
        scale: The amount by which the whole plot is to be scaled.
        shift: The origin corresponds to this pixel on the images (first two coordinates).
        rgba: The color of the line. 
    """
    vec = vec / sum(vec**2)**0.5
    if vec[0] == 0 and vec[1] == 0:
        orthogonal_vec = np.array([1, 1, 0])
    else:
        orthogonal_vec = np.array([vec[0], -vec[1], 0])
    orthogonal_vec = orthogonal_vec / sum(orthogonal_vec**2)**0.5
    pt1 = np.dot(r, center) + radius * np.dot(r, orthogonal_vec)
    # Make the parameter 30000 smaller for grainy drawing
    theta = np.pi * 2.0 / 30.0
    r1 = general_rotation(np.dot(r, vec), theta)
    for j in range(0, 30):
        pt2 = np.dot(r1, pt1)
        draw.line((pt1[0] * scale + shift[0], 
                    pt1[1] * scale + shift[1], 
                    pt2[0] * scale + shift[0], 
                    pt2[1] * scale + shift[1]), fill=rgba, width=width)
        pt1 = pt2


def generalized_arc(draw, r, center, vec, point, radius, prcnt=1, rgba=(255, 0, 0, 100), scale=200, shift=np.array([1000, 1000, 0])):
    """
    Same as generalized_circle, but instead of drawing the whole circle, only draws a portion of it.
    """
    pt1 = np.dot(r, point)
    vec = vec / sum(vec**2)**0.5
    theta = np.pi * 2.0 / 80.0 * prcnt
    r1 = general_rotation(np.dot(r, vec), theta)
    for j in range(0, 80):
        pt2 = np.dot(r1, pt1)
        #draw.ellipse( (pt2[0]-2,pt2[1]-2,pt2[0]+2,pt2[1]+2), fill = (68,193,195), outline = (68,193,195))
        draw.line((pt1[0] * scale + shift[0], pt1[1] * scale + shift[1], pt2[0]
                   * scale + shift[0], pt2[1] * scale + shift[1]), fill=rgba, width=5)
        pt1 = pt2


def draw_circle(draw, center, vec, radius, rotation_matrix, scale=200, shift=np.array([1000, 1000, 0]), rgba=(255, 122, 0, 50), width=5):
    """
    A simple wrapper for generalized_circle2.
    """
    generalized_circle2(draw, center, vec, radius,
                        rotation_matrix, scale, shift, rgba, width)


def draw_circle_x_y(
        draw, r, center=np.array([1, 1]), radius=1,
        start=np.array([0.0, 1.0, 0.0]), arcExtent=180.0, rgba=(102, 255, 51, 100), width=5,
        shift=np.array([1000, 1000, 0]), scale=200):
    """
    Draws a circle in the x-y plane.
    args:
        center : The center of the circle in original coordinate system.
        radius : The radius of the circle in original coordinate system.
    """
    if len(center) == 2:
        center = np.concatenate((center, np.array([0])), axis=0)
    center = np.dot(r, center) * scale
    shift1 = shift[:3] + center
    pt1 = np.dot(r, start)
    ##
    theta = np.pi * 2.0 / 180.0
    rot = general_rotation(np.dot(r, np.array([0, 0, 1])), theta)
    for j in range(0, arcExtent):
        pt2 = np.dot(rot, pt1)
        #draw.line((pt1[0]*scale + shift1[0], pt1[1]*scale+shift1[1], pt2[0]*scale+shift1[0], pt2[1]*scale+shift1[1]), fill=(153, 153, 255,100), width=5)
        draw.line((pt1[0] * scale + shift1[0], pt1[1] * scale + shift1[1], pt2[0]
                   * scale + shift1[0], pt2[1] * scale + shift1[1]), fill=rgba, width=width)
        pt1 = pt2


def project_circle_on_plane(
        draw, r, center=np.array([1, 1]), radius=1, plane=np.array([4.5, 4.5, 4.5]),
        start=np.array([0.0, 1.0, 0.0]), arcExtent=180.0,
        shift=np.array([1000, 1000, 0]), scale=200):
    """
    Draws the projection of a circle onto a plane.
    args:
        center : The center of the circle in original coordinate system.
        radius : The radius of the circle in original coordinate system.
        plane : The intercepts of the plane on the x, y and z axes.
        start : The point at which to start drawing the arc. It should be ensured that this point lies on the circle.
        arcEctent : The angle the arc is to make.
    """
    [a, b, c] = plane
    center = np.concatenate((center, np.array([0])), axis=0)
    center1 = np.dot(r, center) * scale
    shift1 = shift[:3] + center1
    pt1 = np.dot(r, start)
    [x, y] = np.array([0.0, radius])
    z = c * (1 - x / a - y / b)
    pt1Up = np.dot(r, np.array([x, y, z]))
    ##
    theta = np.pi * 2.0 / 180
    rot = general_rotation(np.dot(r, np.array([0, 0, 1])), theta)
    for j in range(0, arcExtent):
        pt2 = np.dot(rot, pt1)
        pt2Orig = np.dot(np.transpose(r), pt2) + center
        [x, y] = pt2Orig[:2]
        z = c * (1 - x / a - y / b)
        pt2Up = np.dot(r, np.array([x, y, z]))
        if sum((pt1Up - pt2Up)**2) < 0.1:
            draw.line((pt1Up[0] * scale + shift[0], pt1Up[1] * scale + shift[1], pt2Up[0] *
                       scale + shift[0], pt2Up[1] * scale + shift[1]), fill=(102, 102, 255, 100), width=5)
            #draw.line((pt1Up[0]*scale + shift[0], pt1Up[1]*scale+shift[1], pt2Up[0]*scale+shift[0], pt2Up[1]*scale+shift[1]), fill=(102,255,51,100), width=5)
        # The vertical lines clibing up.
        draw.line((pt2[0] * scale + shift1[0], pt2[1] * scale + shift1[1], pt2Up[0] *
                   scale + shift[0], pt2Up[1] * scale + shift[1]), fill=(51, 102, 255, 100), width=5)
        pt1 = pt2
        pt1Up = pt2Up


def project_circle_on_surface(draw, r, fn, center=np.array([0, 0]), radius=0.75, start=np.array([0.0, 0.75, 0.0]), arcExtent=180.0, shift=np.array([1000, 1000, 0]), scale=300):
    """
    Draws the projection of a circle onto an arbitrary surface defined by the function, fn.
    """
    center = np.concatenate((center, np.array([0])), axis=0)
    center1 = np.dot(r, center) * scale
    shift1 = shift[:3] + center1
    pt1 = np.dot(r, start)
    [x, y] = np.array([0.0, radius])
    z = fn(np.matrix([x, y]))
    pt1Up = np.dot(r, np.array([x, y, z]))
    theta = np.pi * 2.0 / 180
    rot = general_rotation(np.dot(r, np.array([0, 0, 1])), theta)
    for j in np.arange(0, arcExtent):
        pt2 = np.dot(rot, pt1)
        pt2Orig = np.dot(np.transpose(r), pt2) + center
        [x, y] = pt2Orig[:2]
        z = fn(np.matrix([x, y]))
        pt2Up = np.dot(r, np.array([x, y, z]))
        if sum((pt1Up - pt2Up)**2) < 0.1:
            draw.line((pt1Up[0] * scale + shift[0], pt1Up[1] * scale + shift[1], pt2Up[0] *
                       scale + shift[0], pt2Up[1] * scale + shift[1]), fill=(102, 102, 255, 100), width=7)
        # The vertical lines clibing up.
        draw.line((pt2[0] * scale + shift1[0], pt2[1] * scale + shift1[1], pt2Up[0] *
                   scale + shift[0], pt2Up[1] * scale + shift[1]), fill=(51, 102, 255, 100), width=8)
        pt1 = pt2
        pt1Up = pt2Up


