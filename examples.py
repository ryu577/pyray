import numpy as np
import os
from circle import * 
from rotation import *

####################################################################################
# If you read the comment carefully, you will probably understand what's going on. #
####################################################################################

def draw_rotating_hot_pink_sphere(save_dir, number_of_circles):
    # Craete total 30 images
    for i in np.arange(30):
        # We'll rotate the sphere by 18 degrees (18 = pi/10) 
        r = rotation(3, np.pi*i / 100.0)
        # Create the canvas size of (2024, 2024)
        im = Image.new("RGB", (2024, 2024), (1, 1, 1))
        draw = ImageDraw.Draw(im, 'RGBA')
        # Function is called here
        draw_sphere(draw, np.array([0,0,0]), np.array([0,0,1]), 1, r, num_circle = number_of_circles)
        # Save
        file_name = save_dir + str(i) + '.png'
        im.save(file_name)


def draw_oscillating_sphere(save_dir, number_of_circles):
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
        draw_sphere(draw, np.array([0,0,0]), np.array([0,0,1]), 1 * np.random.uniform(0.75,1) + 0.4 * np.sin(np.pi/10.0*i), r, num_circle = number_of_circles, rgba=(182, 183, 186, 255), width = 1)
        file_name = save_dir + str(i) + '.png'
        im.save(file_name)


def draw_wavy_sphere_wrapper(save_dir, number_of_circles):
    for i in np.arange(60):
        wavy_index = i % number_of_circles
        # 2.52 is an angle of Z axis (Why do I choose 2.52? For an aesthetic reason:))
        r = rotation(3, 2.50 + np.pi*np.sin(i/10.0) * np.random.uniform(0.8,1) / 30.0)
        # Create the canvas size of (500, 500)
        im = Image.new("RGB", (500, 500), (1, 1, 1))
        draw = ImageDraw.Draw(im, 'RGBA')
        # Sphere's center is np.array([0,0,0])
        # The vector that passes through the center is np.array([0,0,1])
        # Radius is oscillating randomly
        draw_sphere(draw, np.array([0,0,0]), np.array([0,0,1]), 1, r, wavy_index = wavy_index ,num_circle = number_of_circles, rgba=(182, 183, 186, 255), width = 2)
        file_name = save_dir + str(i) + '.png'
        im.save(file_name)


if __name__ == "__main__":
    # Create the directories to save image files
    save_dir_list = ['Images\\RotatingSphereDense\\im', 'Images\\RotatingSphereLight\\im', 'Images\\RotatingOscillatingSphere\\im']
    for path in save_dir_list:
        if not os.path.exists(path):
            os.makedirs(path)

    # Dense sphere: Draw the sphere that consist of 40 circles
    #draw_rotating_hot_pink_sphere(Images\\RotatingSphereDense\\im', 40)

    # Light sphere: Draw the sphere that consist of 20 circles
    #draw_rotating_hot_pink_sphere('Images\\RotatingSphereLight\\im', 20)

    # Oscillating sphere: Draw the sphere that consist of n circles
    #draw_oscillating_sphere('Images\\RotatingOscillatingSphere\\im', 20)

    draw_wavy_sphere_wrapper('Images\\RotatingOscillatingSphere\\im', 60)