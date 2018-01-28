import os
from circle import * 
from rotation import *


def draw_rotating_hot_pink_sphere(save_dir, number_of_circles):
    # Craete total 30 images
    for i in np.arange(30):
        # We'll rotate the sphere by 18 degrees (18 = pi/10) 
        r = rotation(3, np.pi*i / 10.0)
        im = Image.new("RGB", (2024, 2024), (1, 1, 1))
        draw = ImageDraw.Draw(im, 'RGBA')
        draw_sphere(draw, np.array([0,0,0]), np.array([0,0,1]), 1, r, num_circle = number_of_circles)
        file_name = save_dir + str(i) + '.png'
        im.save(file_name)


if __name__ == "__main__":
    # Create the directories to save image files
    save_dir_list = ['Images\\RotatingCubeDense\\im', 'Images\\RotatingCubeLight\\im']
    for path in save_dir_list:
        if not os.path.exists(path):
            os.makedirs(path)

    # Dense sphere: Draw the sphere that consist of 40 circles
    draw_rotating_hot_pink_sphere('Images\\RotatingCubeDense\\im', 40)

    # Light sphere: Draw the sphere that consist of 20 circles
    draw_rotating_hot_pink_sphere('Images\\RotatingCubeLight\\im', 20)