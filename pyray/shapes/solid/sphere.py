import os
import numpy as np
from PIL import Image, ImageDraw
from pyray.shapes.oned.circle import *
from pyray.rotation import rotation
from pyray.helpers import get_image_bytes
from pyray.shapes.solid.polyhedron import *
from pyray.shapes.solid.sphere_goldberg_252 import *

####################################################################################
# To understand what's going on, read the comments carefully _ Josephus 20:21 #
####################################################################################

def draw_rotating_sphere(number_of_circles, line_thickness, save_dir=None, is_stream=False):
    if not is_stream and save_dir is None:
        raise Exception("Save directory required when not streaming")
    # Create total 30 images
    for i in np.arange(30):
        # We'll rotate the sphere by 18 degrees (18 = pi/10)
        r = rotation(3, np.pi*i / 100.0)
        # Create the canvas size of (500, 500)
        im = Image.new("RGB", (500, 500), (1, 1, 1))
        draw = ImageDraw.Draw(im, 'RGBA')
        draw_sphere(draw, np.array([0,0,0]), np.array([0,0,1]), 1,
            r, num_circle = number_of_circles, rgba=(182, 183, 186, 255), width = line_thickness)
        if is_stream:
            yield get_image_bytes(im)
        else:
            file_name = save_dir + str(i) + '.png'
            im.save(file_name)


def draw_oscillating_sphere(save_dir, number_of_circles, line_thickness):
    # Craete total 60 images
    for i in np.arange(60):
        # 2.5 is an angle of Z axis
        # pi * sin(k) is an oscillating factor
        r = rotation(3, 2.5 + np.pi*np.sin(i/10.0) * np.random.uniform(0.75,1) / 20.0)
        # Create the canvas size of (500, 500)
        im = Image.new("RGB", (500, 500), (1, 1, 1))
        draw = ImageDraw.Draw(im, 'RGBA')
        # Sphere's center is np.array([0,0,0])
        # The vector that passes through the center is np.array([0,0,1])
        # Radius is oscillating randomly: 1 * np.random.uniform(0.75,1) + 0.4 * np.sin(np.pi/10.0*i)
        draw_sphere(draw, np.array([0,0,0]), np.array([0,0,1]),
            1 * np.random.uniform(0.75,1) + 0.4 * np.sin(np.pi/10.0*i), r, num_circle = number_of_circles,
            rgba=(182, 183, 186, 255), width = line_thickness)
        file_name = save_dir + str(i) + '.png'
        im.save(file_name)


def draw_wavy_sphere_wrapper(save_dir, number_of_circles, line_thickness):
    # Create n images (frames) where n = number_of_circles
    for i in np.arange(number_of_circles):
        wavy_index = i % number_of_circles
        # 2.52 is an angle of Z axis (Why do I choose 2.52? For an aesthetic reason:))
        r = rotation(3, 2.50 + np.pi*np.sin(i/10.0) * np.random.uniform(0.8,1) / 30.0)
        # Create the canvas size of (500, 500)
        im = Image.new("RGB", (500, 500), (1, 1, 1))
        draw = ImageDraw.Draw(im, 'RGBA')
        # Sphere's center is np.array([0,0,0])
        # The vector that passes through the center is np.array([0,0,1])
        # Radius is oscillating randomly
        draw_sphere(draw, np.array([0,0,0]), np.array([0,0,1]), 1, r,
            wavy_index = wavy_index ,num_circle = number_of_circles,
            rgba=(182, 183, 186, 255), width = line_thickness)
        file_name = save_dir + str(i) + '.png'
        im.save(file_name)


def draw_wavy_sphere_acceleration_wrapper(save_dir, number_of_circles, line_thickness):
    # Create n images (frames) where n = number_of_circles
    for i in np.arange(number_of_circles):
        wavy_index = i % number_of_circles
        if (wavy_index > 0.65*number_of_circles and wavy_index%2!=0):
            pass
        else:
            # 2.52 is an angle of Z axis (Why did I choose 2.52? For aesthetic reasons:))
            r = rotation(3, 2.50 + np.pi*np.sin(i/10.0) * np.random.uniform(0.8,1) / 30.0)
            # Create the canvas size of (500, 500)
            im = Image.new("RGB", (500, 500), (1, 1, 1))
            draw = ImageDraw.Draw(im, 'RGBA')
            # Sphere's center is np.array([0,0,0])
            # The vector that passes through the center is np.array([0,0,1])
            # Radius is oscillating randomly
            draw_sphere2(draw, np.array([0,0,0]), np.array([0,0,1]), 1, r,
                wavy_index = wavy_index ,num_circle = number_of_circles,
                rgba=(182, 183, 186, 255), width = line_thickness)
            file_name = save_dir + str(i) + '.png'
            im.save(file_name)


def draw_goldberg_sphere():
    faces = np.array([[sphere_vertices[j] for j in i] for i in sphere_faces])
    for i in range(30):
        im = Image.new("RGB", (2048, 2048), (1, 1, 1))
        draw = ImageDraw.Draw(im, 'RGBA')
        r = general_rotation(np.array([1,0,0]), 2*np.pi/30*i)
        render_solid_planes(faces, draw, r)
        im.save('im' + str(i) + '.png')


def draw_sphere(draw,
                center,
                vec,
                radius,
                rotation_matrix,
                num_circle,
                wavy_index=-1,
                scale=200,
                shift=np.array([250,
                                250,
                                0]),
                rgba=(255,
                      255,
                      255,
                      1),
                width=10):
    """
    Draws one (1) sphere as seen from a given angle.
    To make an animation of a sphere, you need to call this function multiple times.
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
        # Let's say the vec is [0, 0, z]. [0, 0, z]*[1, 1, 0] will be always
        # [0, 0, 0].
        orthogonal_vec = np.array([1, 1, 0])
    else:
        # For example, the orthogonal vector of [2, 1, 0] is [-1, 2, 0].
        orthogonal_vec = np.array([vec[1], -vec[0], 0])
    # Normalizing
    orthogonal_vec = orthogonal_vec / sum(orthogonal_vec**2)**0.5
    # theta is the angle that ranges from 0 to 180 degrees and is used to draw
    # multiple different sized circles that consist of the sphere
    theta_step = np.pi / num_circle
    # One Non-wavy sphere
    if wavy_index == -1:
        for j in range(0, num_circle):
            radius_runner = radius * np.sin(theta_step * j)
            # drawing a sphere with multiple circles by changing the z-axis
            center = np.array([0, 0, radius * np.cos(theta_step * j)])
            draw_circle(
                draw,
                center,
                vec,
                radius_runner,
                rotation_matrix,
                shift=shift,
                rgba=rgba,
                width=width)

    # One sphere with one ring
    else:
        for j in range(0, num_circle):
            if j == wavy_index:
                # Making wavy by adding 0.1
                radius_runner = radius * (np.sin(theta_step * j) + 0.05)
            else:
                radius_runner = radius * np.sin(theta_step * j)
            # drawing a sphere with multiple circles by changing the z-axis
            center = np.array([0, 0, radius * np.cos(theta_step * j)])
            draw_circle(
                draw,
                center,
                vec,
                radius_runner,
                rotation_matrix,
                shift=shift,
                rgba=rgba,
                width=width)
            # Make the radius smaller again.
            radius_runner -= 0.1


def draw_sphere2(draw,
                 center,
                 vec,
                 radius,
                 rotation_matrix,
                 num_circle,
                 wavy_index=-1,
                 scale=200,
                 shift=np.array([250,
                                 250,
                                 0]),
                 rgba=(255,
                       255,
                       255,
                       1),
                 width=10):
    """
    The only difference between draw_sphere2 and draw_sphere is draw_sphere2 accelerates the waves at the end.
    This is a bad code design. MUST refactor later. I'm on a roll in creating gifs so I'll just keep going.
    """
    # Make the vec a unit vector by dividing it by its length
    vec = vec / sum(vec**2)**0.5
    if vec[0] == 0 and vec[1] == 0:
        # Let's say the vec is [0, 0, z]. [0, 0, z]*[1, 1, 0] will be always
        # [0, 0, 0].
        orthogonal_vec = np.array([1, 1, 0])
    else:
        # For example, the orthogonal vector of [2, 1, 0] is [-1, 2, 0].
        orthogonal_vec = np.array([vec[1], -vec[0], 0])
    # Normalizing
    orthogonal_vec = orthogonal_vec / sum(orthogonal_vec**2)**0.5
    # theta is the angle that ranges from 0 to 180 degrees and is used to draw
    # multiple different sized circles that consist of the sphere
    theta_step = np.pi / num_circle
    # Non-wavy sphere
    if wavy_index == -1:
        for j in range(0, num_circle):
            radius_runner = radius * np.sin(theta_step * j)
            # drawing a sphere with multiple circles by changing the z-axis
            center = np.array([0, 0, radius * np.cos(theta_step * j)])
            draw_circle(
                draw,
                center,
                vec,
                radius_runner,
                rotation_matrix,
                shift=shift,
                rgba=rgba,
                width=width)

    # One sphere with one ring (with acceleration)
    else:
        if (wavy_index > 0.6 * num_circle and wavy_index %
                3 == 0):  # When it accelerates and waves
            # Drawing one sphere by creating n number of circles.
            for j in range(0, num_circle):
                if j == wavy_index:
                    # Making wavy by adding 0.1
                    radius_runner = radius * (np.sin(theta_step * j) + 0.05)
                else:
                    radius_runner = radius * np.sin(theta_step * j)
                # drawing a sphere with multiple circles by changing the z-axis
                center = np.array([0, 0, radius * np.cos(theta_step * j)])
                draw_circle(
                    draw,
                    center,
                    vec,
                    radius_runner,
                    rotation_matrix,
                    shift=shift,
                    rgba=rgba,
                    width=width)
                # Make the radius smaller again.
                radius_runner -= 0.1

        elif (wavy_index > 0.6 * num_circle and wavy_index % 2 != 0):
            # Do nothing (Later remove this condition. I added this for an
            # instructional purpose.)
            pass
        else:  # same as normal wavy shpere
            # Drawing one sphere by creating n number of circles.
            for j in range(0, num_circle):
                if j == wavy_index:
                    # Making wavy by adding 0.1
                    radius_runner = radius * (np.sin(theta_step * j) + 0.05)
                else:
                    radius_runner = radius * np.sin(theta_step * j)
                # drawing a sphere with multiple circles by changing the z-axis
                center = np.array([0, 0, radius * np.cos(theta_step * j)])
                draw_circle(
                    draw,
                    center,
                    vec,
                    radius_runner,
                    rotation_matrix,
                    shift=shift,
                    rgba=rgba,
                    width=width)
                # Make the radius smaller again.
                radius_runner -= 0.1


if __name__ == "__main__":
    # Create the directories to save image files
    save_dir_list = ['images\\RotatingSphereDense\\im',
                    'images\\RotatingSphereLight\\im',
                    'images\\RotatingOscillatingSphere\\im',
                    'images\\WavySphere\\im',
                    'images\\WavySphere_A\\im']
    for path in save_dir_list:
        if not os.path.exists(path):
            os.makedirs(path)

    # Dense sphere: Draw the sphere that consist of 40 circles with line thickness 1
    draw_rotating_sphere('images\\RotatingSphereDense\\im', 40, 1)

    # Light sphere: Draw the sphere that consist of 20 circles with line thickness 1
    draw_rotating_sphere('images\\RotatingSphereLight\\im', 20, 1)

    # Oscillating sphere: Draw the sphere that consist of n circles with line thickness 2
    draw_oscillating_sphere('images\\RotatingOscillatingSphere\\im', 20, 2)

    # Wavy sphere
    draw_wavy_sphere_wrapper('images\\WavySphere\\im', 66, 1)

    # Wavy sphere with acceleration
    draw_wavy_sphere_acceleration_wrapper('images\\WavySphere_A\\im', 66, 1)

