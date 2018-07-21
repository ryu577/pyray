import os
import numpy as np
from PIL import Image, ImageDraw
from pyray.shapes.circle import *
from pyray.rotation import rotation
from pyray.helpers import get_image_bytes

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
            # 2.52 is an angle of Z axis (Why do I choose 2.52? For an aesthetic reason:))
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

