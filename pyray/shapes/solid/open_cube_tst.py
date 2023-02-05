from pyray.shapes.solid.open_cube import *
from itertools import combinations, permutations
from pyray.rotation import general_rotation, rotate_points_about_axis,\
	axis_rotation


def tst_perspective(scale=40, e=4, c=-4):
    for ix in range(60):
        im = Image.new("RGB", (512, 512), (0, 0, 0))
        draw = ImageDraw.Draw(im, 'RGBA')
        #r = rotation(3, np.pi*ix/60.0)
        r = axis_rotation(np.array([0,0,0]), np.array([0,1,0]),
        					ix*2*np.pi/60)[:3,:3]
        for combo in combinations([0, 1, 2], 2):
            (ix1, ix2) = combo
            for p1 in ['+', '-']:
                for p2 in ['+', '-']:
                    fc_st = '000'
                    fc = list(fc_st)
                    fc[ix1] = p1
                    fc[ix2] = p2
                    f = Face(''.join(fc))
                    f.plot_perspective(draw, r, scale=scale,
                           shift=np.array([256, 256, 0, 0]),
                           rgba=(12, 90, 190, 90),
                           wdh=1,e=e, c=c)
        im.save("Images//RotatingCube//im" + str(ix).rjust(4, '0') + ".png")

