import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageMath

from pyray.rotation import general_rotation


class Grid:
    def __init__(
        self,
        scale=64,
        origin=np.array([512, 512]),
        rot=np.eye(2),
        start=np.array([0, 0]),
        end=np.array([3, 3]),
        size=1,
        center=None,
    ):
        self.scale = scale
        self.origin = origin
        self.rot = rot
        self.start = start
        self.end = end
        self.size = size
        if center is None:
            self.center = start
        else:
            self.center = center

    def get_grid_pt(self, x, y):
        r = self.rot
        return (
            np.dot(r, np.array([x, -y]) + self.start - self.center) + self.center
        ) * self.scale + self.origin

    def draw(self, draw, fill="grey", width=2):
        x_extent = self.end[0] - self.start[0]
        y_extent = self.end[1] - self.start[1]
        for i in np.concatenate(
            (np.arange(0, x_extent, self.size), [x_extent]), axis=0
        ):
            h_start = self.get_grid_pt(self.start[0] + i, self.start[1])
            h_end = self.get_grid_pt(self.start[0] + i, self.end[1])
            draw.line(
                (h_start[0], h_start[1], h_end[0], h_end[1]), fill=fill, width=width
            )
        for i in np.concatenate(
            (np.arange(0, y_extent, self.size), [y_extent]), axis=0
        ):
            v_start = self.get_grid_pt(self.start[0], self.start[1] + i)
            v_end = self.get_grid_pt(self.end[0], self.start[1] + i)
            draw.line(
                (v_start[0], v_start[1], v_end[0], v_end[1]), fill=fill, width=width
            )

    def draw1(
        self,
        draw,
        r,
        start_pt=np.array([0, 0]),
        end_pt=np.array([7, -3]),
        origin=np.array([4 * 64, 10 * 64]),
        scale=64,
    ):
        vec = end_pt - start_pt
        up_ext = np.array([int((vec[0] + vec[1]) / 2), int((vec[0] + vec[1]) / 2)])
        down_ext = np.array([int((vec[0] - vec[1]) / 2), int((-vec[0] + vec[1]) / 2)])
        for i in range(abs(int(up_ext[0])) + 1):
            pt1 = np.dot(r, np.array([i, i]) + start_pt) * scale + origin
            pt2 = np.dot(r, np.array([i, i]) + down_ext + start_pt) * scale + origin
            draw.line((pt1[0], pt1[1], pt2[0], pt2[1]), fill="grey", width=2)
        ##
        for i in range(abs(int(down_ext[0])) + 1):
            pt1 = np.dot(r, np.array([i, -i]) + start_pt) * scale + origin
            pt2 = np.dot(r, np.array([i, -i]) + up_ext + start_pt) * scale + origin
            draw.line((pt1[0], pt1[1], pt2[0], pt2[1]), fill="grey", width=2)
