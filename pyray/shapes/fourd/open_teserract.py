import numpy as np
import queue
from collections import defaultdict
from itertools import combinations
from pyray.shapes.solid.open_cube import char2coord
from pyray.rotation import general_rotation, rotate_points_about_axis
from pyray.misc import zigzag3
from PIL import Image, ImageDraw


class Cube():
	def __init__(self, val):
		self.x = char2coord(val[0])
        self.y = char2coord(val[1])
        self.z = char2coord(val[2])
        self.w = char2coord(val[3])
        self.cube_center = np.array([self.x, self.y, self.z, self.w])

